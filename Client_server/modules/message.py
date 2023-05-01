import json


def send_message(sock, message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode('utf-8')
    sock.send(encoded_message)


def get_message(client):
    data = client.recv(1000000)
    if isinstance(data, bytes):
        json_response = data.decode('utf-8')
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError