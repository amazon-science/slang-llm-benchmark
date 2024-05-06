This is the supplementary data package for the NAACL paper 'Toward Informal Language Processing: Knowledge of Slang in Large Language Models'.

We release OpenSubtitles-Slang (OpenSub-Slang), a subset of OPUS OpenSubtitles corpus containing slang related annotations. Our release contains only meta-data information necessary to reconstruct the data, as well as further annotations contributed by our work. This includes two sets of data:

1) slang_OpenSub_meta.tsv - This file contains all entries in which at least one out the three annotators identified a slang within the sentence. For those with at least 2/3 annotator agreement, the entries are also annotated with definition sentences for the slang and its literal paraphrases. Note that some of such entries having missing annotations due to annotation quality control.

2) slang_OpenSub_negatives_meta.tsv - This file contains all entries in which all three annotators believe that the corresponding sentence does not contain any slang usage.

To reconstruct the full data set, download the English monolingual dataset from the OpenSubtitles corpus and run the following script:

3) reconstruct_data.py

We also release the data indices used in our experiments to facilitate reproducible results. These indices can be found in:

4) slang_llm_inds.npz

Please refer to the Jupyter notebook 'Eval-Slang.ipynb' in the /Code package for example usage.

Each entry of the dataset contains the following data fields:

[SENTENCE]
The sentence in which annotators are asked to identify slang.

[FULL_CONTEXT]
The preceding and succeeding sentence in the movie script combined with the main sentence. This includes three sentences. The second of which is the main sentence with annotation. The main sentence is surrounded by <i> and </i> tags.

[SLANG_TERM]
The slang term identified by the annotators.

[ANNOTATOR_CONFIDENCE']
The annotator's confidence for sentences containing slang usage. This ranges from 1 to 3. A confidence score of 2 or above means that the annotators agreed on the exact slang term used in the sentence.

[MOVIE_ID]
The OpenSubtitles movie ID associated with the movie in which the sentence originates from. The movie ID can be queried on OpenSubtitles for movie metadata (e.g. https://www.opensubtitles.org/en/subtitles/3151540 where '3151540' is the movie ID).

[SENT_ID]
The sentence ID associated with the main sentence as given in the OPUS OpenSubtitles corpus.

[REGION]
The region in which the corresponding movie was produced in. In this release, it is either 'US' or 'UK'.

[YEAR]
The year in which the corresponding movie was produced in. All movies sampled for this release were produced after the year 2000.

[DEFINITION_SENTENCE']
A definition sentence of the slang usage in context as provided by the annotators.

[DEFINITION_SOURCE_URL]
The source of the definition sentence given, if the annotators provided one.

[LITERAL_PARAPHRASE_OF_SLANG]
Literal paraphrase of the slang term in context.

See Table 5 in the paper for a complete list of movies annotated.

All movie scripts annotated in this dataset are obtained from the OPUS OpenSubtitles corpus (https://opus.nlpl.eu/OpenSubtitles.php) which is based on user contributed movie subtitles collected by OpenSubtitles (http://www.opensubtitles.org/).