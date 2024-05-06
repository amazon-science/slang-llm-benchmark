import xml.etree.ElementTree as ET
import string
import glob, os
import numpy as np
import pandas as pd
import re

from copy import deepcopy
from tqdm import trange

punctuations = set(string.punctuation)
re_multispace = re.compile(r"\s+")
re_xml = re.compile(r"/([0-9]+).xml")

data_dir_prefix = "en/OpenSubtitles/xml/en/"

def parse_xml_file(xml_file):

    def _parse_s_block(iterator, s_block):
        while True:
            event, element = next(iterator)
            if element.tag == 'time' and event == 'start':
                time_id = element.attrib['id']
                time_val = element.attrib['value']
                if 'S' in time_id:
                    s_block['start_time'] = time_val
                elif 'E' in time_id:
                    s_block['end_time'] = time_val
            if element.tag == 'w' and event == 'start':
                s_block['text'].append(element.text)
            if element.tag == 's' and event == 'end':
                return s_block

    iterator = ET.iterparse(xml_file, events=['start', 'end'])
    blocks = []
    while True:
        try:
            event, element = next(iterator)
            if element.tag == 's' and event == 'start':
                s_block = {'id': None, 'start_time': None, 'end_time': None, 'text': []}
                s_block['id'] = element.attrib['id']
                s_block = _parse_s_block(iterator, s_block)
                # print(s_block)
                blocks.append(s_block)
        except StopIteration:
            break
    return blocks


def remove_space_before_punctuation(text):
    if len(text) <= 1:
        return text

    idx = 1
    new_text = [text[0]]
    while idx < len(text):
        if text[idx][0] in punctuations:
            new_text[-1] = new_text[-1] + text[idx]
        else:
            new_text.append(text[idx])
        idx += 1
    return new_text


def stringfy_block_with_idx_and_time(block):
    id = block['id']
    start_time = block['start_time']
    end_time = block['end_time']
    text = block['text']
    text = [item for item in text if item is not None]
    text = remove_space_before_punctuation(text)
    text = ' '.join(text)
    s = (
        f'id = {id} start_time = {start_time} end_time = {end_time}\n'
        f'{text}\n'
    )
    return s


def stringfy_block_with_pure_text(block):
    text = block['text']
    text = [item for item in text if item is not None]
    text = remove_space_before_punctuation(text)
    text = ' '.join(text)
    return text


def process_file(in_file):
    blocks = parse_xml_file(in_file)
    blocks = [stringfy_block_with_idx_and_time(block) for block in blocks]
    file_content = '\n'.join(blocks)
    return file_content

def lookup_sent(movie_id, sent_id):
    sent_id = int(sent_id)
    sents = movie_sents[movie_id][sent_id-2:sent_id+1]
    return sents[1].strip(), (sents[0]+" <i> "+sents[1]+" </i> "+sents[2]).strip()

data_meta = pd.read_csv('slang_OpenSub_meta.tsv', dtype=str, sep='\t').fillna('').values
movie_ids = data_meta[:,2]
sent_ids = data_meta[:,3]
movie_years = data_meta[:,5]

data_neg_meta = pd.read_csv('slang_OpenSub_negatives_meta.tsv', dtype=str, sep='\t').fillna('').values
movie_ids_neg = data_neg_meta[:,0]
sent_ids_neg = data_neg_meta[:,1]

movie_set = set(movie_ids)
movie_list = sorted(list(movie_set))
year_list = [str(s) for s in sorted(list(set(movie_years)))]

print("Finding XML files for relevant movies...")

movie_files = {}

for y in year_list:
    for d in glob.glob(data_dir_prefix+y+"/*"):
        for f in glob.glob(d+"/*"):
            match = re_xml.search(f)
            if match is not None:
                movie_id = match.group(1)
                if movie_id in movie_set:
                    movie_files[movie_id] = f

print("DONE")

print("Extracting sentences from movie subtitles...")

movie_sents = {}

for m in trange(len(movie_list)):
    m_id = movie_list[m]
    lines = process_file(movie_files[m_id]).split('\n')

    all_sents = []
    for i in range(1, len(lines), 3):
        all_sents.append(re_multispace.sub(' ', lines[i].strip()))
    movie_sents[m_id] = np.asarray(all_sents)

print("DONE")

print("Reconstructing and saving full dataset...")

data_sents = []
data_contexts = []

data_neg_sents = []
data_neg_contexts = []

for i in range(len(movie_ids)):
    sents, contexts = lookup_sent(movie_ids[i], sent_ids[i])
    data_sents.append(sents)
    data_contexts.append(contexts)

for i in range(len(movie_ids_neg)):
    sents, contexts = lookup_sent(movie_ids_neg[i], sent_ids_neg[i])
    data_neg_sents.append(sents)
    data_neg_contexts.append(contexts)

data_sents = np.asarray(data_sents)
data_contexts = np.asarray(data_contexts)

data_neg_sents = np.asarray(data_neg_sents)
data_neg_contexts = np.asarray(data_neg_contexts)

output = pd.DataFrame(np.hstack([data_sents[:,None], data_contexts[:,None], data_meta]), columns=['SENTENCE', 'FULL_CONTEXT', 'SLANG_TERM', 'ANNOTATOR_CONFIDENCE', 'MOVIE_ID', 'SENT_ID', 'REGION', 'YEAR', 'DEFINITION_SENTENCE', 'DEFINITION_SOURCE_URL', 'LITERAL_PARAPHRASE_OF_SLANG'])

output.to_csv('slang_OpenSub.tsv', sep='\t', index=False)

output_neg = pd.DataFrame(np.hstack([data_neg_sents[:,None], data_neg_contexts[:,None], data_neg_meta]), columns=['SENTENCE', 'FULL_CONTEXT', 'MOVIE_ID', 'SENT_ID', 'REGION', 'YEAR'])

output_neg.to_csv('slang_OpenSub_negatives.tsv', sep='\t', index=False)

print("DONE")