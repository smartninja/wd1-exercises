import os
import webapp2
from paste import httpserver
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser


# handlers
class MainHandler(webapp2.RequestHandler):
    def get(self):
        return self.response.write('Hello, SmartNinja!')


# URLs
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)


# run the server
def main():
    assets_dir = os.path.join(os.path.dirname(__file__))
    static_app = StaticURLParser(directory=assets_dir)

    web_app = Cascade([app, static_app])
    httpserver.serve(web_app, host='localhost', port='8080')


if __name__ == '__main__':
    main()
