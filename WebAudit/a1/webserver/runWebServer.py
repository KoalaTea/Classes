from WebServer import WebServer

def main():
    my_server = WebServer("127.0.0.1", 8008)
    my_server.serve_web()

if __name__ == "__main__":
    main()
