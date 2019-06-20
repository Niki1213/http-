from socket import *
import json

s = socket()
s.bind(("0.0.0.0", 8000))
s.listen(3)
c, addr = s.accept()
data = c.recv(1024).decode()
data = json.loads(data)
print(data)
d = {"status": "200", "data": "From test"}
data = json.dumps(d)
c.send(data.encode())

c.close()
s.close()
