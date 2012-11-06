import tornado.ioloop
import tornado.web
import os

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("webroot/templates/index.html") 

if __name__ == "__main__":
  settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "webroot"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies": True,
  }

  urls = [(r"/", MainHandler), ]
  application = tornado.web.Application(urls, **settings)
  application.listen(8988)
  tornado.ioloop.IOLoop.instance().start()
