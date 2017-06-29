import smtplib
from time import gmtime, strftime

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
            message = 'Subject: HomeSecurity Smoketest Status @ ' + \
                        strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n'

            message += 'Hi ' + _name + '!\n\n'
            message += "Please find the below execution report:\n\n"
            message += str(schedule) + '\n\n'
            message += 'Thanks for looking into it....'
            self.server.sendmail(_from_email, to_email, message)

        self.server.quit()
