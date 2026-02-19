import aiosmtplib
from email.message import EmailMessage
from typing import List, Optional
from app.config import settings

class EmailService:
    def __init__(self, use_mailtrap: bool = True):
        self.use_mailtrap = use_mailtrap
        self._configure_smtp()
    
    def _configure_smtp(self):
        """Configure SMTP based on environment"""
        if self.use_mailtrap:
            self.host = settings.mailtrap_smtp_host
            self.port = settings.mailtrap_smtp_port
            self.username = settings.mailtrap_smtp_user
            self.password = settings.mailtrap_smtp_password
        else:
            self.host = settings.SMTP_HOST
            self.port = settings.SMTP_PORT
            self.username = settings.SMTP_USER
            self.password = settings.SMTP_PASSWORD
        
        self.from_email = settings.mailtrap_smtp_user
        self.from_name = settings.mailtrap_smtp_from_name
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send single email"""
        try:
            message = EmailMessage()
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email
            message["Subject"] = subject
            
            # Set content
            message.set_content(text_content or "Please enable HTML to view this email.")
            message.add_alternative(html_content, subtype="html")
            
            # Send via SMTP
            await aiosmtplib.send(
                message,
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                use_tls=self.port == 587,  # TLS for 587, SSL for 465
            )
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
    
    async def send_bulk_emails(
        self,
        recipients: List[str],
        subject: str,
        html_content: str
    ) -> dict:
        """Send bulk emails"""
        results = {"success": [], "failed": []}
        for email in recipients:
            success = await self.send_email(email, subject, html_content)
            if success:
                results["success"].append(email)
            else:
                results["failed"].append(email)
        return results

# Email templates
def get_welcome_email_template(username: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .button {{ background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Our App!</h1>
            </div>
            <div class="content">
                <p>Hi {username},</p>
                <p>Thank you for registering! We're excited to have you on board.</p>
                <p>Please verify your email address to get started:</p>
                <p><a href="#" class="button">Verify Email</a></p>
                <p>If you didn't create this account, please ignore this email.</p>
                <p>Best regards,<br>The Team</p>
            </div>
        </div>
    </body>
    </html>
    """

def get_login_notification_email_template(username: str, login_time: str, ip_address: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h2>New Login Detected</h2>
        <p>Hi {username},</p>
        <p>We detected a new login to your account:</p>
        <ul>
            <li><strong>Time:</strong> {login_time}</li>
            <li><strong>IP Address:</strong> {ip_address}</li>
        </ul>
        <p>If this was you, you can ignore this email.</p>
        <p>If you don't recognize this activity, please secure your account immediately.</p>
    </body>
    </html>
    """