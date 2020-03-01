from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from io import BytesIO

user_data = {
    "user1": "qwerty",
    "user2": "ytrewq"
}


class HttpProcessor(BaseHTTPRequestHandler):
    keys = dict()

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/json')
        self.end_headers()

        # Код ниже - простая отсылка файла
        """f = open("data.json", "rb")
        self.wfile.write(f.read())
        f.close()"""

        # Код ниже - простая проверка авторизации
        # response = BytesIO()
        logined = False
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        mas = body.decode().split("&")
        for key_value_combo in range(len(mas)):
            temp_mas = mas[key_value_combo].split("=")
            self.keys.update({temp_mas[0]: temp_mas[1]})
        print("Recieved:\n{}".format(self.keys))
        # try:
        if self.keys["username"] in user_data.keys():
            if self.keys["password"] == user_data[self.keys["username"]]:
                if self.keys["download"] != "yes":
                    self.wfile.write("{}".format(self.keys["username"]).encode())
                logined = True
            else:
                self.wfile.write("Wrong password!".encode())
        else:
            self.wfile.write("Wrong username!".encode())
        if logined:
            if self.keys["download"] == "yes":
                f = open("data.json", "rb")
                self.wfile.write(f.read())
                f.close()

    def do_POST(self):
        """content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())"""

        """length = self.headers['content-length']
        data = self.rfile.read(int(length))

        print(data)

        with open("data2.json", 'w') as fh:
            fh.write(data.decode())

        self.send_response(200)"""

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        filename = form['file'].filename
        data = form['file'].file.read()
        open(".\\%s" % filename, "wb").write(data)
        self.send_response(200)



if __name__ == '__main__':
    serv = HTTPServer(("localhost", 80), HttpProcessor)
    serv.serve_forever()
