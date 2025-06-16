# === File: trends_api.py (Flask Backend with Rate Limiting) ===

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)
CORS(app)

# Initialize rate limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"]  # Change as needed
)

@app.route('/trends')
@limiter.limit("5 per minute; 100 per day")  # Per IP
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
