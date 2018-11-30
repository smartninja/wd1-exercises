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


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")


class LotteryResult(BaseHandler):
    def get(self):
        numbers = generate_lottery_numbers(8)

        params = {"numbers": numbers}

        return self.render_template("lottery.html", params=params)


def generate_lottery_numbers(quantity):
    """The same function that we had in lesson 10."""
    num_list = []

    while True:
        if len(num_list) == quantity:  # when the length of the list reaches the desired quantity, stop choosing new numbers
            break

        lot_num = random.randint(1, 50)

        if lot_num not in num_list:  # if the chosen number is not in the list yet, add it to it (this helps avoiding duplicates)
            num_list.append(lot_num)

    return num_list

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/lottery', LotteryResult),
], debug=True)
