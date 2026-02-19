# test_email.py
import asyncio
import aiosmtplib
from email.message import EmailMessage

async def send_test_email():
    message = EmailMessage()
    message["From"] = "Iron Vault <noreply@yourapp.com>"
    message["To"] = "test@example.com"
    message["Subject"] = "Test Email from Iron Vault"
    message.set_content("This is a test email to verify Mailtrap works!")
    
    try:
        await aiosmtplib.send(
            message,
            hostname="smtp.mailtrap.io",
            port=2525,
            username="9552358ed86433",
            password="472cb13a478a9e",
            use_tls=False,
            start_tls=True
        )
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send: {e}")

asyncio.run(send_test_email())