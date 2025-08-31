from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse as urlparse
from agent import ReActAgent, get_weather


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_res(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        json_data = json.dumps(response, ensure_ascii=False)
        self.wfile.write(json_data.encode("utf-8"))

    def _handle_req(self, api: str, params: dict):
        if api == "/":
            self._send_res({"message": "Hello from [ai-langchain]!"})
        elif api == "/api/agent":
            if "query" in params:
                query = str(params["query"])
                agent = ReActAgent()
                agent.add_tool_func(get_weather)
                agent.compile(display_graph=True)
                message = agent.invoke(query)
                self._send_res(
                    {
                        "message": message,
                    }
                )
            else:
                self._send_res({"error": "Missing query parameter"}, status=400)
        else:
            self._send_res({"error": "Not Found"}, status=404)

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        api = parsed_path.path
        query_params = urlparse.parse_qs(parsed_path.query)
        params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}

        self._handle_req(api, params)

    def do_POST(self):
        parsed_path = urlparse.urlparse(self.path)
        api = parsed_path.path
        query_params = urlparse.parse_qs(parsed_path.query)
        params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}

        # 文字太长时用body传参
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            post_data = self.rfile.read(content_length)
            try:
                json_data = json.loads(post_data.decode("utf-8"))
                params.update(json_data)
            except json.JSONDecodeError:
                print(f"POST 错误：body不是json格式 {post_data}", flush=True)

        self._handle_req(api, params)


def main():
    server_address = ("", 5002)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("[ai-langchain] running on http://localhost:5002")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
