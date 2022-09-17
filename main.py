import sys, os, random, websocket, json, requests, time, threading

prot=['','', ''] #Dont Leave

TOKEN="" #User token

def send_json_request(ws, request): #send ws request
    ws.send(json.dumps(request))    #strinfigy json and send

def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)

def heartbeat(interval, ws):
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send_json_request(ws, heartbeatJSON)

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')

event = recieve_json_response(ws)

heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

payload = {
    'op': 2,
    "d": {
        "token": TOKEN,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": 'pc'
        }
    }
}
send_json_request(ws, payload)

grupe=[]

while True:
    event = recieve_json_response(ws)

    try:
        if event['t'] == "READY":                                       #On ready event

            gay=0
            for channel in event['d']['private_channels']:
                if event['d']['private_channels'][gay]['type'] == 3:
                    grupe.append(event['d']['private_channels'][gay]['id'])
                gay+=1

            for grupa in grupe:
                if(str(grupa) not in prot):
                    requests.delete(url=f"https://canary.discord.com/api/v9/channels/{grupa}", headers={"authorization": TOKEN})
                    time.sleep(1)

            print("Left ",grupe)
    except Exception as err:
        print(err)
