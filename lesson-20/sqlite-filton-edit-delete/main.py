#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Message, create_tables

from paste import httpserver
from paste.cascade import Cascade
from paste.urlparser import StaticURLParser


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
        return self.render_template("main.html")


class GuestbookHandler(BaseHandler):
    def get(self):
        messages = Message.select().where(Message.deleted == False)

        params = {"messages": messages}

        return self.render_template("guestbook.html", params=params)

    def post(self):
        author = self.request.get("name")
        email = self.request.get("email")
        message = self.request.get("message")

        if not author:
            author = "Anonymous"

        message = Message(author_name=author, email=email, message=message.replace("<script>", ""))
        message.save()

        return self.redirect_to("guestbook-site")  # see name in route


class MessageEditHandler(BaseHandler):
    def get(self, message_id):
        message = Message.select().where(Message.id == int(message_id)).get()

        params = {"message": message}

        return self.render_template("message_edit.html", params=params)

    def post(self, message_id):
        message = Message.select().where(Message.id == int(message_id)).get()

        text = self.request.get("message")
        message.message = text
        message.save()

        return self.redirect_to("guestbook-site")


class MessageDeleteHandler(BaseHandler):
    def get(self, message_id):
        message = Message.select().where(Message.id == int(message_id)).get()

        params = {"message": message}

        return self.render_template("message_delete.html", params=params)

    def post(self, message_id):
        message = Message.select().where(Message.id == int(message_id)).get()

        message.deleted = True  # fake delete
        message.save()

        return self.redirect_to("guestbook-site")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/guestbook', GuestbookHandler, name="guestbook-site"),
    webapp2.Route('/message/<message_id:\d+>/edit', MessageEditHandler, name="message-edit"),
    webapp2.Route('/message/<message_id:\d+>/delete', MessageDeleteHandler, name="message-delete"),
], debug=True)


def main():
    assets_dir = os.path.join(os.path.dirname(__file__))
    static_app = StaticURLParser(directory=assets_dir)

    web_app = Cascade([app, static_app])
    httpserver.serve(web_app, host='localhost', port='8080')


if __name__ == '__main__':
    create_tables()
    main()
