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

        self.slash = "index.html"
        self.aliases = {"/cgi-bin" : "/var/www/cgi-bin/"}
        self.cgi = "/cgi-bin"
        self.cgiaccess = { ".php":"php"}
        self.implemented_methods = [ "PUT", "GET", "POST", "DELETE", "CONNECT" ]

        if(config_file):
            if(isfile(config_file)):
                config = {}
                lines = [line.rstrip('\n') for line in open(config_file)]
                for line in lines:
                    if line.startswith('#'):
                        pass
                    else:
                        config_line = line.split(':')
                        if(config_line[0]=='ScriptAlias'):
                            thealias = config_line[1].split(",")
                            if(len(thealias) < 2):
                                self.err_log(None, 0, "Bad Alias line look at example")
                            else:
                                if('aliases' not in config):
                                    config['aliases'] = {}
                                config['aliases'][thealias[0]] = thealias[1]
                        else:
                            config[config_line[0]] = config_line[1].rstrip()
                print(config)

                if 'ip' in config:
                    self.ip=config['ip']
                else:
                    self.ip = ip

                if 'port' in config:
                    self.port=int(config['port'])
                else:
                    self.port=port

                if 'log' in config:
                    self.logfile=config['log']
                else:
                    self.logfile="mywebserv.log"

                if 'errlog' in config:
                    self.errlogfile=config['errlog']
                else:
                    self.errlogfile="mywebserv.err"

                if 'allowed_methods' in config:
                    self.allowed_methods=[]
                    for method in config['allowed_methods'].split(','):
                        self.allowed_methods.append(method.rstrip())
                else:
                    self.allowed_methods = [ "PUT", "GET", "POST", "DELETE", "CONNECT" ]

                if 'root' in config:
                    self.root=config['root']
                else:
                    self.root="/var/www/html"

                if 'aliases' in config:
                    self.aliases=config['aliases']

                if 'cgi' in config:
                    self.cgi=config['cgi']

        else:
            self.ip=ip
            self.port=port
            self.logfile = "mywebserv.log"
            self.errlogfile = "mywebserv.err"
            self.allowed_methods = [ "PUT", "GET", "POST", "DELETE", "CONNECT" ]
            self.code = []
            self.root = "/var/www/html/"

    def err_log(self, request, return_code, e):
        if(request is None):
            log_file = open(self.errlogfile, "a+")
            log_line = "web server error: " + e
        else:
            print(e)
            log_file = open(self.errlogfile, "a+")
            log_line = request.request_line + " " + str(return_code)
            if 'User-Agent' in request.headers:
                log_line += " - " + request.headers['User-Agent']
        log_file.write(log_line + "\n")
        log_file.close()

    def log(self, request, return_code):
        log_file = open(self.logfile, "a+")
        log_line = request.request_line + " " + str(return_code)
        if 'User-Agent' in request.headers:
            log_line += " - " + request.headers['User-Agent']
        log_file.write(log_line + "\n")
        log_file.close()

    # _resource_path
    #   return the path for the resource requested
    #
    # Arguements
    #   resource    - the resource part of the request line
    #
    # Returns
    #   full_path   - the full path that the resource is located at
    def _resource_path(self, resource):
        full_path = None
        if(resource=="/"):
            full_path = self.root + self.slash
        elif(resource[0] != "/"):
            full_path = self.root + resource
        elif(len(self.aliases) != 0):
            for alias in self.aliases:
                if(resource.startswith(alias)):
                    full_path = self.aliases[alias] + resource[len(alias)+1:]
                    break
            if(full_path is None):
                return self.root + resource
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
            return response

        elif(error==500):
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
            return response

        elif(error==501):
            response_data = "oops 501"
            response= "HTTP/1.1 501 Method Not Implemented" + "\r\n"
            response+="Allow: " + ",".join(self.allowed_methods) + "\r\n"
            response+="Content-Length: " + str(len(response_data)) + "\r\n"
            response+="\r\n"
            response+=response_data
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
            self.log(request, 400)
            return self._error_response(400)
        method = request.get_method()
        resource = request.get_resource()

        # if the method is not implemeneted
        if(method not in self.implemented_methods):
            self.log(request, 501)
            return self._error_response(501)

        # if the method is not allowed
        elif(method not in self.allowed_methods):
            self.log(request, 405)
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
                    self.log(request, 200)
                    return response
                except IOError:
                    self.log(request, 403)
                    return self._error_response(403)
            else:
                self.log(request, 404)
                return self._error_response(404)

        # if the method is a PUT request
        elif(method == "PUT"):
            #201 success 200 modified
            requested_file = self._resource_path(resource)

            return_code = 200
            # if requested file exists
            if(isfile(requested_file) and abspath(requested_file)[:len(self.root)] == self.root):
                return_code = 200
                response= "HTTP/1.1 200 OK" + "\r\n"
                response+="Content-Length: " + str(len(response_data)) + "\r\n"
                response+="\r\n"
            # if requested file does not exist
            else:
                return_code = 201
                response= "HTTP/1.1 201 OK" + "\r\n"
                response+="Content-Length: " + str(len(response_data)) + "\r\n"
                response+="\r\n"

            # make the file
            try:
                with open(requested_file, 'w') as opened_file:
                    opened_file.write(request.data)
                    opened_file.close()
                response+=response_data
                self.log(request, return_code)
                return response
            except IOError:
                self.log(request, 403)
                return self._error_response(403)

        # if the method is a DELETE request
        #TODO returns
        elif(method == "DELETE"):
            #200 completed 204 No Content (enacted but no content returned) 202 accepted but not enact
            requested_file = self._resource_path(resource)

            if(isfile(requested_file) and abspath(requested_file)[:len(self.root)] == self.root):
                try:
                    remove(requested_file)
                    self.log(request, 200)
                except IOError:
                    self.log(request, 403)
                    return self._error_response(403)
            else:
                self.log(request, 204)
                return self._error_response(204)





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
                        environ["SCRIPT_FILENAME"] = cgi_resource
                        if "Cookie" in request.headers:
                            environ["HTTP_COOKIE"] = request.headers["Cookie"]
                        if 'Content-Length' in request.headers:
                            print(request.headers['Content-Length'].strip())
                            environ["CONTENT_LENGTH"] = request.headers['Content-Length'].strip()
                        else:
                            environ["CONTENT_LENGTH"] = ""
                        #environ["QUERY_STRING"] = request.data
                        #environ["SERVER_PORT"] =
                        #environ["REMOTE_ADDR"] = request.get_method()
                        if(request.query):
                            environ["QUERY_STRING"] = request.query
                        else:
                            environ["QUERY_STRING"] = ""
                        try:
                            #WHY DOES THIS NOT WORK!!! It like really should
                            print(cgi_resource)
                            if(request.get_method() == "POST"):
                                print(request.data)
                                p = subprocess.Popen(shebang_location,
                                                    stdin=subprocess.PIPE,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    env=environ
                                                    )
                                stdout, stderr = p.communicate(request.data)
                                if stderr:
                                    self.err_log(request, 500, stderr)
                                p.stderr.close()
                                p.stdout.close()
                                response = stdout
                            else:
                                response = subprocess.Popen(shebang_location, stdout=subprocess.PIPE).communicate()[0]
                        except Exception as e:
                            self.err_log(request, 500, e)
                            return self._error_response(500)
                        print("Response:" + response)
                        self.log(request, 200)
                        real_response = "HTTP/1.1 200 OK" + "\r\n"
                        real_response+=response
                        print("MY REAL: " + real_response)
                        return real_response

                            #TODO split query line if it exist and set variables
                            #/usr/lib64/python2.7/CGIHTTPServer.py
                    else:
                        self.err_log(request, 500, "Shebang file does not exist")
                        return self._error_response(500)
                else:
                    self.err_log(request, 500, "Missing Shebang")
                    return self._error_response(500)

            else:
                self.log(request, 404)
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

        if full_data != '':
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
            method = request.get_method()
            # if the method is a CONNECT request
            if(method == "CONNECT"):
                #create the socker
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #check if there is a port attached to our 'resource'
                #for both try to create a ocket if it fails send an error and return
                host = request.get_resource().split(':')
                if(len(host) == 1):
                    try:
                        s.connect((host[0], 80))
                    except:
                        client_socket.send(self._error_response(500))
                        client_socket.close()
                        return
                else:
                    try:
                        s.connect((host[0], int(host[1])))
                    except:
                        client_socket.send(self._error_response(500))
                        client_socket.close()
                        return

                #if we did not hit an except we send out ok response
                client_socket.send("HTTP/1.1 200 OK\r\n")

                #now we read data until one of the two connections breaks
                while True:
                    #CLIENT SOCKET
                    #constantly reset full_data since that is our output
                    full_data = ''
                    #while we don't hit the end of a request keep reading and forwarding the
                    # data from the client
                    while "\r\n\r\n" not in full_data:
                        data = client_socket.recv(1024)
                        s.send(data)
                        full_data = full_data + data
                        #if the socket dies break
                        if not data:
                            break
                    #if the client socket died, we will break
                    print("Client sent\n" + full_data)
                    if not data:
                        print("Client broke on us")
                        break
                    #if we did not break due to a socket death there may be more data
                    #from the client (like POST with a lot of data!)
                    if full_data != '':
                        request = Request(full_data)
                        if("Content-Length" in request.headers):
                            current_data_len = len(request.data)
                            print(current_data_len)
                            content_len = int(request.headers["Content-Length"])
                            print(content_len)
                            if(current_data_len < content_len):
                                data = client_socket.recv(content_len - current_data_len)
                                s.send(data)
                                full_data += data

                    #SERVER SOCKET
                    #if the client socket completed it's output then we will
                    #wait for the server to respond (problem with our \r\n\r\n
                    #is it is not correct now)
                    full_data = ''
                    while "\r\n\r\n" not in full_data:
                        data = s.recv(1024)
                        full_data = full_data + data
                        if not data:
                            break
                    print("The sever gave us\n" + full_data)
                    client_socket.send(full_data)
                    if not data:
                        print("The sever broke on us")
                        break
                s.close()
            else:
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
                #self._handle_client(client_socket)
                # Threading did not work when I last tried. I will come back to this
                threading.Thread(target=self._handle_client, args=(client_socket,)).start()
        except KeyboardInterrupt:
            print("Killing server due to SIGINT")
            server_socket.close()
