import asyncio
from celery import Task
from app.celery_app import celery_app
from app.email_utils import EmailService, get_welcome_email_template, get_login_notification_email_template
from .config import settings

class AsyncTask(Task):
    """Custom task to handle async operations"""
    _email_service = None
    
    @property
    def email_service(self):
        if self._email_service is None:
            self._email_service = EmailService(use_mailtrap=True)
        return self._email_service
    
    
    

@celery_app.task(base=AsyncTask, bind=True, name="app.tasks.send_welcome_email")
def send_welcome_email(self, user_data: dict):
    """Send welcome email to new user"""
    print(f"📧 Starting send_welcome_email with data: {user_data}")
    
    try:
        # Extract user data
        email = user_data["email"]
        username = user_data.get("username", email.split("@")[0])
        print(f"📧 Extracted - email: {email}, username: {username}")
        
        # Create email content
        subject = "Welcome to Our Platform!"
        print(f"📧 Getting email template for {username}")
        html_content = get_welcome_email_template(username)
        print(f"📧 Template created, length: {len(html_content)}")
        
        # Send email (run async in sync context)
        print(f"📧 Creating event loop...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        print(f"📧 Sending email via EmailService...")
        success = loop.run_until_complete(
            self.email_service.send_email(email, subject, html_content)
        )
        loop.close()
        
        print(f"📧 Send result: success={success}")
        
        if success:
            print(f"✅ Welcome email sent to {email}")
            return {"status": "success", "email": email}
        else:
            print(f"❌ Failed to send email to {email}")
            raise Exception("Failed to send email")
            
    except Exception as e:
        print(f"❌ Error in send_welcome_email: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        self.retry(exc=e, countdown=60, max_retries=3)
        
        
        
        

@celery_app.task(base=AsyncTask, bind=True, name="app.tasks.send_login_notification")
def send_login_notification(self, user_data: dict):
    
    print(f"📧 Starting send_login_email with data: {user_data}")
    
    """Send login notification email"""
    try:
        email = user_data["email"]
        username = user_data.get("username", email.split("@")[0])
        login_time = user_data["login_time"]
        ip_address = user_data.get("ip_address", "Unknown")
        print(f"📧 Extracted - email: {email}, username: {username}")
        
        
        subject = "New Login Detected"
        html_content = get_login_notification_email_template(username, login_time, ip_address)
        
        print(f"📧 Creating event loop...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        print(f"📧 Sending email via EmailService...")
        success = loop.run_until_complete(
            self.email_service.send_email(email, subject, html_content)
        )
        loop.close()
        
        return {"status": "success", "email": email, "type": "login_notification"}
        
    except Exception as e:
        print(f"❌ Error in send_welcome_email: {type(e).__name__}: {e}")
        self.retry(exc=e, countdown=60, max_retries=3)
        
        

@celery_app.task(name="app.tasks.send_bulk_notifications")
def send_bulk_notifications(recipients: list, subject: str, template_name: str, template_data: dict):
    """Send bulk notifications (for cron jobs)"""
    # Implementation for periodic tasks
    pass

@celery_app.task(name="app.tasks.cleanup_old_notifications")
def cleanup_old_notifications():
    """Periodic cleanup task"""
    # Implementation for cleaning up old notification records
    pass