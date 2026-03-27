import os
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, urlparse

class CustomHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query, keep_blank_values=True)
        content_type = query.get("q", ["text/plain; charset=utf-8"])[0]
        fetch_site = self.headers.get("Sec-Fetch-Site", "none").lower()
        fetch_mode = self.headers.get("Sec-Fetch-Mode", "navigate").lower()
        fetch_dest = self.headers.get("Sec-Fetch-Dest", "document").lower()

        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        flag_cookie = cookie["FLAG"].value if "FLAG" in cookie else None
        body = (flag_cookie or "Hello ENKI").encode()

        self.close_connection = True
        self.send_response(HTTPStatus.OK)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Vary", "Sec-Fetch-Site, Sec-Fetch-Mode, Sec-Fetch-Dest")
        if fetch_site == "none"\
            and fetch_mode == "navigate"\
            and fetch_dest == "document":
            self.send_header("Content-Length", 0)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(body)

if __name__ == "__main__":
    with ThreadingHTTPServer(("0.0.0.0", 3000), CustomHandler) as httpd:
        httpd.serve_forever()