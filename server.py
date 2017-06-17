from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output= " "
                query1= session.query(Restaurant).all()
                for x in query1:
                    output+= x.name + "<br>"

                self.wfile.write(output.encode())
                print (output)
                return
        except IOError:
            self.send_error(404,"File not found %s"%self.path)

def main():
    try:
        port= 8080
        server= HTTPServer(('', port), webServerHandler)
        print("web server running on port %s " %port)
        server.serve_forever()

    except KeyboardInterrupt:
        print ("^C entered, stopping web server ....")
        server.socket.close()

if __name__ == '__main__':
    main()
