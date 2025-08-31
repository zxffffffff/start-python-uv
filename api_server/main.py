from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {'message': 'Hello from [api-server]!'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            response = {'error': 'Not Found'}
            self.wfile.write(json.dumps(response).encode('utf-8'))

def main():
    server_address = ('', 5001)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("[api-server] running on http://localhost:5001")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
