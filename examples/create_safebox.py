from sendsecure import Safebox, Recipient, ContactMethod, Attachment, Client

if __name__ == "__main__":
    try:
         user_email = 'darthvader@empire.com'
         token = 'USER|1d495165-4953-4457-8b5b-4fcf801e621a'
         enterprise_account = 'deathstar'
         endpoint = 'https://portal.xmedius.com'

         safebox = Safebox(user_email)
         safebox.subject = 'Family matters'
         safebox.message = 'Son, you will find attached the evidence.'

         recipient = Recipient('lukeskywalker@rebels.com')
         recipient.contact_methods.append(ContactMethod('555-232-5334'))
         safebox.recipients.append(recipient);

         attachment = Attachment('Birth_Certificate.pdf', 'application/pdf');
         safebox.attachments.append(attachment);

         client = Client(token, enterprise_account, endpoint);
         safe_response = client.submit_safebox(safebox);
         print 'SafeBox ID:', safe_response.guid
    except Exception, details:
        print details
