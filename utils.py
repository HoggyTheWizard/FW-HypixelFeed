import feedparser

thread_ids = []

def get_list(id_list):
    if len(id_list) > 100:
        del thread_ids[:2]
        return thread_ids
    else:
        return id_list

def feed():
    while True:
        raw_feed = feedparser.parse("https://hypixel.net/forums/-/index.rss")
        filtered_feed = []
        for entry in raw_feed.entries:
            if entry["id"] not in thread_ids and int(entry["slash_comments"]) == 0:
                filtered_feed.append(entry)
                print()
        return [filtered_feed, get_list(thread_ids)]
