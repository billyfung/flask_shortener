from flask import Flask, render_template, send_file, send_from_directory, redirect, url_for
import redis
import urlparse

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def return_shortened():
    url_to_parse = request.form.get('input-url')
    parts = urlparse.urlparse(url_to_parse)
    if not part.scheme in ('http', 'https'):
        error = "Please enter valid url"
    else:
        # with a valid url, shorten it using encode to 62
        parsed = url_shortener.shorten(url_to_parse)
    return render_template('shorten_details.html', 
        link_target=link_target,
        short_id=short_id,
        click_count=click_count)

if __name__ == '__main__':
    app.run()
