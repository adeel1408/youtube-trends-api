from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd
import time
import random

app = Flask(__name__)
CORS(app)

# 🔁 Free Proxies (manually added)
PROXIES = [
    'http://138.201.5.62:8080',
    'http://51.158.154.173:3128',
    'http://161.35.70.249:3128',
    # Add more from free-proxy-list.net
]

@app.route('/trends')
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')
    time_range = request.args.get('time', 'today 12-m')

    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    try:
        time.sleep(1.5)  # Delay to avoid 429
        proxy = {'https': random.choice(PROXIES)}

        pytrends = TrendReq(hl='en-US', tz=360, proxies=proxy)
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
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
