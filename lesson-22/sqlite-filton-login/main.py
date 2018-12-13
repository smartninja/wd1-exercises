#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Message, create_tables
from requests_oauthlib import OAuth2Session
from secrets import get_client_id, get_client_secret  # rename the secrets_template.py file into secrets.py

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
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # needed to run oAuth locally. Delete this line in production!

        if not params:
            params = {}

        # check if user is logged in via GutHub
        token = self.request.cookies.get("oauth_access_token")
        token_type = self.request.cookies.get("oauth_token_type")

        if token and token_type:
            github = OAuth2Session(get_client_id(), token={"access_token": token, "token_type": token_type})
            user = github.get('https://api.github.com/user')

            params["user"] = user.json()

        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")


class LoginHandler(BaseHandler):
    def get(self):
        # get authorization from GitHub (start OAuth2)
        authorization_base_url = "https://github.com/login/oauth/authorize"

        github = OAuth2Session(get_client_id())
        authorization_url, state = github.authorization_url(authorization_base_url)

        # you'll need this cookie for callback
        self.response.set_cookie("oauth_state", value=state)

        return self.redirect(authorization_url)


class CallbackHandler(BaseHandler):
    def get(self):
        # receive authorization from GitHub (finish OAuth2)
        state = self.request.cookies.get("oauth_state")

        token_url = 'https://github.com/login/oauth/access_token'

        github = OAuth2Session(get_client_id(), state=state)
        token = github.fetch_token(token_url, client_secret=get_client_secret(), authorization_response=self.request.url)

        # github login cookies
        self.response.set_cookie("oauth_access_token", value=token["access_token"])
        self.response.set_cookie("oauth_token_type", value=token["token_type"])

        return self.redirect_to("main")


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


class DeletedMessagesHandler(BaseHandler):
    def get(self):
        messages = Message.select().where(Message.deleted == True)

        params = {"messages": messages}

        return self.render_template("deleted_messages.html", params=params)


class MessageRestoreHandler(BaseHandler):
    def get(self, message_id):
        message = Message.select().where(Message.id == int(message_id)).get()

        params = {"message": message}

        return self.render_template("message_restore.html", params=params)

    def post(self, message_id):
        message = Message.select().where(Message.id == int(message_id)).get()

        message.deleted = False
        message.save()

        return self.redirect_to("guestbook-site")


class MessageCompleteDeleteHandler(BaseHandler):
    def get(self, message_id):
        message = Message.select().where(Message.id == int(message_id)).get()

        params = {"message": message}

        return self.render_template("message_complete_delete.html", params=params)

    def post(self, message_id):
        message = Message.select().where(Message.id == int(message_id)).get()

        message.delete_instance()  # permanently deleting the message

        return self.redirect_to("deleted-messages")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main"),
    webapp2.Route('/login', LoginHandler, name="login"),
    webapp2.Route('/callback', CallbackHandler, name="callback"),
    webapp2.Route('/guestbook', GuestbookHandler, name="guestbook-site"),
    webapp2.Route('/message/<message_id:\d+>/edit', MessageEditHandler, name="message-edit"),
    webapp2.Route('/message/<message_id:\d+>/delete', MessageDeleteHandler, name="message-delete"),
    webapp2.Route('/message/<message_id:\d+>/restore', MessageRestoreHandler, name="message-restore"),
    webapp2.Route('/message/<message_id:\d+>/complete-delete', MessageCompleteDeleteHandler, name="message-complete-delete"),
    webapp2.Route('/deleted', DeletedMessagesHandler, name="deleted-messages"),
], debug=True)


def main():
    assets_dir = os.path.join(os.path.dirname(__file__))
    static_app = StaticURLParser(directory=assets_dir)

    web_app = Cascade([app, static_app])
    httpserver.serve(web_app, host='localhost', port='8080')


if __name__ == '__main__':
    create_tables()
    main()
