import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def _send_email(subject, body, receiver_email, sender_email, cc_email, bcc_email, smtp_server, smtp_port, smtp_password, attachment_files=None):
    try:        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(receiver_email)
        msg['Cc'] = ', '.join(cc_email)  # Add CC to the headers
        msg['Subject'] = subject

        # Attach the body with the email
        msg.attach(MIMEText(body, 'html'))

        # Attach the uploaded files, if provided
        if attachment_files:
            for filename, file_contents in attachment_files:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file_contents)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                msg.attach(part)

        # Convert the message to a string
        msg_string = msg.as_string()

        # Collect all recipients (To + CC + BCC)
        all_recipients = receiver_email + cc_email + bcc_email

        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, smtp_password)
            server.sendmail(sender_email, all_recipients, msg_string)

        return {"status": 200, "message": "Email sent successfully!"}
    except Exception as e:
        return {"status": 500, "message": "Error sending email: " + str(e)}


if __name__ == "__main__":
    _send_email(
        "Test Subject", 
        "Test Body", 
        ["receiver1@example.com", "receiver2@example.com"],  # List of To recipients
        "sender@example.com", 
        ["cc1@example.com", "cc2@example.com"],  # List of CC recipients
        ["bcc1@example.com", "bcc2@example.com"],  # List of BCC recipients
        'smtp.office365.com', 
        587,
        "smtp_password"
    )
