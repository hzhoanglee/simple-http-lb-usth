import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        server_ip = socket.gethostbyname(socket.gethostname())
        path = self.path
        if path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
            return
        else:
            response = f"Port: {os.environ.get('SERVER_PORT', 8080)}\nServer IP: {server_ip}\nClient IP: {client_ip}\nPath: {path}\n"
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode())

            with open('data.log', 'a') as f:
                f.write(f"{server_ip},{client_ip},{path}\n")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server started on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    port = int(os.environ.get('SERVER_PORT', 8080))
    run(port=port)
