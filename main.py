import webapp2

from emailsender import EmailSender
from subscribe import SubscribeHandler

app = webapp2.WSGIApplication(
    [('/', SubscribeHandler),
    ('/email', EmailSender)],
    debug=True
)
