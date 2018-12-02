import os
import webapp2


# handlers
class MainHandler(webapp2.RequestHandler):
    def get(self):
        return self.response.write('Hello, SmartNinja!')


# URLs
app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    # to see the fakebook.html, add /templates/fakebook.html to your URL
], debug=True)


# run on server
localhost = True  # True: non-GAE localhost server; False: GAE on either localhost or on Google Cloud
if localhost:
    def main():
        from paste import httpserver
        from paste.cascade import Cascade
        from paste.urlparser import StaticURLParser

        assets_dir = os.path.join(os.path.dirname(__file__))
        static_app = StaticURLParser(directory=assets_dir)

        web_app = Cascade([app, static_app])
        httpserver.serve(web_app, host='localhost', port='8080')


    if __name__ == '__main__':
        main()
