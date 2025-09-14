from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
CORS(app)

COMPONENTS = []
CONTEXT = ""
BUILD_STATE = {
  "status": "idle",
  "components": {
    "stm32f103": {
      "name": "STM32",
      "description": "Primary microcontroller unit (MCU) for processing and control.",
      "img": "/component.jpg",
      "submodules": {
        "220uF_capacitor": {
          "name": "220uF Capacitor",
          "description": "Stabilizes power supply to the MCU.",
          "img": "/component.jpg",
        },
        "10k_resistor": {
          "name": "10k Resistor",
          "description": "Pull-up resistor for reset pin.",
          "img": "/component.jpg",
        }
      }
    },
    "drv8825": {
      "name": "DRV8825",
      "description": "Step motor driver for controlling stepper motors.",
      "img": "/component.jpg",
      "submodules": {
        "100uF_capacitor": {
          "name": "100uF Capacitor",
          "description": "Filters voltage spikes from motor operation.",
          "img": "/component.jpg",
        },
        "1k_resistor": {
          "name": "1k Resistor",
          "description": "Current limiting resistor for stepper motor coils.",
          "img": "/component.jpg",
        }
      }
    },
    "graphnode1": {
      "name": "Subcircuit",
      "description": "Hierarchical node containing its own graph.",
      "img": "/component.jpg",
      "subgraph": {
        "subA": ["subB", "subC"],
        "subB": ["subC"],
        "subC": []
      }
    }
  },
  "adjGraph": {
    "stm32f103": ["drv8825"],
    "r1": ["stm32f103"],
    "r2": ["stm32f103"],
    "r3": ["stm32f103"],
    "r4": ["stm32f103"],
    "drv8825": ["c1","c2","r5"],
    "c1": [],
    "c2": [],
    "r5": [],
    "graphnode1": ["stm32f103", "drv8825"]
  },
  "layouts": {
    "stm32f103": "/layout.png",
    "drv8825": "/layout.png",
    "c1": "/layout.png",
    "c2": "/layout.png",
    "graphnode1": "/layout.png"
  },
}

@app.route('/setquery', methods=['POST'])
def set_query():
    data = request.json
    components = data.get('components', [])
    context = data.get('context', "")
    print("Received components:", components)
    print("Received context:", context)
    return jsonify({"status": "success", "message": "Query received"}), 200

@app.route("/buildstatus", methods=['GET'])
def build_status():
    return jsonify(BUILD_STATE), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)