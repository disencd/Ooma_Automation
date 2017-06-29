import smtp
import sys, os
import re

'''
Send a greeting email to our customer email list
with the daily weather forecast and schedule
'''


def get_emails():
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


def report_generator(log):
    result_list = []
    result = re.compile('(Result :)+([\w\d.])', re.UNICODE)
    with open(log) as fh:
        for line in fh:
            match = result.search(line)
            if match:
                print(line)
                result_list.append(line)

    return line

def get_schedule():
    # Reading our schedule from a file
    try:
        # schedule_file = open('/tmp/listener.log', 'r')
        #
        # schedule = schedule_file.read()

        schedule = report_generator('/tmp/listener.log')
    except FileNotFoundError as err:
        print(err)

    return schedule


def main():
    # Get our dictionary of customer emails and names
    emails = get_emails()

    # Get our daily performance schedule
    schedule = get_schedule()

    # Send emails to all of our customers with schedule
    smtp.send_emails(emails, schedule)


main()
