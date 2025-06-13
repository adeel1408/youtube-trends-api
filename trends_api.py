from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')  # Default to worldwide
    time = request.args.get('time', 'today 12-m')  # Default to 12 months

    if not keyword:
        return jsonify({'error': 'Keyword parameter is required.'}), 400

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe=time, geo=geo, gprop='youtube')
        df = pytrends.interest_over_time()

        if df.empty:
            return jsonify({'message': 'No trend data found.', 'timeline': []})

        df = df.reset_index().drop(columns=['isPartial'])

        return jsonify({
            'keyword': keyword,
            'geo': geo or 'Worldwide',
            'timeframe': time,
            'timeline': df.to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
