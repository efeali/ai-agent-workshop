import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

class EmailManager:
    def __init__(self):
        load_dotenv()

        self.host = os.getenv('EMAIL_HOST')
        self.port = int(os.getenv('EMAIL_PORT'))
        self.user = os.getenv('EMAIL_USER')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.from_email = os.getenv('EMAIL_FROM')
        self.to_email = os.getenv('EMAIL_TO')

    def send_email(self, subject, body):
        """Send a simple email with the given subject and body"""
        try:


            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.host, self.port,timeout=30, context=context) as server:
                print(f"Connected to the server, logging in")
                server.login(self.user, self.password)
                print(f"Sending the email")
                server.send_message(msg)

            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_reminder(self, todos):
        """Send email reminder for upcoming todos"""
        if not todos:
            return

        try:

            subject = "Todo Reminder - Tasks Due Soon"

            body = "Hello! You have the following tasks due within the next 24 hours:\n\n"

            for todo in todos:
                body += f"• {todo['task']}\n"
                body += f"  Description: {todo['description']}\n"
                body += f"  Due: {todo['due_date']} at {todo['due_time']}\n\n"

            body += "Don't forget to complete them on time!\n\nBest regards,\nYour AI Todo Assistant"

            if self.send_email(subject,body):
                print(f"Reminder email sent successfully for {len(todos)} todos")
            else:
                print("Failed to send reminder email")

        except Exception as e:
            print(f"Error sending email: {e}")
