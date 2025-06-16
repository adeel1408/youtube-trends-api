# === File: trends_api.py (Flask Backend) ===

from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/trends')
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')  # Default to worldwide
    time = request.args.get('time', 'today 12-m')

    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
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
