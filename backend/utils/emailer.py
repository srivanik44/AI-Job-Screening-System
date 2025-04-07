import smtplib
from email.message import EmailMessage

# ✅ Set your Gmail and app password here
sender = "Shadowquill60@gmail.com"
password = "vinzvqzpyxzmedmw"  # 🔒 Use your actual app password (not Gmail login)

def send_interview_email(name, email, role, company="Our Company"):
    # Static interview details
    interview_date = "Wednesday, April 10th"
    interview_time = "11:00 AM"
    interview_mode = "Zoom"
    zoom_link = "https://zoom.us/your-interview-link"

    subject = f"Interview Invitation for {role} Role at {company}"

    body = f"""
Hi {name},

We are pleased to inform you that you have been shortlisted for the position of {role} at {company}.

We would like to schedule your interview as per the following details:

📅 Date: {interview_date}  
⏰ Time: {interview_time}  
💻 Mode: {interview_mode}  
🔗 Zoom Link: {zoom_link}

Please be available 5 minutes before the scheduled time.  
If you have any questions or need to reschedule, feel free to reach out to us.

Best regards,  
HR Team  
"""

    # Create and send the email
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print(f"✅ Interview email sent to {email}")
        return f"✅ Interview email sent to {name} ({email}) for role: {role}"
    except Exception as e:
      print(f"❌ Email failed to send: {str(e)}")  # ✅ See what went wrong
      return "❌ Failed to send interview email."

