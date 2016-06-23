#!/usr/bin/env python
# coding: utf-8
# Usage: examples/logistic_regression examples.db:track_hello
from sys import argv
from itertools import groupby, islice, izip
from operator import itemgetter
from random import Random

import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

import twitterology as tw
import twitterology.features as tf
from model import MODEL

import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import cross_val_score, StratifiedKFold

from tqdm import tqdm


def make_samples(samples_a, samples_b, samples_f, ratio):
    samples = []
    pairs = []

    for (user_a, timeline_a), (user_b, timeline_b) in izip(samples_a, samples_b):
        assert user_a == user_b
        samples.append(MODEL.difference(timeline_a, timeline_b))
        pairs.append([user_a, user_b])

    random = Random(42)
    more_pairs = int(ratio * len(samples))

    for _ in range(more_pairs):
        user_a, timeline_a = random.choice(samples_f)
        user_b, timeline_b = random.choice(samples_f)

        samples.append(MODEL.difference(timeline_a, timeline_b))
        pairs.append([user_a, user_b])

    samples = np.array(samples)
    pairs = np.array(pairs)

    return samples, pairs


def make_full_samples(samples_f, count):
    random = Random(43)
    samples_f = np.array(random.sample(samples_f, count))

    samples = []
    pairs = []

    for user_a, timeline_a in samples_f:
        for user_b, timeline_b in samples_f:
            if user_a == user_b:
                continue

            samples.append(MODEL.difference(timeline_a, timeline_b))
            pairs.append([user_a, user_b])

    samples = np.array(samples)
    pairs = np.array(pairs)

    return samples, pairs


def cross_val_predict_proba(clf, samples, targets, cv):
    proba = -np.ones_like(targets, dtype="float")

    for train_idx, test_idx in tqdm(cv):
        train_samples, train_targets = samples[train_idx], targets[train_idx]
        test_samples, test_targets = samples[test_idx], targets[test_idx]

        clf.fit(train_samples, train_targets)

        test_proba = clf.predict_proba(test_samples)
        proba[test_idx] = test_proba[:, 1]

    return proba


def plot_features(samples, targets, table):
    rows = (len(MODEL.features.labels) + 1) / 2

    fig, axs = plt.subplots(rows, 2, figsize=(7, rows * 1.8))
    fig.subplots_adjust(hspace=0.5, wspace=0.3)

    lines = {}
    axs = iter(axs.ravel())
    for index, (distribution, label, ax) in enumerate(zip(samples.T, MODEL.features.labels, axs), start=1):
        for target in [False, True]:
            mask = (targets == target).astype(int)
            density, edges = np.histogram(distribution, weights=mask, bins=23, density=True)

            lines[int(target)], = ax.plot(
                np.repeat(edges, 2)[1:-1], np.repeat(density, 2), ":" if target else "-", label=str(target)
            )

        ax.tick_params(labelsize="x-small")
        ax.yaxis.set_visible(False)
        ax.set_ylim([-0.1 * max(density), 1.1 * max(density)])
        title = ax.set_title(label.decode("utf-8"))
        title.set_family("serif")
        title.set_size("small")

    for ax in axs:
        ax.axis("off")

    plt.figlegend(lines.values(), lines.keys(), 'lower right', title=u'Класс')
    plt.savefig("plots/{}/features".format(table))


def main():
    database, table = argv[1].split(":")

    samples_a = np.load("db/{}/samples_a.npy".format(table))
    samples_b = np.load("db/{}/samples_b.npy".format(table))
    samples_f = np.load("db/{}/samples_f.npy".format(table))

    samples, pairs = make_samples(samples_a, samples_b, samples_f, 10.0)
    targets = (pairs[:, 0] == pairs[:, 1])

    splitter = StratifiedKFold(
        targets, n_folds=10,
        random_state=123, shuffle=True
    )
    clf = LogisticRegression()

    proba = cross_val_predict_proba(
        clf, samples, targets,
        cv=splitter
    )

    false_positives, true_positives, _ = roc_curve(targets, proba)
    roc_auc = auc(false_positives, true_positives)

    plt.figure(figsize=(7, 7))
    plt.plot(false_positives, true_positives, label="AUC: {:.5f}".format(roc_auc),
             linewidth=2.0)
    plt.legend(loc="lower right")
    plt.grid()
    plt.savefig("plots/{}/roc".format(table))

    np.save("db/{}/coef.npy".format(table), clf.coef_[0])

    plot_features(samples, targets, table)

    full_samples, full_pairs = make_full_samples(samples_f, 400)
    full_proba = clf.predict_proba(full_samples)[:, 1].astype("string")
    estimates = np.append(full_pairs, full_proba.reshape(len(full_proba), 1), axis=1)
    np.save("db/{}/estimates.npy".format(table), estimates)


if __name__ == "__main__":
    main()
