import jinja2
import os
import webapp2

from google.appengine.api import mail
from google.appengine.api import users

from urlparse import urlparse

class EmailSender(webapp2.RequestHandler):

  def get(self):
    # require users to be logged in to send emails
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return

    email = user.email()

    # The confirm url corresponds to the App Engine app url
    pr = urlparse(self.request.url)
    confirm_url = '%s://%s?user=%s' % (pr.scheme, pr.netloc, user.user_id())

    # load the email template and replace the placeholder with the confirm url
    jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    template = jinja_environment.get_template('mail_template.html')
    email_body = template.render({'confirm_url': confirm_url})

    message = mail.EmailMessage(
        sender = email,
        to = email,
        subject = 'Please confirm your subscription to Mailing-List XYZ',
        html = email_body)

    try:
      message.send()
      self.response.write('OK')
    except:
      self.error(500)
