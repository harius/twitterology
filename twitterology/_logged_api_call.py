from contextlib import contextmanager
from datetime import datetime
from operator import attrgetter


@contextmanager
def logged_api_call(client, api, log_file="./log/api_calls.txt", **kwargs):
    get_api = attrgetter(api)
    opened_log = open(log_file, "a")

    def write_to_log(header):
        opened_log.write("{}\t{}\t{}\t{}\n".format(
            datetime.now().isoformat(), header, api, kwargs
        ))

    write_to_log("start")
    try:
        yield get_api(client).post(**kwargs)
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        write_to_log(type(e).__name__)
    write_to_log("end")
