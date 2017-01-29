import socket
import os
from Request import Request

class WebServer(object):

    def __init__(self, ip=0.0.0.0, port=80, config_file=None):
        if(config_file):
            pass
        else:
            self.ip=ip
            self.port=port
            self.log = "/var/log/mywebserv/mywebserv.log"
            self.errlog = "/var/log/mywebserv/mywebserv.log"
            self.methods = [ "PUT", "GET", "PUT", "DELETE", "CONNECT" ]
            self.code = []
            self.root = "/var/www/"


    def _response(self, method, resource, data=''):
        if(method not in self.methods):
            if(os.is_file(self.root + "405.html")):
                response_data = "have 405.html"
            else:
                response_data = "no 405.html"
            response= "HTTP/1.1 405 METHOD NOT ALLOWED" + "\r\n"
            response+="Allow: " + ", ".join(self.methods) + "\r\n"
            response+="Content-Length: " + str(response_data.len()) + "\r\n"
            response+="\r\n\r\n"
            response+=response_data
            return response
        else:
            pass

    def _parse(self, client_data):
        request = Request(client_data)
        method = request.get_method()
        resource = request.get_resource()
        data = request.data

        self._response(method, resource, data)

    def _handle_client(self, client_socket):
        full_data = ''
        while True:
            data = client_socket.recv(1024)
            full_data = full_data + data
            if not data:
                break

        self._parse(full_data)
        client_socket.close()

    def serve_web(self):
        server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(10)
        while 1:
            (client_socket, address) = server_socket.accept()
            self._handle_client(client_socket)

def main():
    serv = WebServer("127.0.0.1", 80)
    serv.serve_web()

main()
