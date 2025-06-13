from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')
    time = request.args.get('time', 'today 12-m')

    if not keyword:
        return jsonify({'error': 'Keyword parameter is required.'}), 400

    try:
        keywords = [kw.strip() for kw in keyword.split(',')]
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(keywords, cat=0, timeframe=time, geo=geo, gprop='youtube')
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({'message': 'No trend data found.'}), 404

        data = data.drop(labels=['isPartial'], axis='columns')

        return jsonify({
            'keywords': keywords,
            'geo': geo or 'Worldwide',
            'timeframe': time,
            'timeline': data.reset_index().to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
