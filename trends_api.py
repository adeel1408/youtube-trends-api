from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import os
import random

app = Flask(__name__)

# List of user-agent headers to rotate
AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64)",
    "Mozilla/5.0 (Linux; Android 10)"
]

def get_trends(keyword, geo, time_range):
    try:
        user_agent = random.choice(AGENTS)
        pytrends = TrendReq(
            hl='en-US',
            tz=360,
            requests_args={'headers': {'User-Agent': user_agent}}
        )

        pytrends.build_payload([keyword], geo=geo, timeframe=time_range)
        data = pytrends.interest_over_time()

        if data.empty:
            return {"error": "No trend data found."}, 404

        # Clean data
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
