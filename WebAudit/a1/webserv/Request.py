class Request(object):

    def __init__(self, client_data):
        client_data_list = client_data.split("\r\n\r\n")
        client_headers = {}
        split_headers = client_data_list[0].split("\r\n")
        #currently still holds space in front from the split :
        for header in split_headers[1:]:
            split_header = header.split(":")
            client_headers[split_header[0]] = ':'.join(split_header[1:])
        self.headers = client_headers
        self.data = client_data_list[1]
        self.request_line = split_headers[0]
        self.raw = client_data

    def get_method(self):
        request_list = self.request_line.split()
        return request_list[0]

    def get_resource(self):
        request_list = self.request_line.split()
        return request_list[1]



