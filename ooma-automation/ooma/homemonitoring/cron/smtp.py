import smtplib

def send_emails(emails, schedule):
    # Connect to the smtp server
    server = smtplib.SMTP('smtp.gmail.com', '587')

    # Start TLS encryption
    server.starttls()

    # Login
    password = input("What's your password?")
    from_email = 'disen@ooma.com'
    server.login(from_email, password)

    # Send to entire email list
    for to_email, name in emails.items():
        message = 'Subject: Beagle Bone Automation Status!\n'
        message += 'Hi ' + name + '!\n\n'
        message += "Today's Performance Schedule:"
        message += schedule + '\n\n'
        message += 'Hope to see you there!'
        server.sendmail(from_email, to_email, message)

    server.quit()
