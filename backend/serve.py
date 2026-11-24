from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from mimetypes import guess_type
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit
from os import environ

from frontend.page import CATEGORY_KEYS, IMAGE_NAMES, render_coat, render_home




IMAGE_FOLDER = Path(__file__).resolve().parents[1] / "frontend" / "images"
PORT = int(environ.get("PORT", "8001"))



class PromoHandler(BaseHTTPRequestHandler):
   def do_GET(self):
       url = urlsplit(self.path)


       if url.path == "/":
           options = parse_qs(url.query)
           show_preview = options.get("show") == ["preview"]
           query = options.get("q", [""])[0].strip()[:80]
           category = options.get("category", ["all"])[0]


           if category not in CATEGORY_KEYS:
               category = "all"


           self.send_page(render_home(show_preview, query, category))
           return


       if url.path == "/coat":
           self.send_page(render_coat())
           return


       directory, _, encoded_filename = url.path.rpartition("/")
       filename = unquote(encoded_filename)


       if directory != "/images" or filename not in IMAGE_NAMES:
           self.send_error(404)
           return


       try:
           image = (IMAGE_FOLDER / filename).read_bytes()
       except FileNotFoundError:
           self.send_error(404, "Image file not found")
           return


       content_type = guess_type(filename)[0] or "application/octet-stream"
       self.send_content(image, content_type)


   def send_page(self, page):
       self.send_content(page.encode("utf-8"), "text/html; charset=utf-8")


   def send_content(self, content, content_type):
       self.send_response(200)
       self.send_header("Content-Type", content_type)
       self.send_header("Content-Length", str(len(content)))
       self.end_headers()
       self.wfile.write(content)




if __name__ == "__main__":
   with ThreadingHTTPServer(("0.0.0.0", PORT), PromoHandler) as server:
       print(f"Open http://localhost:{PORT}/")
       try:
           server.serve_forever()
       except KeyboardInterrupt:
           pass
