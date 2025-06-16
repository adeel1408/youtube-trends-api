from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd
import random
import time

app = Flask(__name__)
CORS(app)

# Proxies with authentication
proxy_list = [
    "http://zcvwafez:0d7uu829q8mj@198.23.239.134:6540",
    "http://zcvwafez:0d7uu829q8mj@207.244.217.165:6712",
    "http://zcvwafez:0d7uu829q8mj@107.172.163.27:6543",
    "http://zcvwafez:0d7uu829q8mj@23.94.138.75:6349",
    "http://zcvwafez:0d7uu829q8mj@216.10.27.159:6837",
    "http://zcvwafez:0d7uu829q8mj@136.0.207.84:6661",
    "http://zcvwafez:0d7uu829q8mj@64.64.118.149:6732",
    "http://zcvwafez:0d7uu829q8mj@142.147.128.93:6593",
    "http://zcvwafez:0d7uu829q8mj@104.239.105.125:6655",
    "http://zcvwafez:0d7uu829q8mj@173.0.9.70:5653"
]

@app.route('/trends')
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')  # Default to worldwide
    time_range = request.args.get('time', 'today 12-m')

    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    max_retries = 5
    last_error = ""

    for attempt in range(max_retries):
        selected_proxy = random.choice(proxy_list)
        try:
            pytrends = TrendReq(
                hl='en-US',
                tz=360,
                proxies=[selected_proxy],
                timeout=(5, 10),  # (connect timeout, read timeout)
                retries=2,
                backoff_factor=0.3
            )

            pytrends.build_payload([keyword], cat=0, timeframe=time_range, geo=geo, gprop='youtube')
            df = pytrends.interest_over_time()

            if df.empty:
                return jsonify({'trend_data': []})

            df = df.drop(columns=['isPartial'])
            result = df.reset_index().to_dict(orient='records')
            return jsonify({
                'keyword': keyword,
                'proxy_used': selected_proxy,
                'trend_data': result
            })

        except Exception as e:
            last_error = str(e)
            time.sleep(1)  # Wait before retrying

    return jsonify({'error': f"All proxies failed. Last error: {last_error}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
