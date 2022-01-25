import os
from pydoc import pager
import random
import re
import sys
from tkinter import N
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    prob_dict = {}

    # adding 0 probabilities to prob_dict
    for key in corpus:
        prob_dict[key] = 0
    
    # adding initial random value to dict
    for key in prob_dict:
        prob_dict[key] = (1-damping_factor) * (1/len(prob_dict))

    pages_connected_to_page = corpus[page]
    for i in pages_connected_to_page:
        if i in prob_dict:
            prob_dict[i] += (1/len(pages_connected_to_page)) * damping_factor
    
    #normalizing
    summ=0
    for i in prob_dict:
        summ += prob_dict[i]
    for i in prob_dict:
        prob_dict[i] = prob_dict[i] / summ

    return prob_dict


    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    
    # initialising pagerank
    for key in corpus:
        pagerank[key] = 0
    
    mypage = random.choice(list(pagerank.keys()))
    
    for i in range(n):
        pagerank[mypage] +=1
        print("pagerank:", pagerank)
        mymodel = transition_model(corpus,mypage,damping_factor)
        print("corpus:",corpus)
        print("mymodel",mymodel)
        mypage = random.choices(list(mymodel.keys()),list(mymodel.values()))[0]
        print("mypage:", mypage)
        
        # input()
    
    
    
    for i in pagerank:
        pagerank[i] = pagerank[i]/n

    return pagerank
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank={}
    n = len(corpus)
    for page in corpus:
        pagerank[page] = 1/n

    while True:
        old_pagerank = pagerank
        
        for page in pagerank:
            summ = 0
            for i in pages_that_link_to_page(page,corpus):
                summ += pagerank[i]/len(corpus[i])

            pagerank[page] = ((1-damping_factor)/n) + (damping_factor*summ)

        diff_array = np.array(list(pagerank.values())) - np.array(list(old_pagerank.values()))
        
        for diff in diff_array:
            if diff < 0.001:
                return pagerank
    
        

    raise NotImplementedError

def pages_that_link_to_page(p,corpus):
    pages=[]
    for page in corpus:
        for links in corpus[page]:
            if p in links:
                pages.append(page)
    return pages




if __name__ == "__main__":
    main()
