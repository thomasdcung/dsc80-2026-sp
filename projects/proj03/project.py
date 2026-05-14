# project.py


import pandas as pd
import numpy as np
from pathlib import Path
import re
import requests
import time


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_book(url):

    crawl_delay = 0.5  # default
    try:
        robots_resp = requests.get('https://www.gutenberg.org/robots.txt', timeout=10)
        for line in robots_resp.text.splitlines():
            stripped = line.strip()
            if stripped.lower().startswith('crawl-delay'):
                parts = stripped.split(':')
                if len(parts) == 2:
                    crawl_delay = float(parts[1].strip())
                    break
    except Exception:
        pass
 
    time.sleep(crawl_delay)
 
    response = requests.get(url, timeout=30)
    text = response.text
 
    text = text.replace('\r\n', '\n')

    start_match = re.search(r'\*{3} START OF .+? \*{3}', text, re.DOTALL)
    end_match   = re.search(r'\*{3} END OF .+? \*{3}',   text, re.DOTALL)
 
    if start_match and end_match:
        text = text[start_match.end() : end_match.start()]
 
    return text





# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def tokenize(book_string):

    START = '\x02'
    STOP  = '\x03'
 
    paragraphs = re.split(r'\n{2,}', book_string)
 
    token_pattern = re.compile(r'[A-Za-z0-9_]+|[^\w\s]|[^\S\n]')
    token_pattern = re.compile(r'\w+|[^\w\s]')
 
    tokens = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        para_tokens = token_pattern.findall(para)
        if not para_tokens:
            continue
        tokens.append(START)
        tokens.extend(para_tokens)
        tokens.append(STOP)
 
    if not tokens:
        tokens = [START, STOP]
 
    return tokens



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


class UniformLM:
 
    def __init__(self, tokens):
        self.mdl = self.train(tokens)
 
    def train(self, tokens):

        unique_tokens = pd.Series(tokens).unique()
        prob = 1.0 / len(unique_tokens)
        return pd.Series(prob, index=unique_tokens)
 
    def probability(self, words):

        prob = 1.0
        for w in words:
            if w not in self.mdl.index:
                return 0
            prob *= self.mdl[w]
        return prob
 
    def sample(self, M):

        tokens = np.random.choice(self.mdl.index, size=M, replace=True,
                                  p=self.mdl.values)
        return ' '.join(tokens)



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


class UnigramLM:
 
    def __init__(self, tokens):
        
        self.mdl = self.train(tokens)
 
    def train(self, tokens):

        s = pd.Series(tokens)
        return s.value_counts(normalize=True)
 
    def probability(self, words):

        prob = 1.0
        for w in words:
            if w not in self.mdl.index:
                return 0
            prob *= self.mdl[w]
        return prob
 
    def sample(self, M):

        tokens = np.random.choice(self.mdl.index, size=M, replace=True,
                                  p=self.mdl.values)
        return ' '.join(tokens)
 



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


class NGramLM(object):
    
    def __init__(self, N, tokens):
        # You don't need to edit the constructor,
        # but you should understand how it works!
        
        self.N = N

        ngrams = self.create_ngrams(tokens)

        self.ngrams = ngrams
        self.mdl = self.train(ngrams)

        if N < 2:
            raise Exception('N must be greater than 1')
        elif N == 2:
            self.prev_mdl = UnigramLM(tokens)
        else:
            self.prev_mdl = NGramLM(N-1, tokens)

    def create_ngrams(self, tokens):
        ...
        
    def train(self, ngrams):
        ...
    
    def probability(self, words):
        ...
    

    def sample(self, M):
        ...
