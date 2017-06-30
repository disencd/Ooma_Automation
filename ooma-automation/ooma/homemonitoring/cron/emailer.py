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
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.html_file = self.abs_path + '/../setup/report.html'
        self._filename = self.abs_path + '/emails.txt'

    def get_emails(self):
        # Reading emails from a file
        emails = {}

        try:
            email_file = open(self._filename, 'r')

            for line in email_file:
                (email, name) = line.split(',')
                emails[email] = name.strip()

        except FileNotFoundError as err:
            print(err)

        return emails

    def construct_report(self, sl_no, testcase, result):
        html_str = "<TR><TD>" + str(sl_no) + "</TD>" \
                   "<TD>" + testcase + "</TD> " \
                   "<TD>" + result + "</TD></TR>"

        return html_str

    def report_generator(self, log):
        result_list = ""
        result = "Result :"
        _cnt = 1
        try:
            with open(log) as fh:
                for line in fh:
                    if result in line:

                        index = line.find(result)
                        index += len(result)
                        # result_str += line[index:] + '\n'
                        str = line[index:]
                        val = str.split(' -')
                        result_list += self.construct_report(_cnt, val[0], val[1])
                        _cnt += 1
        except:
            print("Unexpected error:", sys.exc_info()[0])

        if not result_list:
            sys.exit()

        return result_list

    def process_html_result(self, result):

        with open(self.html_file) as fh:
            data = fh.read().replace('@outputstring', result)

        fh.close()

        return data

    def get_report_card(self):
        # Reading our schedule from a file
        try:
            report_result = self.report_generator('/tmp/listener.log')

            final_output = self.process_html_result(report_result)

        except FileNotFoundError as err:
            print(err)

        return final_output

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
