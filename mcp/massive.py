#!/usr/bin/env python3
from skidl import *
import os
import anthropic
import json
# import kinet2pcb

n = 4
datas = []
d2s = []
for i in range(n):
    with open("adjacency_" + str(i) + ".json", "r") as f:
        datas.append(json.load(f))
        d2s.append(datas[-1])
        datas[-1] = datas[-1]["device_pins"]

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
API_URL = "https://api.anthropic.com/v1/messages"

# ===== PROMPT TEMPLATE =====
SYSTEM_PROMPT = (
    """
    You are an expert electrical engineer AI with specific expertise in PCB components. You will be given:

    Multiple JSON lists for different components, the i'th component in the following format:
    "i_device_pins": {
        "AVDD": "i_device_pin_12",
        "AVSS": "i_device_pin_3", 
        "DVDD": "i_device_pin_13",
        "DGND": "i_device_pin_2",
        "AIN0/REFP1": "i_device_pin_11",
        "AIN1": "i_device_pin_10",
        "AIN2": "i_device_pin_7", 
        "AIN3/REFN1": "i_device_pin_6",
        "REFP0": "i_device_pin_9",
        "REFN0": "i_device_pin_8",
        "SCLK": "i_device_pin_1",
        "CS": "i_device_pin_16",
        "DIN": "i_device_pin_14",
        "DOUT/DRDY": "i_device_pin_15",
        "DRDY": "i_device_pin_14",
        "CLK": "i_device_pin_3"
    }

    Your job is to decide which connections between components are necessary. For example, you might have to connect:
    * 1_device_pin_15 to 0_device_pin_4
    * 2_device_pin_6 to 3_device_pin_9
    * 0_device_pin_1 to 3_device_pin_1

    **Example output:**

    If the above three connections are the only needed connections, please output as follows:
    "connections": {
        "0_device_pin_1": ["3_device_pin_1"],
        "1_device_pin_15": ["0_device_pin_4"],
        "2_device_pin_6": ["3_device_pin_9"]
    }

    Your task is to integrate this chip:

    **Rules:**

    * Only include **required connections**.
    * Each edge represents a **necessary electrical connection**.
    * Be very careful about which nodes we are connecting; for example, GND should connect to DGND because they are both ground.
    * You ARE allowed to connect pins even if the devices are not one index apart.
    
    IMPORTANT: Do **not** include any explanations, reasoning, or extra text.  
    Output **only** a valid JSON edge list exactly as shown in the example.  
    The JSON must be parseable; do not include comments, markdown, or extra formatting.
    """
)

for i in range(n):
    datas[i] = json.dumps(datas[i])
    datas[i] = "device_pins: " + datas[i]
    datas[i] = datas[i].replace("device_pin", str(i) + "_device_pin")
    d2s[i] = json.dumps(d2s[i])
    # d2s[i] = "{\"device_pins\": " + d2s[i] + "}"
    d2s[i] = d2s[i].replace("device_pin", str(i) + "_device_pin")
    d2s[i] = json.loads(d2s[i])

print(datas)

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
message = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=1024,
    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": SYSTEM_PROMPT + "\n\nHere is your information:\n\n" +
            "\n\n".join(datas)}]}]
)
# # resp = requests.post(API_URL, headers=headers, json=payload, timeout=300)
# # resp.raise_for_status()

nets = {}
components = {}

def gen(idx):
    print("\n\n\n")
    print(d2s[idx])
    aux_components = d2s[idx]["auxiliary_components"]
    connections = d2s[idx]["connections"]
    dev_pins = d2s[idx][str(idx) + "_device_pins"]

    for name, comp in aux_components.items():
        if comp["type"] == "capacitor":
            c = Part("Device", "C", value=comp["value"], footprint="Capacitor_SMD:C_0603_1608Metric")
            components[str(idx) + "_" + name] = c
        elif comp["type"] == "resistor":
            r = Part("Device", "R", value=comp["value"], footprint="Resistor_SMD:R_0603_1608Metric")
            components[str(idx) + "_" + name] = r
        elif comp["type"] == "crystal":
            c = Part("Device", "Crystal", value=comp["value"], footprint="Crystal:Crystal_0603_1608Metric")
            components[str(idx) + "_" + name] = c
        elif comp["type"] == "inductor":
            c = Part("Device", "L", value=comp["value"], footprint="Inductor_SMD:L_0603_1608Metric")
            components[str(idx) + "_" + name] = c
        elif comp["type"] == "diode":
            c = Part("Device", "D", value=comp["value"], footprint="Diode_SMD:D_0603_1608Metric")
            components[str(idx) + "_" + name] = c
        else:
            raise ValueError(f"Unsupported component type: {comp['type']}")

    # ===== Create Device Pins =====
    # We'll make a dummy IC for the main device
    device = Part("MCU_Microchip_ATmega", "ATmega8-16A", footprint="Package_QFP:TQFP-32_7x7mm_P0.8mm")
    components[str(idx) + "_main_device"] = device
    for i in range(1, 33):
        pin_name = str(idx) + "_device_pin_" + str(i)
        nets[pin_name] = Net(pin_name)
        device[i] += nets[pin_name]

    # ===== Connect Components to Nets =====
    for category, cat_connections in connections.items():
        for node, connected_nodes in cat_connections.items():
            # If the node is an auxiliary component
            if node in dev_pins:
                node = dev_pins[node]
            if node in components:
                comp = components[str(idx) + "_" + node]
                for pin_num, conn_node in enumerate(connected_nodes, start=1):
                    if conn_node in dev_pins:
                        conn_node = dev_pins[conn_node]
                    if conn_node not in nets:
                        nets[conn_node] = Net(conn_node)
                    comp[pin_num] += nets[conn_node]
            # If the node is a device pin
            elif node.startswith(str(idx) + "_device_pin"):
                pin_net = nets[node]
                for conn_node in connected_nodes:
                    if conn_node in dev_pins:
                        conn_node = dev_pins[conn_node]
                    if conn_node not in nets:
                        nets[conn_node] = Net(conn_node)
                    pin_net += nets[conn_node]
            else:
                # Possibly a net by itself
                if node not in nets:
                    nets[node] = Net(node)
                for conn_node in connected_nodes:
                    if conn_node in dev_pins:
                        conn_node = dev_pins[conn_node]
                    if conn_node not in nets:
                        nets[conn_node] = Net(conn_node)
                    nets[node] += nets[conn_node]

for i in range(n):
    gen(i)

print(components)

info = json.loads(message.content[0].text)["connections"]
for n1, n2s in info.items():
    for n2 in n2s:
        if n1 not in nets:
            nets[n1] = Net(n1)
        if n2 not in nets:
            nets[n2] = Net(n2)
        nets[n1] += nets[n2]
        
# ===== Generate Netlist =====
# generate_netlist()
generate_pcb()