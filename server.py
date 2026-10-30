"""Server locale per Offline Character Chat.
Serve la pagina e inoltra SOLO /api/chat, /api/tags e /api/show a Ollama (localhost:11434).
Uso: python server.py [--lan] [porta]   (--lan = raggiungibile dalla rete di casa)"""
import http.client, os, socket, socketserver, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = 'offline-character-chat.html'
OLLAMA = ('127.0.0.1', 11434)
ALLOW = {('GET', '/api/tags'), ('POST', '/api/chat'), ('POST', '/api/show')}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send_all(self, code, body=b'', ctype='text/plain; charset=utf-8'):
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split('?')[0]
        if path in ('/', '/' + PAGE):
            with open(os.path.join(HERE, PAGE), 'rb') as f:
                self.send_all(200, f.read(), 'text/html; charset=utf-8')
        elif ('GET', path) in ALLOW:
            self.proxy(None, path)
        else:
            self.send_all(404, b'Not found')

    def do_POST(self):
        path = self.path.split('?')[0]
        body = self.rfile.read(int(self.headers.get('Content-Length') or 0))
        if ('POST', path) in ALLOW:
            self.proxy(body, path)
        else:
            self.send_all(404, b'Not found')

    def proxy(self, body, path):
        c = None
        try:
            c = http.client.HTTPConnection(*OLLAMA, timeout=900)
            c.request(self.command, path, body=body, headers={'Content-Type': 'application/json'} if body is not None else {})
            r = c.getresponse()
        except OSError:
            if c: c.close()
            return self.send_all(502, b'{"error":"Ollama non raggiungibile su localhost:11434"}', 'application/json')
        try:
            self.send_response(r.status)
            self.send_header('Content-Type', r.getheader('Content-Type', 'application/json'))
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            while True:
                chunk = r.read1(8192)
                if not chunk: break
                self.wfile.write(chunk)
                self.wfile.flush()
        except (OSError, ValueError):
            pass  # il browser ha chiuso (Stop): chiudere Ollama sotto ferma la generazione
        finally:
            c.close()

class Srv(ThreadingHTTPServer):
    def server_bind(self):
        # Non fa la ricerca DNS inversa del nome host (rallenta o si blocca senza internet).
        socketserver.TCPServer.server_bind(self)
        self.server_name, self.server_port = self.server_address[:2]

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()

if __name__ == '__main__':
    args = sys.argv[1:]
    lan = '--lan' in args
    nums = [a for a in args if a.isdigit()]
    port = int(nums[0]) if nums else 8000
    try:
        srv = Srv(('0.0.0.0' if lan else '127.0.0.1', port), H)
    except OSError as e:
        print('Impossibile avviare il server sulla porta %d: %s' % (port, e))
        sys.exit(1)
    print('Offline Character Chat')
    print('  Sul PC:        http://localhost:%d/' % port)
    if lan:
        ip = lan_ip()
        print('  Dal telefono:  http://%s:%d/   (stessa rete Wi-Fi)' % (ip, port))
        if ip == '127.0.0.1':
            print('  ATTENZIONE: non trovo una rete. Collega PC e telefono allo stesso Wi-Fi (va bene anche senza internet).')
    print('Ollama deve essere acceso su questo PC. Ctrl+C per fermare.')
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
