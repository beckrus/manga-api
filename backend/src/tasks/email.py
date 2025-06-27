from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape
import logging
import smtplib

from src.config import settings
from src.tasks.celery import celery_app


def check_smtp_settings() -> bool:
    if all(settings.SMTP_USER, settings.SMTP_PASS, settings.SMTP_USER, settings.SMTP_PASS):
        return True
    return False


@celery_app.task(bind=True, retry_kwargs={"max_retries": 5})
def send_welcome_email_task(self, user: dict):
    if not check_smtp_settings:
        return "❌ SMTP is not configured"
    try:
        logging.info("✅ Preparing Welcome email template...")
        env = Environment(
            loader=FileSystemLoader("templates"), autoescape=select_autoescape(["html", "xml"])
        )
        template = env.get_template("email/welcome_email.html")
        html = template.render(
            username=user["username"], site_url=settings.SITE_URL, site_name=settings.SITE_NAME
        )

        return send_email_task(user["email"], "Weclome!", html)
    except OSError as e:
        if e.errno == 101:
            logging.error(f"❌ Network is unreachable, check SMTP_HOST and SMTP_PORT!: {e}")
            raise self.retry(exc=e, countdown=60)
        else:
            logging.error(f"❌ OSError occurred: {e}")
            raise e
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"❌ SMTP Authentication failed, check username and password!: {e}")
        raise self.retry(exc=e, countdown=60 * 60)
    except Exception as e:
        logging.error(f"❌ Failed to send email for {user['email']}: {e}")
        raise self.retry(exc=e, countdown=60)


def send_email_task(to_email: str, subject: str, message: str):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg.attach(MIMEText(message, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
        smtp.sendmail(msg["From"], msg["To"], msg.as_string())
        return f"✅ Email to {to_email} with subject {subject} sent successfully!"
