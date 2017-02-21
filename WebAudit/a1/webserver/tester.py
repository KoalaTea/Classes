import socket
import requests

def usesocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # root user python
    #s.connect(("127.0.0.1", 80))
    # non root user python
    s.connect(("127.0.0.1", 8008))

    # bad req
    #s.send("GET / HTTP/1.2\r\n\r\n")
    # false file
    #s.send("GET /notreal HTTP/1.0\r\n\r\n")
    # no permissions file
    #s.send("GET /badperms HTTP/1.0\r\n\r\n")
    # break out of dir req
    #s.send("GET /../../../../etc/passwd HTTP/1.0\r\n\r\n")
    # normal req
    #s.send("GET / HTTP/1.0\r\n\r\n")
    # cgi req
    s.send("GET /cgi-bin/index.php HTTP/1.0\r\n\r\n")
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

#userequests()
usesocket()
