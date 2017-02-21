#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO:
#   move to 3.4 dealing with sockets
#   Connect method
import socket
from os import listdir, remove, environ
from os.path import isfile, abspath
from Request import Request
import threading
import subprocess
#import subprocess #php?

# WebServer Class to deal with all web things
class WebServer(object):

    # __init__
    #   Constructor
    #
    # Arguments:
    #   ip          - the ip the webserver should bind to
    #   port        - the port the webserver should bind to
    #   config_file - a config_file to define settings for the webserver
    #
    # Returns:
    #   Webserver object
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
            self.root = "/var/www/html/"
            self.slash = "index.html"
            self.aliases = {"/cgi-bin" : "/var/www/cgi-bin/"}
            self.cgi = "/cgi-bin"
            self.cgiaccess = { ".php":"php"}

    # _resource_path
    #   return the path for the resource requested
    #
    # Arguements
    #   resource    - the resource part of the request line
    #
    # Returns
    #   full_path   - the full path that the resource is located at
    def _resource_path(self, resource):
        if(resource=="/"):
            full_path = self.root + self.slash
        elif(resource[0] != "/"):
            full_path = self.root + resource
        elif(len(self.aliases) != 0):
            for alias in self.aliases:
                if(resource.startswith(alias)):
                    full_path = self.aliases[alias] + resource[len(alias)+1:]
        else:
            full_path = self.root + resource[1:]
        return full_path


    # _error_response
    #   Returns error responses based on the error code
    #
    # Arguements:
    #   error       - The error code
    #
    # Returns
    #   response    - The http response headers and body
    def _error_response(self, error):
        if(error==400):
            if(isfile(self.root + "400.html")):
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
            if(isfile(self.root + "401.html")):
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
            if(isfile(self.root + "403.html")):
                response_data = "have 403.html"
            else:
                response_data = "no 403.html"
            response= "HTTP/1.1 403 Forbidden" + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

        elif(error==404):
            if(isfile(self.root + "404.html")):
                response_data = "have 405.html"
            else:
                response_data = "no 404.html"
            response= "HTTP/1.1 404 File Not Found" + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

        elif(error==405):
            if(isfile(self.root + "405.html")):
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

        elif(error=500):
            response_data = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>500 Internal Server Error</title>
</head><body>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error or
misconfiguration and was unable to complete
your request.</p>
<p>Please contact the server administrator at
 root@localhost to inform them of the time this error occurred,
 and the actions you performed just before this error.</p>
