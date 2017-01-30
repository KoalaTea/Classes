import socket
from os import listdir
from os.path import isfile
from Request import Request

class WebServer(object):

    def __init__(self, ip="0.0.0.0", port=80, config_file=None):
        if(config_file):
            pass
        else:
            self.ip=ip
            self.port=port
            self.log = "/var/log/mywebserv/mywebserv.log"
            self.errlog = "/var/log/mywebserv/mywebserv.log"
            self.implemented_methods = [ "PUT", "GET", "POST", "DELETE", "CONNECT" ]
            self.allowed_methods = [ "PUT", "GET", "POST", "DELETE", "CONNECT" ]
            self.code = []
            self.root = "/var/www"
            self.slash = "/index.html"


    def _error_response(self, error):
        if(error==405):
            if(isfile(self.root + "/405.html")):
                response_data = "have 405.html"
            else:
                response_data = "no 405.html"
            response= "HTTP/1.1 405 Method Not Allowed" + "\r\n"
            response+="Allow: " + ", ".join(self.allowed_methods) + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

        elif(error==404):
            if(isfile(self.root + "/404.html")):
                response_data = "have 405.html"
            else:
                response_data = "no 404.html"
            response= "HTTP/1.1 404 File Not Found" + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

        elif(error==501):
            response_data = "oops 501"
            response= "HTTP/1.1 501 Method Not Implemented" + "\r\n"
            response+="Allow: " + ",".join(self.allowed_methods) + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            respones+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

    def _response(self, method, resource, data=''):
        if(method not in self.implemented_methods):
            return self._error_response(501)
        elif(method not in self.allowed_methods):
            return self._error_response(405)
        elif(method == "GET" or method == "POST"):
            if(resource=="/"):
                resource = self.slash
            if(any(isfile(self.root + resource) for resource in listdir(self.root))):
                #is a responses data suppossed to be \r\n per line?
                with open(join(self.root, resource), 'r') as opened_file:
                    response_data = opened_file.read
                    opened_file.close()
                response= "HTTP/1.1 200 OK" + "\r\n"
                response+="Content-Length: " + str(len(response_data)) + "\r\n"
                response+="\r\n"
                response+=response_data
                response+="\r\n\r\n"
            else:
                return self._error_response(404)

    def _handle_client(self, client_socket):
        full_data = ''

        '''
        while True:
            data = client_socket.recv(1024)
            full_data = full_data + data
            if not data:
                break
        '''
        while "\r\n\r\n" not in full_data:
            data = client_socket.recv(1024)
            full_data = full_data + data
            if not data:
                break

        request = Request(full_data)
        if("Content-Length" in request.headers):
            current_data_len = len(request.data)
            print(current_data_len)
            content_len = int(request.headers["Content-Length"])
            print(content_len)
            if(current_data_len < content_len):
                data = client_socket.recv(content_len - current_data_len)
                request.data += data
                request.raw += data

        #full_data = client_socket.recv(1024)

        #temp testing stuff
        print(repr(request.raw))
        print(request.raw)
        print(request.headers)
        method = request.get_method()
        resource = request.get_resource()

        response = self._response(method, resource, request.data)
        print(response)
        client_socket.send(response)

        client_socket.close()

    def serve_web(self):
        try:
            server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip, self.port))
            server_socket.listen(10)
            while 1:
                (client_socket, address) = server_socket.accept()
                self._handle_client(client_socket)
        except KeyboardInterrupt:
            print("Killing server due to SIGINT")
            server_socket.close()

def main():
    serv = WebServer("127.0.0.1", 80)
    serv.serve_web()

main()
