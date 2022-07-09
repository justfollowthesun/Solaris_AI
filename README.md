This repository contains code for uploading to a server and creating a system for automatically analyzing feedback using NLP technologies. In the folder `nlp_functions` u can find all the necessary stuff required for text processing. Be advised, that you should additionaly upload the model for text classification (it will start automatically in your machine).
Please be advised, that Yandex.Translate token expired every 24 hours and you should refresh it for translate. Just write Ivan for a new token and put it to nlp_keys file.

Some comments about possible errors:
1. `OSError: Can't load tokenizer for 'cardiffnlp/twitter-roberta-base-sentiment'. If you were trying to load it from 'https://huggingface.co/models
', make sure you don't have a local directory with the same name. Otherwise, make sure 'cardiffnlp/twitter-roberta-base-sentiment' is the correc
t path to a directory containing all relevant files for a RobertaTokenizerFast tokenizer.`

**Solution**:
1) Rename cardiffnlp folder
2) launch the scrypt again
3) delete renamed folder

2. Your system can't find the spacy models

**Solution**:
just type in the comand line:
`python -m spacy download en_core_web_lg`
`python -m spacy download en_core_web_sm`
