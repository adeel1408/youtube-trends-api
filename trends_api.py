from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd
import time
import random

app = Flask(__name__)
CORS(app)

# ✅ Full Proxy List (free)
PROXIES = [
    'http://93.190.138.107:46182',   # NL
    'http://57.129.81.201:8080',     # DE
    'http://159.69.57.20:8880',      # DE
    'http://8.219.97.248:80',        # SG
    'http://4.149.210.210:3128',     # US
    'http://34.48.171.130:33080',    # US
    'http://70.36.101.234:60014',    # US
    'http://47.251.43.115:33333'     # US
]

@app.route('/trends')
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')  # e.g., 'US'
    time_range = request.args.get('time', 'today 12-m')  # e.g., 'today 12-m', 'now 1-d'

    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    for attempt in range(len(PROXIES)):
        proxy = {'https': PROXIES[attempt]}
        try:
            print(f"🔁 Trying proxy {attempt+1}/{len(PROXIES)}: {proxy['https']}")
            time.sleep(1.5)  # To avoid being blocked

            pytrends = TrendReq(hl='en-US', tz=360, proxies=proxy)
            pytrends.build_payload([keyword], cat=0, timeframe=time_range, geo=geo, gprop='youtube')
            df = pytrends.interest_over_time()

            if df.empty:
                continue

            df = df.drop(columns=['isPartial'], errors='ignore')
            result = df.reset_index().to_dict(orient='records')
            return jsonify({
                'keyword': keyword,
                'trend_data': result,
                'proxy_used': proxy['https']
            })

        except Exception as e:
            print(f"❌ Proxy failed: {proxy['https']} | Error: {e}")
            continue

    return jsonify({'error': 'All proxies failed. Try again later or update proxy list.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
