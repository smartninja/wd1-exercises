#!/usr/bin/env python
import json
import os
import jinja2
import requests
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


class WeatherHandler(BaseHandler):
    def get(self):
        city = "London"
        units = "metric"
        app_key = "your-own-api-key-here"  # enter your own API key from OpenWeatherMap API (openweathermap.org/api)

        url = "http://api.openweathermap.org/data/2.5/weather?q={0}&units={1}&appid={2}".format(city, units, app_key)

        result = requests.get(url)

        weather_info = json.loads(result.text)

        params = {"weather_info": weather_info}

        return self.render_template("weather.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main"),
    webapp2.Route('/weather', WeatherHandler, name="weather"),
], debug=True)


# run on localhost server
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
