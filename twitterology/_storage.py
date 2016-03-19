def _dump_for_storage(dictionary, sep, prefix):
    for key, value in dictionary.iteritems():
        full_key = prefix + key
        if isinstance(value, dict):
            for item in _dump_for_storage(value, sep, full_key + sep):
                yield item
        elif not isinstance(value, list):
            yield full_key, value


def dump_for_storage(dictionary, sep="__", prefix=""):
    return dict(_dump_for_storage(dictionary, sep, prefix))
