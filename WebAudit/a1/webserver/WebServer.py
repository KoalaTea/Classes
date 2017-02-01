import socket
from os import listdir
from os.path import isfile, abspath
from Request import Request
import threading
#import subproccess #php?

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
            self.root = "/var/www/html"
            self.slash = "/index.html"


    def _error_response(self, error):
        if(error==400):
            if(isfile(self.root + "/400.html")):
                response_data = "have 400.html"
            else:
                response_data = "no 400.html"
            response= "HTTP/1.1 400 Bad Request" + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

        elif(error==401):
            if(isfile(self.root + "/401.html")):
                response_data = "have 401.html"
            else:
                response_data = "no 401.html"
            response= "HTTP/1.1 401 Unauthorized" + "\r\n"
            response+="Allow: " + ", ".join(self.allowed_methods) + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

        elif(error==403):
            if(isfile(self.root + "/403.html")):
                response_data = "have 403.html"
            else:
                response_data = "no 403.html"
            response= "HTTP/1.1 403 Forbidden" + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

        elif(error==405):
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
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

    def _response(self, request, data=''):
        if(request.error):
            return self._error_response(400)
        method = request.get_method()
        resource = request.get_resource()
        if(method not in self.implemented_methods):
            return self._error_response(501)
        elif(method not in self.allowed_methods):
            return self._error_response(405)
        elif(method == "GET" or method == "POST"):
            if(resource=="/"):
                resource = self.slash
            requested_file = self.root + resource
            if(isfile(requested_file) and abspath(requested_file)[:len(self.root)] == self.root):
                #is a responses data suppossed to be \r\n per line?
                try:
                    with open(requested_file, 'r') as opened_file:
                        response_data = opened_file.read()
                        opened_file.close()
                    response= "HTTP/1.1 200 OK" + "\r\n"
                    response+="Content-Length: " + str(len(response_data)) + "\r\n"
                    response+="\r\n"
                    response+=response_data
                    return response
                except IOError:
                    return self._error_response(403)
            else:
                return self._error_response(404)
        elif(method == "PUT"):
            #201 success 200 modified
            pass
        elif(method == "DELETE"):
            #200 completed 204 No Content (enacted but no content returned) 202 accepted but not enact
            pass
        elif(method == "CONNECT"):
            pass

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

        response = self._response(request, request.data)
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
                #threading.Thread(target=self._handle_client, args=(client_socket,))
        except KeyboardInterrupt:
            print("Killing server due to SIGINT")
            server_socket.close()
