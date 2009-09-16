#!/usr/bin/env python

import tornado.web
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.auth
import os.path
import re
import markdown
import unicodedata

from tornado.options import define, options


define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="Google Group database host")
define("mysql_database", default="google_groups", help="Google Group database name")
define("mysql_user", default="root", help="Google Group database user")
define("mysql_password", default="root", help="Google Group database password")



class Application(tornado.web.Application):
    """Initial class that gets executed when the app starts
    """
    
    def __init__(self):
        """initialize the database with appropriate parameters configured.
        """
        
        handlers = [
            (r"/", HomeHandler),
            (r"/([^/]+)", GroupHandler),
            (r"/([^/]+)/discussion", DiscussionPageHandler),
            (r"/([^/]+)/discussion/([^/]+)", DiscussionHandler),
            (r"/([^/]+)/members", MemberPageHandler),
            (r"/([^/]+)/members/([^/]+)", MemberHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
        ]
        settings = dict(
            product_title=u"PaGaL Groups",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    # def get_current_user(self):
    #     user_id = self.get_secure_cookie("user")
    #     if not user_id: return None
    #     return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))


class HomeHandler(BaseHandler):
    """Home Page handler. Is made of part discussions by using a UI module
    """
    
    def get(self):
        """ handles the get request for '/' url
        """
        groups = self.db.query("SELECT * FROM `group`")
        self.render("home.html", groups=groups)

class GroupHandler(tornado.web.RequestHandler):
    """this is responsible for taking you to the group
    if the user is permitted to view the group
    """
    def get(self,group_name):
        permission = self.db.execute("SELECT `group_visibility` FROM `group` WHERE `group_visibility`=" + group_name)
    
    def __init__(self):
        """
        """

class DiscussionPageHandler(tornado.web.RequestHandler):
    """responsible for showing all the discussion indexes
    through appropriate pagination.
    """
    
    def __init__(self ):
        """
        """
        
        

class DiscussionHandler(tornado.web.RequestHandler):
    """responsible for handling the individual discussion
    pages that shows the discussion continuation flow.
    """
    
    def __init__(self):
        """
        """
        
        

class MemberPageHandler(tornado.web.RequestHandler):
    """responsible for showing all the member indexes
    through appropriate pagination if the user is 
    authorized to view it.
    """
    
    def __init__(self):
        """
        """
        
        

class MemberHandler(tornado.web.RequestHandler):
    """responsible for showing the profile of the individual
    members of the group through pagination if the person is
    authorized to view it.
    """
    
    def __init__(self):
        """
        """
        
        


class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        self.write("login")

    #     if self.get_argument("openid.mode", None):
    #         self.get_authenticated_user(self.async_callback(self._on_auth))
    #         return
    #     self.authenticate_redirect()
    
    # def _on_auth(self, user):
    #     if not user:
    #         raise tornado.web.HTTPError(500, "Google auth failed")
    #     author = self.db.get("SELECT * FROM authors WHERE email = %s",
    #                          user["email"])
    #     if not author:
    #         # Auto-create first author
    #         any_author = self.db.get("SELECT * FROM authors LIMIT 1")
    #         if not any_author:
    #             author_id = self.db.execute(
    #                 "INSERT INTO authors (email,name) VALUES (%s,%s)",
    #                 user["email"], user["name"])
    #         else:
    #             self.redirect("/")
    #             return
    #     else:
    #         author_id = author["id"]
    #     self.set_secure_cookie("user", str(author_id))
    #     self.redirect(self.get_argument("next", "/"))


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.write('logout')

        # self.clear_cookie("user")
        # self.redirect(self.get_argument("next", "/"))




def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
