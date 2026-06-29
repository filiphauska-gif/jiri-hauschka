from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import mimetypes

mimetypes.add_type('model/vnd.usdz+zip', '.usdz')
mimetypes.add_type('model/gltf-binary', '.glb')

class Handler(SimpleHTTPRequestHandler):
    extensions_map = SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map.update({
        '.usdz': 'model/vnd.usdz+zip',
        '.glb': 'model/gltf-binary',
        '.js': 'text/javascript',
    })

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        super().end_headers()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', '4000'))
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print(f'Serving static site on http://127.0.0.1:{port}/', flush=True)
    try:
        with server:
            server.serve_forever()
    except KeyboardInterrupt:
        pass
