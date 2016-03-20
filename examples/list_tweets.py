import twitterology as tw


if __name__ == "__main__":
    storage = tw.sources.tweets()

    tables = []
    for table in storage:
        _, track, session = table.split("__")
        tables.append((session, track))

    for session, track in sorted(tables):
        print "{:>16} {}".format(track, session)
