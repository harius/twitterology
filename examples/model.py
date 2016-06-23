#!/usr/bin/env python
import twitterology.features as tf


def model(sampling):
    return tf.ProductDifference(
        tf.AbsoluteDifference(
            tf.Product(
                tf.Median(tf.Length()),
                tf.Average(tf.Count(tf.NeutralPunctuation())),
                tf.Average(tf.IsRetweet()),
                tf.Average(tf.Count(tf.Hashtags())),
                tf.Average(tf.Count(tf.Mentions())),
                tf.Average(tf.IncludesLink()),
                tf.Median(tf.Time()),

                tf.AverageInterval(sampling=sampling),
                tf.Diversity()
            )
        ),
        tf.JaccardDifference(
            tf.Product(
                # tf.Counts(tf.Hashtags(), top=4),
                tf.Counts(tf.Mentions(), top=2),
                tf.Counts(tf.Words(), top=8)
            )
        )
    )


MODEL = model(0.5)
FULL_MODEL = model(1.0)
