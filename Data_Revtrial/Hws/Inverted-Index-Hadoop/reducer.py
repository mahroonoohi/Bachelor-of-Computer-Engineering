#!/usr/bin/env python

from sys import stdin
import re

index = {}

for line in stdin:

        word_postings= line.split()
        word=word_postings[0]
        postings=word_postings[1:]
        
        if not word in index:
              index[word] = set()
        
        index[word].update(postings)
        

for word in index:
    s = [word]
    postings = list(index[word])
    print(word, ' '.join(sorted(postings)))
        
