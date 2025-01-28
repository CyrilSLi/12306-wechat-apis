# 64x32rgb

A China Railway (HSR and traditional) train tracker using a 64x32 RGB LED matrix.

It currently displays the start, current, and end stations, the company and if it’s a regularly scheduled service, and a line diagram, but the APIs I use have much more data, e.g. the max occupancy of each car, and whether stations have luggage storage.

Requests to 12306 APIs are cached to minimize the chances of being banned for request frequency

## Usage (on computer via PyGame emulation)

1. Clone the repository and `cd` into it

```
cd Projects/64x32rgb
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python main.py
```
