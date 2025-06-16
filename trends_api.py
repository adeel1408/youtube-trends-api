from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd
import time
import random

app = Flask(__name__)
CORS(app)

# ✅ Free Proxies (http/https supported)
PROXIES = [
    'http://93.190.138.107:46182',
    'http://57.129.81.201:8080',
    'http://51.81.245.3:17981',
    'http://161.35.98.111:8080',
    'http://200.174.198.86:8888',
    'http://188.245.239.104:4001',
    'http://5.161.143.206:1080',
    'http://136.52.10.221:8888',
    'http://123.26.132.171:8080',
    'http://159.69.57.20:8880',
    'http://8.219.97.248:80',
    'http://4.149.210.210:3128',
    'http://34.48.171.130:33080',
    'http://70.36.101.234:60014',
    'http://115.79.70.69:8470',
    'http://47.251.43.115:33333'
]

@app.route('/trends')
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')
    time_range = request.args.get('time', 'today 12-m')

    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    try:
        time.sleep(1.5)  # Delay to reduce 429 errors
        proxy = random.choice(PROXIES)

        # ✅ Set both http and https proxies
        pytrends = TrendReq(
            hl='en-US',
            tz=360,
            proxies={
                'http': proxy,
                'https': proxy
            }
        )

        pytrends.build_payload([keyword], cat=0, timeframe=time_range, geo=geo, gprop='youtube')
        df = pytrends.interest_over_time()

        if df.empty:
            return jsonify({'trend_data': [], 'message': 'No trend data found.'})

        df = df.drop(columns=['isPartial'])
        result = df.reset_index().to_dict(orient='records')

        return jsonify({
            'keyword': keyword,
            'trend_data': result
        })

    except Exception as e:
        print("❌ API Error:", e)
        return jsonify({'error': f'API Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
