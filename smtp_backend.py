import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders
from email.mime.base import MIMEBase

def send_enhanced_email(sender_email, app_password, receiver_email, subject, plain_body, attachment_path=None, smtp_server="smtp.gmail.com", port=587):
    """
    Enhanced SMTP email function with file attachment support
    Returns: (success: bool, message: str, details: dict)
    """
    
    # Create HTML version automatically
    html_body = f"""
    <html>
      <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #4CAF50; color: white; padding: 15px; text-align: center; }}
            .content {{ padding: 20px; background: #f9f9f9; }}
            .footer {{ text-align: center; padding: 10px; font-size: 12px; color: #666; }}
        </style>
      </head>
      <body>
        <div class="container">
            <div class="header">
                <h2>📧 SMTP Protocol Email</h2>
            </div>
            <div class="content">
                {plain_body.replace('\n', '<br>')}
            </div>
            <div class="footer">
                <p>This email was sent using <b>Python SMTP Protocol</b></p>
                <p>Computer Networks Mini-Project | SMTP Demonstration</p>
            </div>
        </div>
      </body>
    </html>
    """
    
    # Create message container
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = f"Python SMTP Client <{sender_email}>"
    message['To'] = receiver_email
    
    # Attach both plain text and HTML versions
    part1 = MIMEText(plain_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    message.attach(part1)
    message.attach(part2)
    
    # Add attachment if provided
    attachment_info = None
    if attachment_path and os.path.exists(attachment_path):
        try:
            # Get file details
            filename = os.path.basename(attachment_path)
            file_size = os.path.getsize(attachment_path)
            
            with open(attachment_path, "rb") as attachment:
                # Create attachment part
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)
            
            # Add header as key/value pair to attachment part
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            
            # Add attachment to message
            message.attach(part)
            attachment_info = {
                "filename": filename,
                "size": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            return False, f"❌ Error processing attachment: {str(e)}", {}
    
    try:
        # SMTP Connection Process
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Secure the connection
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        
        # Prepare success response
        details = {
            "from": sender_email,
            "to": receiver_email,
            "subject": subject,
            "body_length": len(plain_body),
            "html_included": True,
            "smtp_server": smtp_server,
            "port": port,
            "attachment": attachment_info
        }
        
        return True, "✅ Email sent successfully!", details
        
    except smtplib.SMTPAuthenticationError:
        return False, "❌ Authentication failed! Please check:\n- Email address\n- App Password (16 characters)\n- 2-Factor Authentication is enabled", {}
    
    except smtplib.SMTPConnectError:
        return False, "❌ Connection failed! Check:\n- Internet connection\n- SMTP server and port\n- Firewall settings", {}
    
    except Exception as e:
        return False, f"❌ Error: {str(e)}", {}