from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# In production, this would use PLATO's actual storage
SURVEY_DB = "/tmp/pps_responses.jsonl"

@app.route('/pps/submit', methods=['POST'])
def submit_pps():
    """Receive PLATO Presence Scale responses."""
    data = request.json
    
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "room": data.get("room", "unknown"),
        "agent": data.get("agent", "unknown"),
        "score": data.get("score"),
        "responses": data.get("responses"),
        "session_duration_sec": data.get("session_duration_sec"),
        "tile_count": data.get("tile_count")
    }
    
    # Append to log
    with open(SURVEY_DB, "a") as f:
        f.write(json.dumps(record) + "\n")
    
    return jsonify({"status": "recorded", "score": record["score"]})

@app.route('/pps/stats/<room>', methods=['GET'])
def room_stats(room):
    """Get PPS statistics for a room."""
    if not os.path.exists(SURVEY_DB):
        return jsonify({"error": "no data"}), 404
    
    scores = []
    with open(SURVEY_DB) as f:
        for line in f:
            r = json.loads(line)
            if r["room"] == room:
                scores.append(r["score"])
    
    if not scores:
        return jsonify({"error": "no data for room"}), 404
    
    import statistics
    return jsonify({
        "room": room,
        "n": len(scores),
        "mean": round(statistics.mean(scores), 2),
        "median": round(statistics.median(scores), 2),
        "stdev": round(statistics.stdev(scores), 2) if len(scores) > 1 else 0,
        "min": min(scores),
        "max": max(scores)
    })

@app.route('/pps/bpi/<room>', methods=['GET'])
def compute_bpi(room):
    """Compute Behavioral Presence Index from session logs."""
    # In production, this queries PLATO's actual session logs
    # For demo, return mock calculation formula
    
    return jsonify({
        "room": room,
        "formula": "BPI = 0.3*dwell + 0.2*return + 0.2*scroll + 0.15*(1/latency) + 0.15*cross_ref",
        "components": {
            "dwell_time_norm": "seconds in room / 300",
            "return_rate": "sessions per day / 10",
            "scroll_depth": "% tiles viewed / 100",
            "latency_inv": "1 / (response_seconds + 1)",
            "cross_ref_rate": "links clicked between tiles / total_tiles"
        },
        "note": "Connect to PLATO session log API for live computation"
    })

if __name__ == "__main__":
    app.run(port=8902, debug=True)
