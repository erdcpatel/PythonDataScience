import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define the HTML header and footer
with open('header.html', 'r') as f:
    header = f.read()

with open('footer.html', 'r') as f:
    footer = f.read()

# Define the email content with dynamic placeholders
content = """
<html>
  <head></head>
  <body>
    <p>Hello {name},</p>
    <p>Your file {filename} was {status}.</p>
    <p>Here is your custom report:</p>
    <table>
      <tr>
        <th>Metric</th>
        <th>Value</th>
      </tr>
      <tr>
        <td>Metric 1</td>
        <td>{metric1}</td>
      </tr>
      <tr>
        <td>Metric 2</td>
        <td>{metric2}</td>
      </tr>
    </table>
  </body>
</html>
"""

# Insert dynamic content into the email content
name = "John"
filename = "report.csv"
status = "uploaded successfully"
metric1 = 10
metric2 = 20
email_content = content.format(name=name, filename=filename, status=status, metric1=metric1, metric2=metric2)

# Combine the HTML header, content, and footer
html = header + email_content + footer

# Send the email
msg = MIMEMultipart()
msg['From'] = "sender@example.com"
msg['To'] = "recipient@example.com"
msg['Subject'] = "Custom Report"
msg.attach(MIMEText(html, 'html'))

smtp_server = "smtp.example.com"
smtp_port = 587
smtp_username = "sender@example.com"
smtp_password = "password"
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_username, smtp_password)
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()


''''''''''''''''''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import os

# Define the HTML header and footer
with open('header.html', 'r') as f:
    header = f.read()

with open('footer.html', 'r') as f:
    footer = f.read()

# Read the email content from a file
with open('content.html', 'r') as f:
    content = f.read()

# Insert dynamic content into the email content
name = "John"
filename = "report.csv"
status = "uploaded successfully"
metric1 = 10
metric2 = 20
email_content = content.format(name=name, filename=filename, status=status, metric1=metric1, metric2=metric2)

# Combine the HTML header, content, and footer
html = header + email_content + footer

# Create the email message
msg = EmailMessage()
msg['From'] = "sender@example.com"
msg['To'] = "recipient@example.com"
msg['Subject'] = "Custom Report"

# Add the HTML email content
msg.set_content(html, subtype='html')

# Add the attachment if there was a failure
if status != "uploaded successfully":
    with open('template.csv', 'rb') as f:
        attachment = f.read()
    msg.add_attachment(attachment, maintype='application', subtype='octet-stream', filename='template.csv')

# Send the email
smtp_server = "smtp.example.com"
smtp_port = 587
smtp_username = "sender@example.com"
smtp_password = "password"
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)
