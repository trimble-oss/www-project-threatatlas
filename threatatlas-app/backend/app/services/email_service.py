"""Email service for sending invitation and notification emails."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import settings

logger = logging.getLogger(__name__)

# Setup Jinja2 template environment
template_dir = Path(__file__).parent.parent / "templates"
# nosemgrep: python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2
jinja_env = Environment(
    loader=FileSystemLoader(str(template_dir)),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailService:
    """Service for sending emails via SMTP."""

    @staticmethod
    def _get_role_display(role: str) -> str:
        """Get user-friendly role name."""
        role_names = {
            'admin': 'Administrator',
            'standard': 'Standard User',
            'read_only': 'Read-Only User'
        }
        return role_names.get(role, role.title())

    @staticmethod
    def _get_role_description(role: str) -> str:
        """Get role description."""
        descriptions = {
            'admin': 'Full access to all features and user management',
            'standard': 'Create and edit your own products and diagrams',
            'read_only': 'View-only access to all resources'
        }
        return descriptions.get(role, '')

    @staticmethod
    def _send_email(to_email: str, subject: str, html_body: str) -> bool:
        """
        Send an email via SMTP.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_body: HTML email body

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
            message["To"] = to_email
            message.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                if settings.smtp_tls:
                    server.starttls()
                if settings.smtp_username and settings.smtp_password:
                    server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(message)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    @staticmethod
    def send_invitation_email(email: str, token: str, inviter_name: str, role: str) -> bool:
        """
        Send an invitation email to a new user.

        Args:
            email: Recipient email address
            token: Unique invitation token
            inviter_name: Name of the user who sent the invitation
            role: Role the user will have (admin, standard, read_only)

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            template = jinja_env.get_template("invitation_email.html")
            # nosemgrep: python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2
            html_body = template.render(
                title="You're Invited to ThreatAtlas",
                invitation_url=f"{settings.frontend_url}/accept-invitation/{token}",
                inviter_name=inviter_name,
                role_display=EmailService._get_role_display(role),
                role_description=EmailService._get_role_description(role),
                expiry_days=settings.invitation_expire_hours // 24
            )

            return EmailService._send_email(
                to_email=email,
                subject="You're Invited to ThreatAtlas 🎉",
                html_body=html_body
            )

        except Exception as e:
            logger.error(f"Failed to send invitation email to {email}: {str(e)}")
            return False

    @staticmethod
    def send_invitation_reminder_email(
        email: str,
        token: str,
        inviter_name: str,
        role: str,
        expiry_date: datetime
    ) -> bool:
        """
        Resend/remind invitation email to a user.

        Args:
            email: Recipient email address
            token: Unique invitation token
            inviter_name: Name of the user who sent the invitation
            role: Role the user will have
            expiry_date: When the invitation expires

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            template = jinja_env.get_template("invitation_resend_email.html")
            # nosemgrep: python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2
            html_body = template.render(
                title="Reminder: ThreatAtlas Invitation",
                invitation_url=f"{settings.frontend_url}/accept-invitation/{token}",
                inviter_name=inviter_name,
                role_display=EmailService._get_role_display(role),
                role_description=EmailService._get_role_description(role),
                expiry_date=expiry_date.strftime("%B %d, %Y")
            )

            return EmailService._send_email(
                to_email=email,
                subject="Reminder: Your ThreatAtlas Invitation",
                html_body=html_body
            )

        except Exception as e:
            logger.error(f"Failed to send reminder email to {email}: {str(e)}")
            return False

    @staticmethod
    def send_welcome_email(
        email: str,
        username: str,
        full_name: str | None,
        role: str
    ) -> bool:
        """
        Send welcome email to a newly registered user.

        Args:
            email: User's email address
            username: User's username
            full_name: User's full name (optional)
            role: User's role

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            template = jinja_env.get_template("welcome_email.html")
            # nosemgrep: python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2
            html_body = template.render(
                title="Welcome to ThreatAtlas",
                user_name=full_name or username,
                username=username,
                email=email,
                role_display=EmailService._get_role_display(role),
                app_url=settings.frontend_url
            )

            return EmailService._send_email(
                to_email=email,
                subject="Welcome to ThreatAtlas! 🚀",
                html_body=html_body
            )

        except Exception as e:
            logger.error(f"Failed to send welcome email to {email}: {str(e)}")
            return False
