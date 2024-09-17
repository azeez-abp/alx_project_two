#!/usse/bin/pythom3
""""Module for sending email
    smtplib is in0built pyhton libarary
"""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="email_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class EmailService:
    """Service for sending HTML emails."""

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    def __init__(self, from_email: str, from_email_password: str):
        self.from_email = from_email
        self.from_email_password = from_email_password

    def send_html_email(self, subject: str, html_body: str, to_email: str) -> bool:
        """
        Send an HTML email using SMTP.

        Args:
            subject (str): Subject of the email.
            html_body (str): HTML body of the email.
            to_email (str): Recipient's email address.
        """
        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach the HTML body to the email
        msg.attach(MIMEText(html_body, "html"))

        try:
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(self.from_email, self.from_email_password)
                server.sendmail(self.from_email, to_email, msg.as_string())
                logging.info(f"HTML email sent successfully to {to_email}")
                return True
        except smtplib.SMTPAuthenticationError:
            logging.error(
                "Authentication failed.\
                          Check your email or password."
            )
            return False
        except smtplib.SMTPConnectError:
            logging.error("Failed to connect to the SMTP server.")
            raise
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            raise


# Usage Example
# if __name__ == "__main__":
#     # Fetch sensitive info from environment variables
#     FROM_EMAIL = os.getenv('FROM_EMAIL')
#     FROM_EMAIL_PASSWORD = os.getenv('FROM_EMAIL_PASSWORD')

#     if not FROM_EMAIL or not FROM_EMAIL_PASSWORD:
#         logging.error("Email credentials are not set in \
# the environment variables.")
#         raise EnvironmentError("Missing email credentials in \
# environment variables.")

#     email_service = EmailService(from_email=FROM_EMAIL,
# from_email_password=FROM_EMAIL_PASSWORD)

#     try:
#         email_service.send_html_email(
#             subject="HTML Test Email",
#             html_body="<h1>This is a test email with HTML!</h1>",
#             to_email="recipient@example.com"
#         )
#     except Exception as e:
#         logging.error(f"Error occurred while sending email: {e}")
