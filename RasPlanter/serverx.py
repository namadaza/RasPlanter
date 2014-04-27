import tornado.web
import socket
import re
from base64 import b64encode
from hashlib import sha1

websocket_answer = (
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    'Sec-WebSocket-Accept: {key}\r\n\r\n',
)

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8999))
s.listen(1)

client, address = s.accept()
text = client.recv(1024)
print text

key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', text)
    .groups()[0]
    .strip())

response_key = b64encode(sha1(key + GUID).digest())
response = '\r\n'.join(websocket_answer).format(key=response_key)

print response
client.send(response)

print client.recv(1024)
client.send('hello from server')