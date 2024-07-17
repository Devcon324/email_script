import webapp2

from emailsender import EmailSender
from google.appengine.ext import db


class SubscribeHandler(webapp2.RequestHandler):

  def post(self):
    user_id = self.request.get('user')

    # insert the subscription into the Datastore
    subscription = Subscription(user_id=user_id)
    subscription.put()

  def get(self):
    # retrieve up to 1000 subscriptions from the Datastore
    subscriptions = Subscription.all().fetch(1000)

    if not subscriptions:
      self.response.write('No subscriptions')
      return

    count = len(subscriptions)

    for s in subscriptions:
      self.response.write('%s subscribed<br/>' % (s.user_id))

    self.response.write('<br/>')
    self.response.write('%d subscriptions.' % (count))


class Subscription(db.Model):
    user_id = db.TextProperty(required=True)
