import smtplib, ssl
from scripts.config import PASSWORD


def send_deposit_update(balance, tx, health):
    port = 465  # For SSL
    email = "principalcomponents10@gmail.com"
    password = PASSWORD


    sender_email = email
    receiver_email = "aaron.w.barlow@gmail.com"

    this = 'test string'
    message = f"""\
    Subject: Deposit Made

    You had a WETH Balance of: {balance}


    It was deposited with this transaction:

    {tx}
    
    Your health factor is:
    {health}
    """

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(sender_email, receiver_email, message)
    return 0

def send_message(message):
    port = 465  # For SSL
    email = "principalcomponents10@gmail.com"
    password = PASSWORD

    sender_email = email
    receiver_email = "aaron.w.barlow@gmail.com"

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(sender_email, receiver_email, message)
    return 0