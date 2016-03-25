from datetime import datetime

import dataset


def tweets(track=None, locations=None, session=None):
    database = dataset.connect("sqlite:///db/tweets.db")
    if track is None and locations is None:
        return [table.split("__") for table in database.tables
                if table.startswith("track") or table.startswith("locations")]

    if track is not None and locations is not None:
        raise ValueError("Cannot filter both track and location")

    if session is None:
        session = "{:%Y%m%d-%H%M%S}".format(datetime.now())

    if track is not None:
        name = "track__{}__{}".format(track, session)
    elif locations is not None:
        name = "locations__{}__{}".format(locations, session)

    return database.get_table(name, primary_id="id_str", primary_type="String")


def timelines(source, session=None):
    database = dataset.connect("sqlite:///db/timelines.db")

    if session is None:
        session = "{:%Y%m%d-%H%M%S}".format(datetime.now())
    name = source + "__" + session

    return database.get_table(name, primary_id="id_str", primary_type="String")
