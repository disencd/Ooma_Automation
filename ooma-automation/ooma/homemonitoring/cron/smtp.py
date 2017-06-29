import smtplib
from time import gmtime, strftime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

'''
    Email Class - sending report
'''
class SmtpEmail():
    def __init__(self):
        pass

    def send_emails(self, emails, schedule):

        # Connect to the smtp server
        # self.server = smtplib.SMTP('smtp.gmail.com', '587')
        self.server = smtplib.SMTP('smtp.gmail.com', '587')
        # Start TLS encryption
        self.server.starttls()

        _from_email = 'disencd@gmail.com'
        self.server.login(_from_email, 'Cdd1@ges')



        # Send to entire email list
        for to_email, _name in emails.items():

            # Create message container - the correct MIME type is multipart/alternative here!
            message = MIMEMultipart('alternative')

            message['subject'] = 'Subject: HomeSecurity Smoketest Status@ ' + \
                        strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n'
            message['To'] = to_email
            message['From'] = _from_email
            message.preamble = """
                    Your mail reader does not support the report format.
                    Please visit us <a href="http://www.mysite.com">online</a>!"""

            hi_message = "Hi " + _name + "!\n\n Please find the below execution report:\n\n"

            # Record the MIME type text/html.
            text_body = MIMEText(hi_message, 'plain')
            html_body = MIMEText(schedule, 'html')


            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            message.attach(text_body)
            message.attach(html_body)

            self.server.sendmail(_from_email, to_email, message.as_string())

        self.server.quit()
