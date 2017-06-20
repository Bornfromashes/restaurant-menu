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
#Create
            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output= "<html> <body>"
                output+="<h2>Make a new restaurant</h2>"
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/new' >"
                output += "<input name = 'newRestaurantName'  type='text' placeholder = 'myRestaurantName' ><br><br>"
                output += "<input type = 'submit' value = 'Create'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                return


#Read
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output= " "
                output= " <html><body>"
                output+="<a href= '/restaurants/new'>Create New Restaurant</a>"
                output+= "<br>"
                query1= session.query(Restaurant).all()
                for x in query1:
                    output+= x.name +"<br>"
                    output += "<a href ='/restaurants/%s/menuitems' >See Menu </a> " % x.id
                    output += "</br>"
                    output += "<a href ='/restaurants/%s/edit' >Edit </a> " % x.id
                    output += "</br>"
                    output += "<a href ='/restaurants/%s/delete' >Delete </a> " % x.id
                    output += "</br><br><br>"
                output+="</body></html>"
                self.wfile.write(output.encode())
                print (output)
                return
#menuitems
            if self.path.endswith("/menuitems"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resid= self.path.split("/")[2]
                output= " "
                output= " <html><body>"
                output+="MENU ITEMS"
                output+= "<br><br><br>"
                query1= session.query(MenuItem).filter_by(restaurant_id= resid).all()
                for x in query1:
                    output+= x.name
                    output+= "<br><br>"
                output+="</body></html>"
                self.wfile.write(output.encode())
                print (output)
                return
#Update
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resid= self.path.split("/")[2]
                query2= session.query(Restaurant).filter_by(id= resid).one()
                output = "<html><body>"
                output += "<h1>"
                output += query2.name
                output += "</h1>"
                output += "<a href ='/restaurants/%s/editname' >Rename Restaurant </a> " % query2.id
                output += "<br> <br>"
                output += "<a href ='/restaurants/%s/menu' >Add Items in menu </a> " % query2.id
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
#updating name
            if self.path.endswith("/editname"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resid= self.path.split("/")[2]
                query2= session.query(Restaurant).filter_by(id= resid).one()
                output = "<html><body>"
                output += "<h1>"
                output += query2.name
                output += "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/editname' >" % resid
                output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % query2.name
                output += "<input type = 'submit' value = 'Rename'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
#adding MenuItem
            if self.path.endswith("/menu"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resid= self.path.split("/")[2]
                query2= session.query(Restaurant).filter_by(id= resid).one()
                output = "<html><body>"
                output += "<h1>"
                output += "Add menu items to " + query2.name
                output += "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/menu' >" % resid
                output += "<input name = 'name' type='text' placeholder = 'Name' >"
                output += "<input name = 'description' type='text' placeholder = 'Description' >"
                output += "<input name = 'price' type='text' placeholder = 'Price' >"
                output += "<input name = 'course' type='text' placeholder = 'Course' >"
                output += "<input type = 'submit' value = 'Add'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return
#delete
            if self.path.endswith("/delete"):
                resid= self.path.split("/")[2]
                rest= session.query(Restaurant).filter_by(id= resid).one()
                session.delete(rest)
                session.commit()
                self.send_response(300)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()






        except IOError:
            self.send_error(404,"File not found %s"%self.path)

    def do_POST(self):
        #Creating new restaurant
        if self.path.endswith("/new"):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            pdict['boundary']= bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields= cgi.parse_multipart(self.rfile, pdict)
                messagecontent= fields.get('newRestaurantName')
                New = Restaurant(name= messagecontent[0].decode("utf-8"))
                session.add(New)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
        #updating name
        if self.path.endswith("/editname"):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                    myRestaurantQuery.name = messagecontent[0].decode("utf-8")
                    session.add(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        #adding menu items
        if self.path.endswith("/menu"):
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            pdict['boundary']= bytes(pdict['boundary'], "utf-8")
            restaurantIDPath = self.path.split("/")[2]
            res= session.query(Restaurant).filter_by(id= restaurantIDPath).one()
            if ctype == 'multipart/form-data':
                fields= cgi.parse_multipart(self.rfile, pdict)
                messagecontent= fields.get('name')
                messagecontent1= fields.get('description')
                messagecontent2= fields.get('price')
                messagecontent3= fields.get('course')
                New = MenuItem(name=messagecontent[0].decode("utf-8"), description= messagecontent1[0].decode("utf-8"), price= messagecontent2[0].decode("utf-8"), course= messagecontent3[0].decode("utf-8"), restaurant=Restaurant(name =res.name))
                session.add(New)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

def main():
    try:
        port= 8080
        server= HTTPServer(('', port), webServerHandler)
        print("web server running on port %s " %port)
        server.serve_forever()

    except KeyboardInterrupt:
        print ("Fuck off")
        server.socket.close()

if __name__ == '__main__':
    main()
