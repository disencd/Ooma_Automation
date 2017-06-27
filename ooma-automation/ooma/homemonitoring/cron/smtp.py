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
        message = 'Subject: Beagle Bone Automation Status @ ' + \
                    strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n'

        message += 'Hi ' + name + '!\n\n'
        message += "Today's Performance Schedule:\n\n"
        message += schedule + '\n\n'
        message += 'Hope to see you there!'
        server.sendmail(from_email, to_email, message)

    server.quit()
