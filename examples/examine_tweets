#!/usr/bin/env python
# Usage: examples/logistic_regression examples.db:track_hello
from sys import argv
from itertools import groupby, islice
from operator import itemgetter
from random import Random

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

import tabulate

import twitterology as tw
import twitterology.features as tf
from model import MODEL

import numpy as np
np.set_printoptions(precision=2, suppress=True)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import cross_val_score, StratifiedKFold

from tqdm import tqdm


def link_to(user_id):
    return "https://twitter.com/intent/user?user_id=" + user_id


def format_sample(sample):
    return "  ".join(
        "{:.2f}".format(x) if isinstance(x, float)
        else repr(x).decode("unicode-escape").encode("utf-8")
        for x in sample
    )


def main():
    database, table = argv[1].split(":")

    samples_a = dict(np.load("db/{}/samples_a.npy".format(table)))
    samples_b = dict(np.load("db/{}/samples_b.npy".format(table)))

    estimates = np.load("db/{}/estimates.npy".format(table))
    coef = np.load("db/{}/coef.npy".format(table))

    seen = set()

    total = 0
    count = 0
    for user_a, user_b, proba in estimates:
        proba = float(proba)
        total += 1
        if proba > 0.95 and user_a != user_b and (user_a not in seen or user_b not in seen):
            count += 1

            print "\n===", count, proba, "===\n"
            print link_to(user_a)
            """
            print format_sample(samples_a[user_a])
            print
            """
            print link_to(user_b)
            """
            print format_sample(samples_b[user_b])
            print
            print MODEL.difference(samples_a[user_a], samples_b[user_b]) * coef
            """
            seen.add(user_a)
            seen.add(user_b)
            seen = set()
    print "flagged:", count, "/", total
    print "seen:", len(seen)

    tab = tabulate.tabulate([(f.decode("utf-8"), "{:.2f}".format(c)) for f, c in zip(MODEL.features.labels, coef)],
                            tablefmt="latex")
    with open("plots/{}/tab.tex".format(table), "w") as tabfile:
        tabfile.write(tab.encode("utf-8"))


if __name__ == "__main__":
    main()
