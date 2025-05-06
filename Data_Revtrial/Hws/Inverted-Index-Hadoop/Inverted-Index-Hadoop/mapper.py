#!/usr/bin/env python

from sys import stdin
import re
import os

for line in stdin:
        doc_id = os.environ.get("map_input_file","tedt_id")
        doc_id = doc_id.split('/')[-1]
        words = re.findall(r'\w+', line.strip())
        for word in words:
                print("%s %s" % (word.lower(), doc_id))
