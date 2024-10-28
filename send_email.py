import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sender and recipient information
sender_email = "zhengweihang79@gmail.com"  # Sender's Gmail address
recipient_email = "xxweislyxx@gmail.com"  # Recipient's email address
sender_password = "pnps vkxl pgvi djfx"  # Use app password if 2FA is enabled

# Create the message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = recipient_email
msg["Subject"] = "Important Update"

# Add body to the message
body = """
Hello,

This is a test email sent from a Python script.

Best regards,
Your Name
"""
msg.attach(MIMEText(body, "plain"))

try:
    # Connect to the server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.set_debuglevel(1)  # Enable debug output
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
