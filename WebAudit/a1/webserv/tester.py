import socket
import requests

def usesocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect(("127.0.0.1", 80))
    s.send("GET / HTTP/1.0\r\n\r\n")
    #s.close()


    full_data = ''
    while True:
        data = s.recv(1024)
        full_data+=data
        if not data:
            break

    print(repr(full_data))
    print(full_data)

def userequests():
    r=requests.post("http://127.0.0.1/", json={"what": "kay"})
    print(r)
    print(r.headers)
    print(r.text)

userequests()
