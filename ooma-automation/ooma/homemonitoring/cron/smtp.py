import smtplib
from time import gmtime, strftime

def send_emails(emails, schedule):
    # Connect to the smtp server
    #server = smtplib.SMTP('smtp.gmail.com', '587')
    server = smtplib.SMTP('smtp.gmail.com', '587')

    # Start TLS encryption
    server.starttls()

    # Login
    #password = input("What's your password?")
    from_email = 'disencd@gmail.com'
    server.login(from_email, 'Cdd1@ges')

    # Send to entire email list
    for to_email, name in emails.items():
        message = 'Subject: HomeSecurity Smoketest Status @ ' + \
                    strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n'

        message += 'Hi ' + name + '!\n\n'
        message += "Please find the below execution report:\n\n"
        message += str(schedule) + '\n\n'
        message += 'Thanks for looking into it....'
        server.sendmail(from_email, to_email, message)

    server.quit()
