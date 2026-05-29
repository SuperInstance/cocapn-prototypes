# cocapn-prototypes

Experimental prototypes and proof-of-concept demos for the Cocapn Fleet — PLATO Presence Scale backend, interactive HTML demos, and integration experiments.

## What This Gives You

- **PPS Backend** (`pps_backend.py`) — Flask server that collects and aggregates PLATO Presence Scale survey responses
- **Interactive demos** (`plato-presence-scale-demo.html`) — browser-based PLATO Presence Scale UI
- **CI pipeline** — GitHub Actions workflow for Python testing

## Quick Start

```bash
# Run the PPS backend
pip install flask
python pps_backend.py

# Submit a survey response
curl -X POST http://localhost:5000/pps/submit \
  -H "Content-Type: application/json" \
  -d '{"room": "lab", "agent": "test", "score": 4.2, "responses": [1,2,3,4,5]}'

# Get room statistics
curl http://localhost:5000/pps/stats/lab
```

## How It Fits

Prototyping ground for Cocapn Fleet experiments. Part of the SuperInstance ecosystem.

Related repos:
- [cocapn-plato](https://github.com/SuperInstance/cocapn-plato) — PLATO framework
- [cocapn-curriculum](https://github.com/SuperInstance/cocapn-curriculum) — fleet curriculum
- [cocapn-tutor](https://github.com/SuperInstance/cocapn-tutor) — tutoring system

## License

Apache 2.0
