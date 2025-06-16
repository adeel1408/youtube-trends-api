# === File: trends_api.py (Flask Backend with Unlimited Requests + Proxy Rotation) ===

from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd
import random

app = Flask(__name__)
CORS(app)

# Proxies with authentication (username:password@ip:port)
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
    time = request.args.get('time', 'today 12-m')

    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    try:
        # Randomly select a proxy for each request
        selected_proxy = random.choice(proxy_list)
        pytrends = TrendReq(hl='en-US', tz=360, proxies=[selected_proxy])

        pytrends.build_payload([keyword], cat=0, timeframe=time, geo=geo, gprop='youtube')
        df = pytrends.interest_over_time()

        if df.empty:
            return jsonify({'trend_data': []})

        df = df.drop(columns=['isPartial'])
        result = df.reset_index().to_dict(orient='records')
        return jsonify({
            'keyword': keyword,
            'trend_data': result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
