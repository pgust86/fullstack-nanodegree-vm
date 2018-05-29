from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## import CRUD Operations from Lesson 1 ##
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href="">EDIT</a></br>"
                    output += "<a href="">DELETE</a></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += '''<form method ='POST' enctype='multipart/form-data'
                    action='/restaurants/new' >'''
                output += '''<input name= 'newRestaurantName' type='text'
                    placeholder = 'New Restaurant Name' >'''
                output += "<input type= 'submit' value='Create'>"
                output += "</html></body>"
                self.wfile.write(output)
                return


            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += '''<form method = 'POST' enctype='multipart/form-data' action='/
                    hello'><h2>What would you like me to say?</h2><input name="message"
                    type="text" ><input type="submit" value = "Submit"></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "&#161Hola!"
                output += '''<form method = 'POST' enctype='multipart/form-data' action = '/
                    hello'><h2>What would you like me to say?</h2><input name="message"
                    type="text" ><input type="submit" value = "Submit"></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    #Create new Restaurant class
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type',    'text/html')
                    self.send_header('Location', 'restaurants')
                    self.end_headers()

                    return
            #self.send_response(301)
            #self.send_header('Content-type', 'text/html')
            #self.end_headers()
            #ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            #if ctype == 'multipart/form-data':
            #    fields = cgi.parse_multipart(self.rfile, pdict)
            #    messagecontent = fields.get('message')
            #output = ""
            #output += "<html><body>"
            #output += "<h2> Okay, how about this: </h2>"
            #output += "<h1> %s </h1>" % messagecontent[0]

            #output += '''<form method = 'POST' enctype='multipart/form-data' action = '/
            #    hello'><h2>What would you like me to say?</h2><input name='message'
            #    type='text' ><input type='submit' value = 'Submit'></form>'''
            #output += "</body></html>"
            #self.wfile.write(output)
            #print output

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webServerHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
