from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')  # Default to worldwide if not provided
    time = request.args.get('time', 'today 12-m')  # Default to past 12 months

    if not keyword:
        return jsonify({'error': 'Keyword parameter is required.'}), 400

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe=time, geo=geo, gprop='youtube')
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({'message': f"No trend data found for keyword '{keyword}', region '{geo}', and time '{time}'."}), 404

        data = data.drop(labels=['isPartial'], axis='columns')

        # Format response
        result = {
            'keyword': keyword,
            'geo': geo or 'Worldwide',
            'timeframe': time,
            'trend_data': data.reset_index().to_dict(orient='records')
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
