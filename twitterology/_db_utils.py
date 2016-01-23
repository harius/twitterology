def _prepare_for_db(dictionary, sep, prefix):
    for key, value in dictionary.iteritems():
        full_key = prefix + key
        if isinstance(value, dict):
            for item in _prepare_for_db(value, sep, full_key + sep):
                yield item
        elif not isinstance(value, list):
            yield full_key, value


def prepare_for_db(dictionary, sep="__", prefix=""):
    return dict(_prepare_for_db(dictionary, sep, prefix))
