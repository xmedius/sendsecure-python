from sendsecure import Safebox, Participant, ContactMethod, Attachment, Client

if __name__ == "__main__":
    try:
        user_email = 'darthvader@empire.com'
        token = 'USER|1d495165-4953-4457-8b5b-4fcf801e621a'
        enterprise_account = 'deathstar'
        endpoint = 'https://portal.xmedius.com'

        safebox = Safebox(user_email=user_email)
        safebox.subject = 'Family matters'
        safebox.message = 'Son, you will find attached the evidence.'

        participant = Participant(email='lukeskywalker@rebels.com')
        contact_method = ContactMethod({'destination': '555-232-5334', 'destination_type':ContactMethod.DestinationType.HOME})
        participant.guest_options.contact_methods.append(contact_method)
        safebox.participants.append(participant)

        attachment = Attachment({'source': 'Birth_Certificate.pdf', 'content_type': 'application/pdf'})
        safebox.attachments.append(attachment)

        options = {'token': token, 'enterprise_account': enterprise_account, 'endpoint': endpoint}
        client = Client(options)
        safe_response = client.submit_safebox(safebox)
        print('SafeBox ID:', safe_response.guid)
    except Exception as details:
        print(details)
