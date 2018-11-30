#!/usr/bin/env python
import os
import random

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


class Capital:
    def __init__(self, capital, country, image):
        self.capital = capital
        self.country = country
        self.image = image


def setup_data():
    lj = Capital(capital="Ljubljana", country="Slovenia", image="/assets/img/city1.jpg")
    zg = Capital(capital="Zagreb", country="Croatia", image="/assets/img/city2.jpg")
    w = Capital(capital="Vienna", country="Austria", image="/assets/img/city3.jpg")
    rm = Capital(capital="Rome", country="Italy", image="/assets/img/city4.jpg")
    be = Capital(capital="Berlin", country="Germany", image="/assets/img/city5.jpg")

    return [lj, zg, w, rm, be]


class MainHandler(BaseHandler):
    def get(self):
        capital = setup_data()[random.randint(0, 4)]  # get random capital from the list

        params = {"capital": capital}

        return self.render_template("main.html", params=params)


class ResultHandler(BaseHandler):
    def post(self):
        answer = self.request.get("answer")
        country = self.request.get("country")

        capitals = setup_data()
        for item in capitals:
            if item.country == country:
                if item.capital.lower() == answer.lower():
                    result = True
                else:
                    result = False

                params = {"result": result, "item": item}

                return self.render_template("result.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
], debug=True)
