from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd
import time

app = Flask(__name__)
CORS(app)

@app.route('/trends')
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')  # Default to worldwide
    time_range = request.args.get('time', 'today 12-m')

    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    try:
        time.sleep(1.5)  # Delay to prevent Google rate limit

        pytrends = TrendReq(hl='en-US', tz=360)
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
        print("Error:", e)  # Visible in Render logs
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
