from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq

app = Flask(__name__)
CORS(app)

pytrends = TrendReq(hl='en-US', tz=360)

@app.route("/")
def root():
    return jsonify({"message": "YouTube Trends API is working."})

@app.route("/trends", methods=["GET"])
def get_trends():
    keyword = request.args.get("keyword")
    geo = request.args.get("geo", "")
    time = request.args.get("time", "now 1-H")

    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    pytrends.build_payload([keyword], cat=0, timeframe=time, geo=geo, gprop='youtube')
    data = pytrends.interest_over_time()

    if data.empty:
        return jsonify({"message": "No trends data found"}), 404

    data = data.reset_index()[['date', keyword]]
    return jsonify(data.to_dict(orient='records'))
