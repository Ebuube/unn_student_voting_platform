"""
How to parse csv using sample

>> python ./test_csv.py
"""
from pprint import pprint
from utils.csv_parser import parse_csv

with open("sample_registry_upload.csv", "r") as file:
    content = file.read()

result = parse_csv(content)

pprint(result)
