class Request(object):

    def __init__(self, client_data):
        client_data_list = client_data.split("\r\n\r\n")
        self.headers = client_data_list[0]
        self.data = client_data_list[1]

    def get_method():
        headers_list = self.headers.split("\r\n")
        request_list = headers_list[0].split()
        return request_list[0]

    def get_resource():
        headers_list = self.headers.split("\r\n")
        request_list = headers_list[0].split()
        return request_list[1]