<p>More information about this error may be available
in the server error log.</p>
</body></html>
"""
            response= "HTTP/1.1 500 Internal Server Error" + "\r\n"
            response+="Allow: " + ",".join(self.allowed_methods) + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"

        elif(error==501):
            response_data = "oops 501"
            response= "HTTP/1.1 501 Method Not Implemented" + "\r\n"
            response+="Allow: " + ",".join(self.allowed_methods) + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
            response+="\r\n\r\n"
            return response

    # _response
    #   Decides how to deal with an http request and crafts the response
    #
    # Arguements
    #   request     - The request object representing the http request from the client
    #   data        - Data posted in the request if it exists
    #
    # Returns
    #   response    - Servers http response to be sent back to the client
    def _response(self, request, data=''):
        if(not request.get_resource().startswith(self.cgi)):
           return self._run_method(request)
        else:
           return self._run_cgi(request)

    # _run_method
    #   Runs the requested method on the resource if the method is allowed and implemented
    #
    # Arguements
    #   request     - The request object representing the http request from the client
    #
    # Returns
    #   response    - Servers http response to be sent back to the client
    def _run_method(self, request):
        # if the request is bad
        if(request.error):
            return self._error_response(400)
        method = request.get_method()
        resource = request.get_resource()

        # if the method is not implemeneted
        if(method not in self.implemented_methods):
            return self._error_response(501)

        # if the method is not allowed
        elif(method not in self.allowed_methods):
            return self._error_response(405)

        # if the method is a GET or POST request
        elif(method == "GET" or method == "POST"):
            requested_file = self._resource_path(resource)
            print(requested_file)

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

        # if the method is a PUT request
        elif(method == "PUT"):
            #201 success 200 modified
            requested_file = self._resource_path(resource)

            # if requested file exists
            if(isfile(requested_file) and abspath(requested_file)[:len(self.root)] == self.root):
                response= "HTTP/1.1 200 OK" + "\r\n"
                response+="Content-Length: " + str(len(response_data)) + "\r\n"
                response+="\r\n"
            # if requested file does not exist
            else:
                response= "HTTP/1.1 201 OK" + "\r\n"
                response+="Content-Length: " + str(len(response_data)) + "\r\n"
                response+="\r\n"

            # make the file
            try:
                with open(requested_file, 'w') as opened_file:
                    opened_file.write(request.data)
                    opened_file.close()
                response+=response_data
                return response
            except IOError:
                return self._error_response(403)

        # if the method is a DELETE request
        elif(method == "DELETE"):
            #200 completed 204 No Content (enacted but no content returned) 202 accepted but not enact
            requested_file = self._resource_path(resource)

            if(isfile(requested_file) and abspath(requested_file)[:len(self.root)] == self.root):
                try:
                    remove(requested_file)
                except IOError:
                    return self._error_response(403)
            else:
                return self._error_response(204)

        # if the method is a CONNECT request
        elif(method == "CONNECT"):
            pass

    # _run_cgi
    #   Run cgi to get responses
    #
    # Arguements
    #   request     - The request object representing the http request from the client
    #
    # Returns
    #   response    - Servers http response to be sent back to the client
    #
    def _run_cgi(self, request):
        print("got cgi")
        # if the request is bad
        if(request.error):
            return self._error_response(400)
        method = request.get_method()
        resource = request.get_resource()

        # if the method is not implemeneted
        if(method not in self.implemented_methods):
            return self._error_response(501)

        # if the method is not allowed
        elif(method not in self.allowed_methods):
            return self._error_response(405)

        else:
            cgi_resource = self._resource_path(request.get_resource())
            if(isfile(cgi_resource)):
                cgi_file = open(cgi_resource)
                shebang = cgi_file.readlines()[0]
                if(shebang.startswith("#!")):
                    shebang_location = shebang[2:].strip()
                    if(isfile(shebang_location)):
                        environ["REQUEST_METHOD"] = request.get_method()
                        environ["SERVER_PROTOCOL"] = request.protocol
                        environ["REQUEST_URI"] = request.get_resource()
                        environ["HTTP_CONNECTION"] = request.get_method()
                        #environ["SERVER_PORT"] =
                        #environ["REMOTE_ADDR"] = request.get_method()
                        try:
                            response = subprocess.Popen([shebang_location, cgi_resource], stdout=subprocess.PIPE).communicate()[0]
                        except:
                            return self._error_response(500)
                        print("Response:" + response)
                        return response
                    else:
                        return self._error_response(500)
                else:
                    return self._error_response(500)

            else:
                return self._error_response(404)


    # _handle_client
    #   Handles client connections, recieving the request and sending a response
    #
    # Arguments
    #   client_socket   - The client connection socket
    #
    # Returns
    #   None
    def _handle_client(self, client_socket):
        full_data = ''

        '''
        while True:
            data = client_socket.recv(1024)
            full_data = full_data + data
            if not data:
                break
        '''
        # have a timeout
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

    # serve_web
    #   starts the webserver and handles connections sending them to _handle_client
    #
    # Arguments
    #   None
    #
    # Returns
    #   None
    def serve_web(self):
        try:
            server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip, self.port))
            server_socket.listen(10)
            while 1:
                (client_socket, address) = server_socket.accept()
                self._handle_client(client_socket)
                # Threading did not work when I last tried. I will come back to this
                #threading.Thread(target=self._handle_client, args=(client_socket,))
        except KeyboardInterrupt:
            print("Killing server due to SIGINT")
            server_socket.close()
