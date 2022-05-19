import httplib2
import os
import oauth2client
from oauth2client import client, tools, file
import base64
from email import encoders
import smtplib  
import mimetypes
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from apiclient import errors, discovery

def get_credentials():
  home_dir = os.path.expanduser('~') #>> C:\Users\Me
  credential_dir = os.path.join(home_dir, '.credentials') # >>C:\Users\Me\.credentials   (it's a folder)
  if not os.path.exists(credential_dir):
      os.makedirs(credential_dir)  #create folder if doesnt exist
  credential_path = os.path.join(credential_dir, 'cred send mail.json')
  store = oauth2client.file.Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
      CLIENT_SECRET_FILE = 'credentials.json'
      APPLICATION_NAME = 'Gmail API Python Send Email'
      SCOPES = 'https://www.googleapis.com/auth/gmail.send'
      flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
      flow.user_agent = APPLICATION_NAME
      credentials = tools.run_flow(flow, store)
  return credentials

def create_message_and_send(sender, to, subject,  message_text_plain, message_text_html, attached_file):
    credentials = get_credentials()
    http = httplib2.Http()
    http = credentials.authorize(http)        #or: http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message_without_attachment = create_message_without_attachment(sender, to, subject, message_text_html, message_text_plain)
    send_Message_without_attachement(service, "me", message_without_attachment, message_text_plain)

def create_message_without_attachment (sender, to, subject, message_text_html, message_text_plain):
    message = MIMEMultipart('alternative') # needed for both plain & HTML (the MIME type is multipart/alternative)
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = to
    message.attach(MIMEText(message_text_plain, 'plain'))
    message.attach(MIMEText(message_text_html, 'html'))
    raw_message_no_attachment = base64.urlsafe_b64encode(message.as_bytes())
    raw_message_no_attachment = raw_message_no_attachment.decode()
    body  = {'raw': raw_message_no_attachment}
    return body

def create_Message_with_attachment(sender, to, subject, message_text_plain, message_text_html, attached_file):
    message = MIMEMultipart() #when alternative: no attach, but only plain_text
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message.attach(MIMEText(message_text_html, 'html'))
    message.attach(MIMEText(message_text_plain, 'plain'))
    my_mimetype, encoding = mimetypes.guess_type(attached_file)
    if my_mimetype is None or encoding is not None:
        my_mimetype = 'application/octet-stream' 

    main_type, sub_type = my_mimetype.split('/', 1)# split only at the first '/'

    if main_type == 'text':
        print("text")
        temp = open(attached_file, 'r')  # 'rb' will send this error: 'bytes' object has no attribute 'encode'
        attachement = MIMEText(temp.read(), _subtype=sub_type)
        temp.close()

    elif main_type == 'image':
        print("image")
        temp = open(attached_file, 'rb')
        attachement = MIMEImage(temp.read(), _subtype=sub_type)
        temp.close()

    elif main_type == 'audio':
        print("audio")
        temp = open(attached_file, 'rb')
        attachement = MIMEAudio(temp.read(), _subtype=sub_type)
        temp.close()            

    elif main_type == 'application' and sub_type == 'pdf':   
        temp = open(attached_file, 'rb')
        attachement = MIMEApplication(temp.read(), _subtype=sub_type)
        temp.close()

    else:                              
        attachement = MIMEBase(main_type, sub_type)
        temp = open(attached_file, 'rb')
        attachement.set_payload(temp.read())
        temp.close()

    encoders.encode_base64(attachement)  #https://docs.python.org/3/library/email-examples.html
    filename = os.path.basename(attached_file)
    attachement.add_header('Content-Disposition', 'attachment', filename=filename) # name preview in email
    message.attach(attachement) 

    message_as_bytes = message.as_bytes() # the message should converted from string to bytes.
    message_as_base64 = base64.urlsafe_b64encode(message_as_bytes) #encode in base64 (printable letters coding)
    raw = message_as_base64.decode()  # need to JSON serializable (no idea what does it means)
    return {'raw': raw} 

def send_Message_without_attachement(service, user_id, body, message_text_plain):
    try:
        message_sent = (service.users().messages().send(userId=user_id, body=body).execute())
        message_id = message_sent['id']
        # print(attached_file)
        print (f'Message sent (without attachment) \n\n Message Id: {message_id}\n\n Message:\n\n {message_text_plain}')
        # return body
    except errors.HttpError as error:
        print (f'An error occurred: {error}')

def send_Message_with_attachement(service, user_id, message_with_attachment, message_text_plain, attached_file):
    try:
        message_sent = (service.users().messages().send(userId=user_id, body=message_with_attachment).execute())
        message_id = message_sent['id']
    except errors.HttpError as error:
        print (f'An error occurred: {error}')

def main():
    to = 'toyoalsrl@gmail.com'
    sender = "snowman"
    subject = "hello"
    message_text_html  = r'hello<br/> <b>감사합니다</b>'
    message_text_plain = "Hi\n"
    attached_file = r'C:\Users\Me\Desktop\audio.m4a'
    create_message_and_send(sender, to, subject, message_text_plain, message_text_html, attached_file)

# if __name__ == '__main__':
#     main()

main()