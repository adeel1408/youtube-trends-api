from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import os

app = Flask(__name__)

# Optional: Load proxy list from a file or environment
PROXIES = [
    # Add working proxies here if needed
    # Example: "http://123.123.123.123:8080"
]

def get_trends(keyword, geo, time_range):
    try:
        # If proxies exist, pass them; else omit the parameter
        if PROXIES:
            pytrends = TrendReq(hl='en-US', tz=360, proxies={'https': PROXIES[0]})
        else:
            pytrends = TrendReq(hl='en-US', tz=360)

        pytrends.build_payload([keyword], geo=geo, timeframe=time_range)
        data = pytrends.interest_over_time()

        if data.empty:
            return {"error": "No trend data found."}, 404

        # Remove 'isPartial' column
        data = data.reset_index()[['date', keyword]]
        result = [{"date": row['date'].isoformat(), "value": row[keyword]} for _, row in data.iterrows()]
        return {"keyword": keyword, "data": result}

    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/trends', methods=['GET'])
def trends_endpoint():
    keyword = request.args.get('keyword')
    geo = request.args.get('geo', '')
    time_range = request.args.get('time', 'today 3-m')

    if not keyword:
        return jsonify({"error": "Missing keyword parameter"}), 400

    return jsonify(get_trends(keyword, geo, time_range))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
