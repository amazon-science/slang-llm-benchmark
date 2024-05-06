# Toward Informal Language Processing: Knowledge of Slang in Large Language Models - Code and Data Repository

#### By: [Zhewei Sun](http://www.cs.toronto.edu/~zheweisun/) and [Qian Hu](https://www.amazon.science/author/qian-hu)

This is the GitHub repository for the upcoming NAACL paper "[Toward Informal Language Processing: Knowledge of Slang in Large Language Models](https://arxiv.org/abs/2404.02323)".

## OpenSubtitles-Slang Dataset

We contribute a comprehensive LLM benchmark dataset - <b>OpenSub-Slang</b> - constructed from movie subtitles from the [OpenSubtitles corpus](https://opus.nlpl.eu/legacy/OpenSubtitles.php) ([Lison and Tiedemann, 2016](https://aclanthology.org/L16-1147/)). We hope that our resource will serve as a standard benchmark for NLP research on slang, as well as serving as a data resource for further development of NLP systems by the wider community.

Our dataset contains 25,000 human-annotated sentences in total, of which 7,488 contain slang usages and 17,512 do not contain any slang usage. All sentences are paired with meta-data (region and year of production) associated with the originating movie. Each slang-containing sentence also comes with an annotator confidence (out of 3) indicating how many of the three annotators flagged the sentence as containing slang. For the slang-containing subset with high annotator confidence, further human annotation was performed to provide definition sentences and one-word paraphrases for the slang terms.

For more details regarding specification of the dataset, please see our paper:

https://arxiv.org/abs/2404.02323

Here are a few examples from our dataset:


| Sentence | Full context | Slang term | Annotator confidence | Movie ID | Sentence ID | Region | Year | Definition sentence | Literal paraphrase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | 
| My wife's had an accident with some Quaaludes. | - I'm up. \<i> My wife's had an accident with some Quaaludes. \</i> - So tired. | quaaludes | 2 | 54446 | 1497 | US | 2000 | a type of sedative or tranquilizer drug, specifically the brand name for the drug methaqualone. in the context provided, it suggests that the speaker's wife has had an accident while under the influence of quaaludes. | tranquilizers |
| You just can't put me on watch dog anymore, all right? | Dude, you don't have to leave, all right? \<i> You just can't put me on watch dog anymore, all right? \</i> Yeah.|watch dog| 2| 5905224| 200| US| 2012| someone who is assigned to keep a lookout or guard over something or someone, often as a form of punishment or restriction.| guardian|
|Sammy only had one eye, but he cut quite a figure.| No, they're right. \<i> Sammy only had one eye, but he cut quite a figure. \</i> I know what you're doing.| cut| 2| 4744540| 21| US| 2012| to present oneself or dress stylishly and attractively.|dress|
|I'll sort it, I promise you.| I'll have a word with Woody. \<i> I'll sort it, I promise you. \</i> I just feel really bad.|sort| 2| 3179568| 1315| UK| 2006| fix, mend|fix|
|Tommy Douglas... was my best mate.| Who's going to take the fall for Dougie? \<i> Tommy Douglas... was my best mate. \</i> Yeah, a mate with a grudge and a big mouth.|mate| 3| 3472293| 1038| UK| 2009| friend, comrade|friend|

## Data Distribution

We release our dataset under the [CC BY-NC license](https://creativecommons.org/licenses/by-nc/4.0/deed.en). We distribute only the meta-data necessary to reconstruct the full dataset from the OpenSubtitles corpus. To facilitate this process, we provide a Python script (`reconstruct_data.py`) that automatically reconstructs the full dataset from OpenSubtitles and our released meta-data.

Step-by-step instructions for obtaining the dataset:

1. Download and extract the monolingual English subset of the OpenSubtitles corpus (we used the [legacy version](https://opus.nlpl.eu/legacy/download.php?f=OpenSubtitles/v2018/xml/en.zip)). Once you have done this, there should be a folder named `en` in the working directory.

2. Download and place the meta-data files (`slang_OpenSub_meta.tsv` and `slang_OpenSub_negatives_meta`) and the reconstruction script (`reconstruct_data.py`) under the same working directory.

3. Run the provided Python script:
``` python3 reconstruct_data.py```
The full data set can be found in `slang_OpenSub.tsv` and `slang_OpenSub_negatives.tsv` in the same working directory.

If you experience any difficulties in obtaining the dataset, please contact the authors.

## Published Results

We use the subsets with high annotator confidence to construct two LLM benchmarks for slang processing: 1) Slang detection and 2) Slang source identification. We provide the necessary code (`Eval-Slang.ipynb`) and data indices (`slang_llm_inds.npz`) to reproduce our results. We summarize our results below:

### Slang detection - Sentence level

| Model | Precision | Recall | F1 score |
| --- | ---: | ---: | ---: |
|BERT| 80.1 | 83.3 | 81.6|
|RoBERTa | 81.3 | 87.5 | 84.2|
|XLNet | 67.5 | 64.3 | 64.6|
|GPT-3 zero-shot | **90.0** | 74.4 | 81.4|
|GPT-3.5 zero-shot | 87.5 | 80.8 | 84.0|
|GPT-4 zero-shot | 88.2 | 80.9 | 84.4|
|GPT-3.5 finetuned | 84.3 | **96.8** | **90.1**|

### Slang detection - Word level

| Model | Precision | Recall | F1 score |
| --- | ---: | ---: | ---: |
BERT | 75.5 | 62.5 | 68.3 
RoBERTa | 74.9 | 68.2 | 71.4 
XL-Net | 62.4 | 43.3 | 51.0 
GPT-3 zero-shot | 49.2 | 59.9 | 54.0 
GPT-3.5 zero-shot | 57.6 | 73.2 | 64.5 
GPT-4 zero-shot | 60.4 | 68.2 | 64.1 
GPT-3.5 finetuned | **74.5** | **81.3**| **77.8**

### Slang source identification

| Model | Original | Masked slang | Masked content |
| --- | ---: | ---: | ---: |
BERT |62.8%|58.7%|62.4%
RoBERTa |66.1%|61.3%|61.3%
XL-Net|55.9%|54.8%|57.1%
GPT-3 zero-shot |67.0%|58.5%|61.7%
GPT-3.5 zero-shot |67.6%|**62.2%**|**66.0%**
GPT-4 zero-shot |71.3%|**62.2%**|59.0%
GPT-3.5 finetuned |**72.9%**|55.9%|63.3%

For more detailed results, please see our paper.
