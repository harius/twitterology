import dataset


def raw_tweets(table_name):
    return dataset.connect(
        "sqlite:///db/raw_tweets.db"
    ).get_table(
        table_name,
        primary_id="id_str", primary_type="String"
    )
