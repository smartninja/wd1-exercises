#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

    def post(self):
        secret = 22
        guess = int(self.request.get("guess"))

        result = None

        if secret == guess:
            result = "Your answer is correct! The secret number is 22."
        elif secret > guess:
            result = "Sorry, but your guess is to low. Try a bit higher."
        elif secret < guess:
            result = "Sorry, but your guess is to high. Try a bit lower."

        params = {"result": result}

        return self.render_template("result.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)


# run on localhost server
gae_env = True  # False: non-GAE localhost server; True: GAE on either localhost or on Google Cloud
if not gae_env:
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
