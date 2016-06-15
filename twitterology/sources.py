from datetime import datetime

import dataset


def sqlite(database, table, metadata=None):
    db = dataset.connect("sqlite:///db/" + database)

    if metadata is not None:
        metatable = db.get_table("_metadata")
        metatable.insert(dict(metadata, table=table))

    return db.get_table(table, primary_id="id_str", primary_type="String")
