
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
from_email = 'manyypallive@gmail.com',
to_emails = "prashantgoyal494@gmail.com",
subject = "Account Verification",
html_content ='<strong>and easy to do anywhere, even with Python</strong>')
print(message)


sg = SendGridAPIClient('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')
response = sg.send(message)