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
    result = "Result :"
    with open(log) as fh:
        for line in fh:
            if result in line:
                index = line.find(result)
                result_list.append(line)

    return result_list

def get_schedule():
    # Reading our schedule from a file
    try:
        schedule_file = open('/tmp/listener.log', 'r')

        #schedule = schedule_file.read()

        schedule1 = report_generator('/tmp/listener.log')
    except FileNotFoundError as err:
        print(err)

    return schedule1


def main():
    # Get our dictionary of customer emails and names
    emails = get_emails()

    # Get our daily performance schedule
    schedule = get_schedule()

    # Send emails to all of our customers with schedule
    smtp.send_emails(emails, schedule)


main()
