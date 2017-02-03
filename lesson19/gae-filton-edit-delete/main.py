#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Message


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
        messages = Message.query(Message.deleted == False).fetch()

        params = {"messages": messages}

        return self.render_template("guestbook.html", params=params)

    def post(self):
        author = self.request.get("name")
        email = self.request.get("email")
        message = self.request.get("message")

        if not author:
            author = "Anonymous"

        if "<script>" in message:  # One way to fight JS injection
            return self.write("Can't hack me! Na na na na :)")

        msg_object = Message(author_name=author, email=email, message=message.replace("<script>", ""))  # another way to fight JS injection
        msg_object.put()  # save message into database

        return self.redirect_to("guestbook-site")  # see name in route


class MessageEditHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))

        params = {"message": message}

        return self.render_template("message_edit.html", params=params)

    def post(self, message_id):
        message = Message.get_by_id(int(message_id))

        text = self.request.get("message")
        message.message = text
        message.put()

        return self.redirect_to("guestbook-site")


class MessageDeleteHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))

        params = {"message": message}

        return self.render_template("message_delete.html", params=params)

    def post(self, message_id):
        message = Message.get_by_id(int(message_id))

        message.deleted = True  # fake delete
        message.put()

        return self.redirect_to("guestbook-site")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/guestbook', GuestbookHandler, name="guestbook-site"),
    webapp2.Route('/message/<message_id:\d+>/edit', MessageEditHandler, name="message-edit"),
    webapp2.Route('/message/<message_id:\d+>/delete', MessageDeleteHandler, name="message-delete"),
], debug=True)
