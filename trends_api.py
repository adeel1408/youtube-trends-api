from flask import Flask, request, jsonify
from pytrends.request import TrendReq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_trends', methods=['GET'])
def get_trends():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')
    timeframe = request.args.get('timeframe', 'now 1-H')

    if not keyword:
        return jsonify({"error": "Missing keyword"}), 400

    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='youtube')
    data = pytrends.interest_over_time()

    if data.empty:
        return jsonify({"error": "No trend data found"}), 404

    trend_data = data[keyword].reset_index().rename(columns={"date": "timestamp", keyword: "value"})
    result = trend_data.to_dict(orient='records')

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
