#python3 langrank_predict.py -o sample-data/ted-train.orig.aze -s sample-data/ted-train.orig.spm8000.aze -l aze -n 3 -t MT
#python langrank_predict.py -o datasets/olid/dan.txt -l dan -n 3 -t OLID
import langrank as lr
import os
import argparse


parser = argparse.ArgumentParser(description='Langrank parser.')
parser.add_argument('-o', '--orig', type=str, required=True, help='unsegmented dataset')
parser.add_argument('-s', '--seg', type=str, help='segmented dataset')
parser.add_argument('-l', '--lang', type=str, required=True, help='language code')
parser.add_argument('-n', '--num', type=int, default=3, help='print top N')
parser.add_argument('-c', '--candidates', type=str, default="all",
                    help="candidates of transfer languages, seperated by ;, use *abc to exclude language abc")
parser.add_argument('-t', '--task', type=str, default="MT", choices=["MT", "POS", "EL", "DEP", "OLID", "SA"],
                    help="The task of interested. Current options support 'MT': machine translation,"
                    "'DEP': Dependency Parsing, 'POS': POS-tagging, 'EL': Entity Linking,"
                    "'OLID': Offensive Language Identification, and 'SA': Sentiment Analysis.")
parser.add_argument('-m', '--model', type=str, default="best", help="model to be used for prediction")

params = parser.parse_args()

assert os.path.isfile(params.orig)
assert (params.seg is None or os.path.isfile(params.seg))

with open(params.orig) as inp:
    lines = inp.readlines()

bpelines = None
if params.seg is not None:
    with open(params.seg) as inp:
        bpelines = inp.readlines()

print("read lines")
prepared = lr.prepare_new_dataset(params.lang, dataset_source=lines, dataset_subword_source=bpelines)
print("prepared")
candidates = "all" if params.candidates == "all" else params.candidates.split(";")
task = params.task
lr.rank(prepared, task=task, candidates=candidates, print_topK=params.num, model=params.model)
print("ranked")

