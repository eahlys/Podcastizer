from datetime import datetime, timedelta

import feedparser
from podgen import Podcast, Episode, Media
from config import PODCASTS_MERGE


def parse_podcast_episodes(feed_url, prepend_str, ignore_title):
    fp = feedparser.parse(feed_url)
    episodes = []
    for item in fp.entries:
        data = {
            'title': str(prepend_str) + ' - ' + item['title'],
            'id': item['id'],
            'media': item['links'][1]['href'],
            'size': item['links'][1]['length'],
            'summary': item['summary'],
            'published': item['published'],
            'duration': item['itunes_duration']
        }

        if item['title'] != ignore_title:
            episodes.append(data)

    return episodes


def get_all_episodes_from_feed_list(feeds, ignore_title):
    all_episodes = []
    for feed in feeds.items():
        episodes = parse_podcast_episodes(feed[1], feed[0], ignore_title)
        all_episodes += episodes

    return all_episodes


def gen_podcast_xml(title, description, website, image, episodes):
    p = Podcast(
        name=title,
        description=description,
        website=website,
        image=image,
        explicit=False
    )

    for episode in episodes:
        duration_time = datetime.strptime(episode['duration'], "%H:%M:%S")
        p.episodes += [
            Episode(
                title=episode['title'],
                id=episode['id'],
                media=Media(episode['media'], episode['size'], duration=timedelta(hours=duration_time.hour, minutes=duration_time.minute, seconds=duration_time.second)),
                summary=episode['summary'],
                publication_date=episode['published']
            )
        ]

    return p.rss_str()

# parse_podcast_episodes(URL2, prepend_str='Guiz', ignore_title=IGNORE_TITLE)
# episodes = get_all_episodes_from_feed_list(PODCASTS_MERGE['inter']['Sources'], PODCASTS_MERGE['inter']['Ignore_title'])

# xml = gen_podcast_xml(
#     title=PODCASTS_MERGE['inter']['Title'],
#     description=PODCASTS_MERGE['inter']['Description'],
#     website=PODCASTS_MERGE['inter']['Website'],
#     image=PODCASTS_MERGE['inter']['Image'],
#     episodes=episodes
# )
#
# print(xml)