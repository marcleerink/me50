import os
import random
import re
import sys

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
    print("PageRank Results from Iteration")
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
    prob_dist = dict()
    number_of_pages = len(corpus)


    for p in corpus:

        rank = (1 - damping_factor) / number_of_pages

        # If page has no links
        # add equal probability to all pages with damping factor
        if len(corpus[page]) == 0:
            prob_dist[p] = rank
            continue

        if p in corpus[page]:
            rank += damping_factor / len(corpus[page])

        prob_dist[p] = rank

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = dict()
    for p in corpus:
        page_rank[p] = 0

    # random page to start with
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        # update page rank for the current page
        page_rank[current_page] += 1 / n

        # get the probability distribution for the next page
        prob_dist = transition_model(corpus, current_page, damping_factor)

        # choose next page based on the probability distribution
        next_page = random.choices(
            list(prob_dist.keys()),
            weights=list(prob_dist.values()),
        )[0]

        current_page = next_page
    # print(sum(page_rank.values()))
    return page_rank


def update_page_ranks(
    corpus,
    page_rank,
    prev_page_rank,
    damping_factor,
    n,
):
    for page in corpus:
        if len(corpus[page]) == 0:
            corpus[page] = set(corpus.keys())
            print(f"Page {page} has no links. Adding links to all pages in corpus.")

        new_rank = (1 - damping_factor) / n
        for incoming_page, links in corpus.items():
            # if the incoming page has a link to the current page
            # then add the incoming page's rank divided by the number of links
            # to the current page
            if page in links:
                new_rank += damping_factor * prev_page_rank[incoming_page] / len(links)
        page_rank[page] = new_rank
    return page_rank


def calculate_accuracy(page_rank, prev_page_rank):
    accuracy = 0
    for p in page_rank:
        accuracy += abs(page_rank[p] - prev_page_rank[p])
    return accuracy


def update_previous_page_ranks(corpus, page_rank, prev_page_rank):
    for p in corpus:
        prev_page_rank[p] = page_rank[p]
    return prev_page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    accuracy = 1
    desired_accuracy = 0.001
    n = len(corpus)

    # set current page rank to 1 / n
    page_rank = dict()
    for p in corpus:
        page_rank[p] = 1 / n

    # set previous page rank to 0
    prev_page_rank = dict()
    for p in corpus:
        prev_page_rank[p] = 0

    # iterate until desired accuracy is reached
    while accuracy > desired_accuracy:
        page_rank = update_page_ranks(
            corpus, page_rank, prev_page_rank, damping_factor, n
        )
        accuracy = calculate_accuracy(page_rank, prev_page_rank)
        prev_page_rank = update_previous_page_ranks(corpus, page_rank, prev_page_rank)
    # print(sum(page_rank.values()))
    return page_rank


if __name__ == "__main__":
    main()
