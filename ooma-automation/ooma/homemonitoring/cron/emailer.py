import smtp
import sys, os
import re
from smtp import SmtpEmail
'''
Send a greeting email to our customer email list
with the daily weather forecast and schedule
'''

class Emailer(object, SmtpEmail):
    def __init__(self):
        pass

    def get_emails(self):
        # Reading emails from a file
        emails = {}
        abs_path = os.path.dirname(os.path.abspath(__file__))
        filename = abs_path + '/emails.txt'

        try:
            email_file = open(filename, 'r')

            for line in email_file:
                (email, name) = line.split(',')
                emails[email] = name.strip()

        except FileNotFoundError as err:
            print(err)

        return emails


    def report_generator(self, log):
        result_list = ""
        result = "Result :"
        with open(log) as fh:
            for line in fh:
                if result in line:
                    index = line.find(result)
                    index += len(result)
                    result_list += line[index:] + '\n'

        return result_list

    def get_report_card(self):
        # Reading our schedule from a file
        try:
            report_card = self.report_generator('/tmp/listener.log')
        except FileNotFoundError as err:
            print(err)

        return report_card

    def send_report_card(self):
        # Get our dictionary of customer emails and names
        emails = self.get_emails()

        # Get our daily performance schedule
        schedule = self.get_report_card()

        super(Emailer, self).send_emails(emails, schedule)

def main():
    email_obj = Emailer()
    # Send emails to all of our customers with schedule
    email_obj.send_report_card()


main()
