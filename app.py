from flask import Flask, render_template, send_file, send_from_directory, redirect, url_for, request
import redis
import urlparse
import string
import os
from werkzeug.exceptions import HTTPException, NotFound
from math import floor

app = Flask(__name__)
app.debug = True

redis = redis.Redis()

def shorten(url):
        short_id = redis.get('reverse-url:' + url)
        if short_id is not None:
            return short_id
        url_num = redis.incr('last-url-id')
        short_id = b62_encode(url_num)
        redis.set('url-target:' + short_id, url)
        redis.set('reverse-url:' + url, short_id)
        return short_id

def b62_encode(number):
    base = string.digits + string.lowercase + string.uppercase
    assert number >= 0, 'positive integer required'
    if number == 0:
        return '0'
    base62 = []
    while number != 0:
        number, i = divmod(number, 62)
        base62.append(base[i])
    return ''.join(reversed(base62))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def return_shortened():
    url_to_parse = request.form['input-url']
    parts = urlparse.urlparse(url_to_parse)
    if not parts.scheme in ('http', 'https'):
        error = "Please enter valid url"
    else:
        # with a valid url, shorten it using encode to 62
        short_id = shorten(url_to_parse)
    return render_template('result.html', short_id=short_id)

@app.route("/<short_id>")
def expand_to_long_url(short_id):
    link_target = redis.get('url-target:' + short_id)
    if link_target is None:
        raise NotFound()
    redis.incr('click-count:' + short_id)
    return redirect(link_target)

@app.route("/<short_id>+")
def shorten_details(short_id):
    link_target = redis.get('url-target:' + short_id)
    if link_target is None:
        raise NotFound()
    click_count = int(redis.get('click-count:' + short_id) or 0)
    return render_template('details.html', 
                        short_id=short_id, 
                        click_count=click_count,
                        link_target=link_target)

if __name__ == '__main__':
    app.run()
