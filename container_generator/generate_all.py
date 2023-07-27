import subprocess
import argparse
import os
from os import path
from subprocess import PIPE, DEVNULL, STDOUT
from tqdm import tqdm

DIR = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser("Multiple Container Generator")

parser.add_argument("input")
parser.add_argument("output")

args = parser.parse_args()

apks = [f for f in os.listdir(args.input) if path.isfile(f"{args.input}/{f}") and f.endswith(".apk")]

for apk in tqdm(apks):
    subprocess.run(["python", f"{DIR}/generate.py", f"{args.input}/{apk}", "-o", f"{args.output}/{apk}", "-i", f"{DIR}/../VirtualApp"], stdout=DEVNULL, stderr=STDOUT)

