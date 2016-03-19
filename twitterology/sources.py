from datetime import datetime

import dataset


def tweets(track, session=None):
    if session is None:
        session = "{:%Y%m%d-%H%M%S}".format(datetime.now())
    name = "track__{}__{}".format(track, session)

    database = dataset.connect("sqlite:///db/tweets.db")
    return database.get_table(name, primary_id="id_str", primary_type="String")
