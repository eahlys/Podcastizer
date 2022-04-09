from flask import Flask, abort, Response

import config
import podcast_utils

app = Flask(__name__)


@app.route('/<id>')
def get_podcast(id):
    if id in config.PODCASTS_MERGE:
        podcast = config.PODCASTS_MERGE[id]
        all_ep = podcast_utils.get_all_episodes_from_feed_list(podcast['sources'], podcast['ignore_title'])
        xml = podcast_utils.gen_podcast_xml(
            title=podcast['title'],
            description=podcast['description'],
            website=podcast['website'],
            image=podcast['image'],
            episodes=all_ep
        )
        return Response(xml, content_type='text/xml')
    else:
        abort(404)


app.run(host='127.0.0.1', port=5555)
