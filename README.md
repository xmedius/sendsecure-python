**XM SendSecure** is a collaborative file exchange platform that is both highly secure and simple to use.
It is expressly designed to allow for the secure exchange of sensitive documents via virtual SafeBoxes.

XM SendSecure comes with a **Web API**, which is **RESTful**, uses **HTTPs** and returns **JSON**.

Specific libraries have been published for various languages:
[C#](https://github.com/xmedius/sendsecure-csharp),
[Java](https://github.com/xmedius/sendsecure-java),
[JavaScript](https://github.com/xmedius/sendsecure-js),
[PHP](https://github.com/xmedius/sendsecure-php),
**Python**
and
[Ruby](https://github.com/xmedius/sendsecure-ruby).


# sendsecure-python

**This library allows you to use the XM SendSecure Web API via Python.**

With this library, you will be able to:
* Authenticate SendSecure users
* Create new SafeBoxes


# Table of Contents

* [Installation](#installation)
* [Quick Start](#quick-start)
* [Usage](#usage)
* [License](#license)
* [Credits](#credits)


# Installation

## Prerequisites

- Python version 3.7+
- The XM SendSecure solution, provided by [XMedius](https://www.xmedius.com?source=sendsecure-python) (demo accounts available on demand)

## Install Package

```python
pip install https://github.com/xmedius/sendsecure-python/tarball/master
```

# Quick Start

## Authentication (Retrieving API Token)

Authentication is done using an API Token, which must be first obtained based on SendSecure enterprise account and user credentials.
Here is the minimum code to get such a user-based API Token (and the user ID).

```python
from sendsecure import Client

if __name__ == "__main__":
    try:
        enterprise_account = 'deathstar'
        username = 'darthvader'
        password = 'd@Rk$1De'

        device_id = 'DV-TIE/x1'
        device_name = 'TIE Advanced x1'
        application_type = 'The Force App'
        endpoint = 'https://portal.xmedius.com'

        token_detail = Client.get_user_token(enterprise_account, username, password,
            device_id, device_name, application_type, endpoint)
        print('User token:', token_detail['token'])
        print('User id:', result['user_id'])
    except Exception as details:
        print(details)
```

## SafeBox Creation (Using SafeBox Helper Class)

Here is the minimum required code to create a SafeBox – with 1 recipient, a subject, a message and 1 attachment.
This example uses the user's *default* security profile (which requires to be set in the account).

```python
from sendsecure import Safebox, Participant, ContactMethod, Attachment, Client

if __name__ == "__main__":
    try:
         user_email = 'darthvader@empire.com'
         token = token_detail['token']
         user_id = token_detail['user_id']
         enterprise_account = 'deathstar'
         endpoint = 'https://portal.xmedius.com'

         safebox = Safebox(user_email=user_email)
         safebox.subject = 'Family matters'
         safebox.message = 'Son, you will find attached the evidence.'

         recipient = Participant(email='lukeskywalker@rebels.com')
         recipient.guest_options.contact_methods.append(ContactMethod({'destination': '555-232-5334'}))
         safebox.participants.append(recipient)

         attachment = Attachment('Birth_Certificate.pdf', 'application/pdf')
         safebox.attachments.append(attachment)

         client = Client({'token': token, 'enterprise_account': enterprise_account, 'endpoint': endpoint})
         safebox_response = client.submit_safebox(safebox)
         print('SafeBox ID:', safebox_response.guid)
    except Exception as details:
        print(details)
```


# Usage

## Helper Methods

### Get User Token
```
get_user_token(enterprise_account, username, password, device_id, device_name, application_type, endpoint, one_time_password)
```
Creates and returns two properties: an API Token and a user ID, for a specific user within a SendSecure enterprise account.
Calling this method again with the exact same params will always return the same Token.

Param              | Definition
-------------------|-----------
enterprise_account | The SendSecure enterprise account
username           | The username of a SendSecure user of the current enterprise account
password           | The password of this user
device_id          | The unique ID of the device used to get the Token
device_name        | The name of the device used to get the Token
application_type   | The type/name of the application used to get the Token ("SendSecure Python" will be used by default if empty)
endpoint           | The URL to the SendSecure service ("https://portal.xmedius.com" will be used by default if empty)
one_time_password  | The one-time password of this user (if any)


### Client Object Constructor
```
Client(options)
```
The options object contains the following parameters :

Param              | Definition
-------------------|-----------
api_token          | The API Token to be used for authentication with the SendSecure service
enterprise_account | The SendSecure enterprise account
endpoint           | The URL to the SendSecure service ("https://portal.xmedius.com" will be used by default if empty)
locale             | The locale in which the server errors will be returned ("en" will be used by default if empty)
user_id            | The user ID, which may be used to manage additional objects directly related to the user (e.g. favorites)

### Enterprise Methods

#### Get Enterprise Settings
```
get_enterprise_settings()
```
Returns all SendSecure General Settings values/properties of the current enterprise account.

#### Get Default Security Profile
```
get_default_security_profile(user_email)
```
Returns the default security profile (if it has been set) for a specific user, with all its setting values/properties.

Param      | Definition
-----------|-----------
user_email | The email address of a SendSecure user of the current enterprise account

#### Get Security Profiles
```
get_security_profiles(user_email)
```
Returns the list of all security profiles available to a specific user, with all their setting values/properties.

Param      | Definition
-----------|-----------
user_email | The email address of a SendSecure user of the current enterprise account

### Consent Message Group Methods

#### Get Consent Message (in all locales)
```
get_consent_group_messages(consent_group_id)
```
Retrieves the consent message (in all available locales) associated to a Security Profile or a SafeBox, among the available consent messages of the current enterprise account.

Param               | Definition
--------------------|-----------
consent_group_id    | The unique ID of the consent group.

### SafeBox Creation Methods

#### Initialize SafeBox
```
initialize_safebox(safebox)
```
Pre-creates a SafeBox on the SendSecure system and returns the updated [Safebox](#safebox) object with the necessary system parameters filled out (GUID, public encryption key, upload URL).

Param      | Definition
-----------|-----------
safebox    | A [Safebox](#safebox) object to be initialized by the SendSecure system

#### Upload Attachment
```
upload_attachment(safebox, attachment)
```
Uploads the specified file as an Attachment of the specified SafeBox and returns the updated [Attachment](#attachment) object with the GUID parameter filled out.

Param       | Definition
------------|-----------
safebox     | An initialized [Safebox](#safebox) object
attachment  | An [Attachment](#attachment) object - the file to upload to the SendSecure system

#### Commit SafeBox
```
commit_safebox(safebox)
```
Finalizes the creation (commit) of the SafeBox on the SendSecure system.
This actually "Sends" the SafeBox with all content and contact info previously specified.

Param      | Definition
-----------|-----------
safebox    | A [Safebox](#safebox) object already initialized, with security profile, participant(s), subject and message already defined, and attachments already uploaded.

#### Submit SafeBox
```
submit_safebox(safebox)
```
This high-level method combines the SafeBox initialization, attachment uploads and the SafeBox commit.

Param      | Definition
-----------|-----------
safebox    | A non-initialized [Safebox](#safebox) object with security profile, participants(s), subject, message and attachments (not yet uploaded) already defined.

### Safebox Methods

#### Reply
```
reply(safebox, reply)
```
Replies to a specific SafeBox with the content specified through a Reply object.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.
reply                | A [Reply](#reply-object) object.

#### Add Time
```
add_time(safebox, value, unit)
```
Extends the SafeBox duration by the specified amount of time.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.
value                | The time value, according to the specified unit.
unit                 | The time unit. Accepted values:```hours```, ```days```, ```weeks```, ```months```.

#### Close SafeBox
```
close_safebox(safebox)
```
Closes the SafeBox immediately, i.e. before its intended expiration. Only available for SafeBoxes in "open" status.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Delete SafeBox Content
```
delete_safebox_content(safebox)
```
Deletes the SafeBox content immediately, i.e. despite the remaining retention period. Only available for SafeBoxes in "closed" status.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Mark SafeBox as Read
```
mark_as_read(safebox)
```
Marks as read all messages within the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Mark SafeBox as Unread
```
mark_as_unread(safebox)
```
Marks as unread all messages within the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Mark Message as Read
```
mark_as_read_message(safebox, message)
```
Marks as read a specific message within the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.
message              | A [Message](#message) object.

#### Mark Message as Unread
```
mark_as_unread_message(safebox, message)
```
Marks as unread a specific message within the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.
message              | A [Message](#message) object.

#### Unfollow SafeBox
```
unfollow(safebox)
```
Call to unfollow the SafeBox. By default, all new SafeBoxes are "followed".

Param                | Definition
---------------------|---------------------
safebox              | A [Safebox](#safebox) object.

#### Follow SafeBox
```
follow(safebox)
```
Call to follow the SafeBox (opposite of the [unfollow](#unfollow-safebox) call).
Param                | Definition
---------------------|---------------------
safebox              | A [Safebox](#safebox) object.

#### Get Audit Record PDF
```
get_audit_record_pdf(safebox)
```
Gets the Audit Record of the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Get Audit Record PDF URL
```
get_audit_record_url(safebox)
```
Gets the URL of the Audit Record of the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Get SafeBox Info
```
get_safebox_info(safebox, sections)
```
Gets all information of the SafeBox, regrouped by sections.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.
sections             | The information sections to be retrieved. Accepted values: ```download_activity```, ```event_history```, ```messages```, ```participants```, ```security_options```. Must be an array of string.

#### Get SafeBox Participants
```
get_safebox_participants(safebox)
```
Gets the list of all participants of the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Get SafeBox Messages
```
get_safebox_messages(safebox)
```
Gets all the messages of the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Get SafeBox Security Options
```
get_safebox_security_options(safebox)
```
Gets all the security options of the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Get SafeBox Download Activity
```
get_safebox_download_activity(safebox)
```
Gets all the download activity information of the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

#### Get SafeBox Event History
```
get_safebox_event_history(safebox)
```
Retrieves the complete event history of the SafeBox.

Param                | Definition
---------------------|-----------
safebox              | A [Safebox](#safebox) object.

### SafeBox Attached Document Methods

#### Get File URL
```
get_file_url(safebox, document)
```
Returns the URL of a document contained in a SafeBox (allowing to download it from the File Server).

Param      | Definition
-----------|-----------
safebox    | A [Safebox](#safebox) object.
document   | An [Attachment](#attachment) object.

### Participant Management Methods

#### Create Participant
```
create_participant(safebox, participant)
```
Creates a new Participant and adds it to the SafeBox.

Param        | Definition
-------------|-------------
safebox      | A [Safebox](#safebox) object.
participant  | A [Participant](#participant) object.

#### Update Participant
```
update_participant(safebox, participant)
```
Updates an existing participant of the specified SafeBox.

Param        | Definition
-------------|-------------
safebox      | A [Safebox](#safebox) object.
participant  | The updated [Participant](#participant) object.

#### Delete Participant's Contact Methods
```
delete_participant_contact_methods(safebox, participant, contact_method_ids)
```
Deletes one or several contact methods of an existing participant of the specified SafeBox.

Param                | Definition
---------------------|---------------------
safebox              | A [Safebox](#safebox) object.
participant          | A [Participant](#participant) object.
contact_method_ids   | An array of contact method unique IDs (see [ContactMethod](#contactmethod) object).


### Recipient Methods

#### Search Recipient
```
search_recipient(term)
```
Returns a list of people (e.g. among Favorites and/or Enterprise Users) that match the specified search term, typically for auto-suggestion when adding participants to a new/existing SafeBox. The returned list depends on the *autocomplete* attributes of the Enterprise Settings.

Param      | Definition
-----------|-----------
term       | A string intended to match a portion of name, email address or company.

### SafeBox List (SafeBoxes) Methods

#### Get SafeBox List
```
get_safeboxes(url, search_params)
```
Returns an object containing the count of found SafeBoxes, the previous page URL, the next page URL and a list of [Safebox](#safebox) objects – for the current user account and according to the specified filtering options.

Param          | Definition
---------------|-----------
url            | The search url (optional).
search_params  | An object containing optional filtering parameters (see options and example below).

Available filtering options:
  * ```status```: to filter by SafeBox status: ```in_progress```, ```closed```, ```content_deleted```, ```unread```.
  * ```search```: to search using a term intended to match a portion of SafeBox subject/ID/message, participant email/first name/last name, attached file name/fingerprint.
  * ```per_page```: to split the list in several pages, with 0 < per_page <= 1000 (default is 100).
  * ```page```: to select the page to return.

Example to return the 1st page with 20 SafeBoxes that are open and unread and that contain the word "Luke":
```
get_safeboxes({ 'status': 'in_progress,unread', 'search_term': 'Luke', 'per_page': 20, 'page': 1 })
```

### User Methods

#### Get User Settings
```
user_settings()
```
Retrieves all the SendSecure User Settings for the current user account.

#### Get Favorites
```
get_favorites()
```
Retrieves all favorites associated to the current user account.

#### Create Favorite
```
create_favorite(favorite)
```
Creates a new favorite for the current user account.

Param                | Definition
---------------------|-----------
favorite             | A [Favorite](#favorite) object.

#### Update Favorite
```
update_favorite(favorite)
```
Updates an existing favorite associated to the current user account.

Param                | Definition
---------------------|-----------
favorite             | The updated [Favorite](#favorite) object.

#### Delete Favorite's Contact Methods
```
delete_favorite_contact_methods(favorite, contact_method_ids)
```
Deletes one or several contact methods of an existing favorite associated to the current user account.

Param                | Definition
---------------------|-----------
favorite             | A [Favorite](#favorite) object.
contact_method_ids   | An array of contact method unique IDs (see [ContactMethod](#contactmethod) object).

#### Delete Favorite
```
delete_favorite(favorite)
```
Delete an existing favorite associated to the current user account.

Param                | Definition
---------------------|-----------
favorite             | A [Favorite](#favorite) object.

## Helper Objects
Here is the alphabetical list of all available objects, with their attributes.

### Attachment
Builds an object to be uploaded to the server as attachment of the SafeBox.
Subset of [Safebox](#safebox) object.
Can be created either with a [File Path](#file-path), a [File](#file) or a [Stream](#stream).
All attributes are mandatory (unless otherwise stated).

#### File Path
Attribute            | Definition
---------------------|-----------
guid                 | The unique ID of the attachment (filled by the system once the file is uploaded).
content_type         | The file Content-type (MIME).
source               | The path (full filename) of the file to upload.
filename             | An alternative file name for the file to upload (optional).

#### File
Attribute            | Definition
---------------------|-----------
guid                 | The unique ID of the attachment (filled by the system once the file is uploaded).
content_type         | The file Content-type (MIME).
source               | The file object to upload.
filename             | An alternative file name for the file to upload (optional).

#### Stream

Attribute            | Definition
---------------------|-----------
guid                 | The unique ID of the attachment (filled by the system once the file is uploaded).
content_type         | The file Content-type (MIME).
source               | The data to upload (any object that implement the file.read() method).
filename             | The file name.
size                 | The file size.

### ConsentMessage
Builds an object to retrieve a consent message in a specific locale.
Subset of [ConsentMessageGroup](#consentmessagegroup) (regrouping all locales of a same consent message).
All attributes are read only.

Attribute            | Definition
---------------------|-----------
locale               | The locale in which the consent message will be returned.
value                | The text of the consent message.
created_at           | The creation date of the consent message.
updated_at           | The last modification date of the consent message.

### ConsentMessageGroup
Builds an object to retrieve all localized versions of the same consent message.
All attributes are read only.

Attribute            | Definition
---------------------|-----------
id                   | The unique ID of the consent message group.
name                 | The name of the consent message group.
created_at           | The creation date of the consent message group.
updated_at           | The last modification date of the consent message group.
consent_messages     | The list of [ConsentMessage](#consentmessage) objects (one per available locale).

### ContactMethod
Builds an object to create a phone number destination owned by a participant or a favorite (or retrieve the contact method information).
May be a subset of [GuestOptions](#guestoptions) or [Favorite](#favorite).
Any ContactMethod – plus the email address – will be usable as Security Code delivery means to the participant.

Attribute            | Definition
---------------------|-----------
destination          | (mandatory) A phone number owned by the participant.
destination_type     | (mandatory) The phone number's type (i.e. home/cell/office/other).
_destroy             | (contextual\*) Indicates whether the contact method should be deleted or not.
id                   | (read only) The unique ID of the contact method.
verified             | (read only) Indicates whether the contact method was verified by the SendSecure system or not (through authentication mechanism).
created_at           | (read only) The creation date of the contact method.
updated_at           | (read only) The last modification date of the contact method.

\* Mandatory only if the existing contact method must be destroyed

### Document
Depending on the context, this object may return two different types of information:

* As a MessageDocument:
Builds an object to retrieve all information of a specific document (file) from a message within an existing SafeBox.
Subset of [Message](#message) object.
All attributes are read only.

Attribute            | Definition
---------------------|-----------
id                   | The unique ID of the file.
name                 | The file name.
sha                  | The fingerprint (SHA-256) of the file.
size                 | The file size.
url                  | The URL of the file.

* As a DownloadActivityDocument:
Builds an object with all the download activity informations for a specific document regarding a specific participant of the SafeBox.
Subset of [DownloadActivityDetail](#downloadactivitydetail).
All attributes are read only.

Attribute            | Definition
---------------------|-----------
id                   | The unique ID of the download activity document.
downloaded_bytes     | The number of bytes of the document that were actually downloaded.
downloaded_date      | The date of the download.

### DownloadActivity
Builds an object with all download activity information of all participants of an existing SafeBox.
Subset of [Safebox](#safebox) object.
All attributes are read only.

Attribute            | Definition
---------------------|-----------
guests               | The list of [DownloadActivityDetail](#downloadactivitydetail) objects associated with each SafeBox participant other than the Owner.
owner                | The [DownloadActivityDetail](#downloadactivitydetail) object associated with the SafeBox Owner.



### DownloadActivityDetail
Builds an object with all the download activity details for a specific participant of the SafeBox.
Subset of [DownloadActivity](#downloadactivity).
All attributes are read only.

Attribute            | Definition
---------------------|-----------
id                   | The unique ID of the download activity detail.
documents            | The list of [Document](#document) objects associated with the SafeBox participant.

### EnterpriseSettings
Builds an object with the SendSecure settings of an Enterprise Account.
All attributes are read only.

Attribute                         | Definition
----------------------------------|--------------------
default_security_profile_id       | The unique ID of the default security profile of the enterprise.
pdf_language                      | The language in which all SafeBox Audit Records are generated.
use_pdfa_audit_records            | Indicates whether the Audit Records are generated as PDF/A or not.
international_dialing_plan        | The country/dialing plan used for formatting national numbers when sending information by phone/SMS.
extension_filter                  | The [ExtensionFilter](#extensionfilter) object associated with the enterprise account.
virus_scan_enabled                | Indicates whether the virus scan is applied or not when uploading files to SafeBoxes.
max_file_size_value               | The maximum file size allowed for a SafeBox attachment.
max_file_size_unit                | The unit of the maximum file size value.
include_users_in_autocomplete     | Indicates whether the users of the enterprise account should be included or not in recipient automatic suggestion.
include_favorites_in_autocomplete | Indicates whether the favorites of the current user should be included or not in recipient automatic suggestion.
users_public_url                  | Indicates whether the Personal Secure Links are allowed or not for the users of the enterprise account.
created_at                        | The creation date of the enterprise settings.
updated_at                        | The last modification date of the enterprise settings.

### EventHistory
Builds an object with all Event History information of a SafeBox.
Subset of [Safebox](#safebox) object.
All attributes are read only.

Attribute            | Definition
---------------------|-----------
type                 | The type of the event.
date                 | The date of the event.
metadata             | An object containing all available metadata according to the type of event.
message              | The complete message describing the event, localized according to the current user locale.

### ExtensionFilter
Builds an object with the list of allowed or forbidden extensions for SafeBox attachments.
Subset of [EnterpriseSettings](#enterprisesettings).
All attributes are read only.

Attribute            | Definition
---------------------|-----------
mode                 | Indicates whether the attachments extensions are allowed or forbidden.
list                 | The list of allowed/forbidden extensions for SafeBox attachments.

### Favorite
Builds an object to create a favorite for a user (or retrieve favorite information).

Attribute            | Definition
---------------------|-----------
email                | (mandatory) The email address of the favorite.
first_name           | (optional) The first name of the favorite.
last_name            | (optional) The last name of the favorite.
company_name         | (optional) The company name of the favorite.
contact_methods      | (contextual\*) The list of all [ContactMethod](#contactmethod) objects of the favorite.
order_number         | (optional) The ordering number of the favorite among the other favorites.
id                   | (read only) The unique ID of the favorite.
created_at           | (read only) The creation date of the favorite.
updated_at           | (read only) The last modification date of the favorite.

\* May be mandatory in the case the favorite is added as participant to a SafeBox requiring other contact methods than email.

### GuestOptions
Builds an object to create a subset of additional attributes for the Participant (or retrieve participant information).
Subset of [Participant](#participant).

Attribute             | Definition
----------------------|-----------
company_name          | (optional) The company name of the participant.
locked                | (optional) Indicates whether the participant access to the SafeBox was revoked or not.
contact_methods       | (contextual\*) The list of all [ContactMethod](#contactmethod) objects of the participant.
bounced_email         | (read only) Indicates if a NDR was received by the system after sending the invitation email to the participant.
failed_login_attempts | (read only) The count of the participant failed login attempts.
verified              | (read only) Indicated whether the participant email address was verified by the SendSecure system or not (through authentication mechanism).
created_at            | (read only) The creation date of the GuestOptions.
updated_at            | (read only) The last modification date of the GuestOptions.

\* May be mandatory depending on the Security Profile of the SafeBox.

### Message
Builds an object to retrieve a specific message from an existing SafeBox.
Subset of [Safebox](#safebox) object.
All attributes are read only.

Attribute            | Definition
---------------------|-----------
id                   | The unique ID of the message.
note                 | The text of the message.
note_size            | The size (character count) of the message.
read                 | Indicates whether the message was read or not.
author_id            | The unique ID of the message author.
author_type          | The participant type (Owner or other) of the author of the message, regarding the SafeBox.
created_at           | The creation date of the message.
documents            | The list of all [Document](#document) objects representing the attachments of the message.

### Participant
Builds an object to create a participant for the SafeBox (or retrieve participant information).
Subset of [Safebox](#safebox) object.

Attribute            | Definition
---------------------|-----------
email                | (mandatory) The email address of the participant.
first_name           | (optional) The first name of the participant.
last_name            | (optional) The last name of the participant.
guest_options        | (optional) The [GuestOptions](#guestoptions) object defining the additional attributes for the participant.
id                   | (read only) The unique ID of the participant.
type                 | (read only) The type of the participant (Owner or other) in the SafeBox.
role                 | (read only) The role of the participant (in terms of permissions) in the SafeBox.
message_read_count   | (read only) The count of read messages of the participant.
message_total_count  | (read only) The total count of messages of the participant.

### PersonalSecureLink
Builds an object to retrieve information about the Personal Secure Link of the current user.
Subset of [UserSettings](#usersettings).
All attributes are read only.

Attribute              | Definition
-----------------------|-----------
enabled                | Indicates whether the Personal Secure Link of the user is enabled or not.
url                    | The URL of the Personal Secure Link of the user.
security_profile_id    | The ID of the Security Profile used by the Secure Link.


### Reply object
Builds an object to create and post a reply within the SafeBox.

Attribute            | Definition
---------------------|-----------
message              | (contextual\*) The message of the Reply.
attachments          | (contextual\*) The list of all [Attachment](#attachment) objects of the Reply.
consent              | (contextual\*\*) The consent acceptance flag.
document_ids         | (auto-filled) The list of the attachment IDs.

\* A message is mandatory if no attachments are provided, and at least one attachment is required if no message is provided.
\*\* Consent acceptance may be mandatory depending on the Security Profile of the SafeBox.

### Safebox
Builds an object to create a new SafeBox or get all information of an existing SafeBox.
Once the SafeBox is created, all attributes are no longer editable.

Attribute                  | Definition
---------------------------|-----------
guid                       | (auto-filled) The unique ID of the SafeBox (available once the SafeBox is initialized).
upload_url                 | (auto-filled) The URL used to upload the SafeBox attachments (available once the SafeBox is initialized). *Note: this attribute is deprecated.*
public_encryption_key      | (auto-filled) The key used to encrypt the SafeBox attachments and/or messages (available once the SafeBox is initialized, only when Double Encryption is enabled).
user_email                 | (mandatory) The email address of the creator of the SafeBox.
subject                    | (optional) The subject of the SafeBox.
message                    | (contextual\*) The initial message of the SafeBox.
attachments                | (contextual\*) The list of all [Attachment](#attachment) objects of the SafeBox.
participants               | (mandatory) The list of all [Participant](#participant) objects of the SafeBox (at least one recipient).
security_profile_id        | (optional\*\*) The ID of the Security Profile used to create the Security Options of the SafeBox (see [SecurityProfile](#securityprofile) and [SecurityOptions](#securityoptions) objects).
notification_language      | (mandatory) The language used for email notifications sent to the recipients.
user_id                    | (read only) The unique ID of the user account of the SafeBox Owner.
enterprise_id              | (read only) The unique ID of the enterprise account of the SafeBox Owner.
status                     | (read only) The current status of the SafeBox (life cycle).
security_profile_name      | (read only) The name of the Security Profile that was used to create the SafeBox.
unread_count               | (read only) The total count of the unread messages within the SafeBox.
double_encryption_status   | (read only) The current encryption status of the SafeBox content (i.e. deciphered or key required).
audit_record_pdf           | (read only) The URL of the Audit Record PDF (available after the SafeBox is closed).
secure_link                | (read only) The URL of the Secure Link that was used to create the SafeBox (when applicable).
secure_link_title          | (read only) The Display Name of the Secure Link that was used to create the SafeBox (when applicable).
email_notification_enabled | (optional) Indicates whether email notifications are enabled for the SafeBox Owner or not (enabled by default, can be disabled for example in a context of SafeBox automated creation by a system).
preview_url                | (read only) The URL of the SafeBox in the SendSecure Web application.
encryption_key             | (read only) The encryption key intended for SafeBox participants (when Double Encryption is enabled). It is returned only once at SafeBox creation and then discarded for security reasons.
created_at                 | (read only) The date on which the SafeBox was created.
updated_at                 | (read only) The date of last modification of the SafeBox.
assigned_at                | (read only) The date on which the SafeBox was assigned to the Owner (useful in context of creation via Secure Link).
latest_activity            | (read only) The date of the latest activity that occurred in the SafeBox.
expiration                 | (read only) The date on which the SafeBox is expected to auto-close.
closed_at                  | (read only) The date on which the SafeBox was closed.
content_deleted_at         | (read only) The date on which the content of the SafeBox was deleted.
security_options           | (read only) The [SecurityOptions](#securityoptions) object, containing the whole set of Security Options of the SafeBox.
messages                   | (read only) The list of all [Message](#message) objects of the SafeBox.
download_activity          | (read only) The [DownloadActivity](#downloadactivity) object keeping track of all downloads of the SafeBox.
event_history              | (read only) The [EventHistory](#eventhistory) object keeping track of all events of the SafeBox.

\* A message is mandatory if no attachments are provided, and at least one attachment is required if no message is provided.
\*\* A Security Profile is always required to create a SafeBox. If no Security Profile ID is specified, the default Security Profile associated to the user will be used.

### SecurityOptions
Builds an object to specify the security options at SafeBox creation, according to the permissions defined in the Security Profile specified in the SafeBox object.
Subset of [Safebox](#safebox) object.
By default, all attribute values are inherited from the Security Profile.
Once the SafeBox is created, all attributes are no longer editable.

Attribute                  | Definition
---------------------------|-----------
reply_enabled              | (optional) Indicates whether participants can reply or not to a SafeBox.
group_replies              | (optional) Indicates whether the Guest Participants can see each other or not in the SafeBox.
retention_period_type      | (optional) The SafeBox content retention type applied when the SafeBox is closed. Accepted values: ```discard_at_expiration```, ```retain_at_expiration```, ```do_not_discard```.
retention_period_value     | (optional) The value of the retention period.
retention_period_unit      | (optional) The unit of the retention period. Accepted values: ```hours```, ```days```, ```weeks```, ```months```, ```years```.
encrypt_message            | (optional) Indicates whether the messages within the SafeBox will be encrypted or not.
double_encryption          | (optional) Indicates whether Double Encryption is enabled or not.
expiration_value           | (contextual\*) The value of the SafeBox open period duration (after which the SafeBox is auto-closed).
expiration_unit            | (contextual\*) The unit of the SafeBox open period duration. Accepted values: ```hours```, ```days```, ```weeks```, ```months```.
expiration_date            | (contextual\*) The auto-close date of the SafeBox.
expiration_time            | (contextual\*) The auto-close time of the SafeBox.
expiration_time_zone       | (contextual\*) The time zone of the auto-close date & time of the SafeBox.
security_code_length       | (read only) The length (number of digits) of the security code sent to participants.
code_time_limit            | (read only) The validity period of the security code once it is sent to the participant.
allowed_login_attempts     | (read only) The number of login attempts that are allowed, beyond which the participant access is automatically revoked.
allow_remember_me          | (read only) Indicates whether the participant can be remembered or not on the device used to access the SafeBox.
allow_sms                  | (read only) Indicates whether the security code can be sent by SMS or not.
allow_voice                | (read only) Indicates whether the security code can be sent by voice call or not.
allow_email                | (read only) Indicates whether the security code can be sent by email or not.
two_factor_required        | (read only) Indicates whether a security code is required or not to authenticate the participant.
auto_extend_value          | (read only) The value of the SafeBox open period auto-extension when a reply is posted near the SafeBox closing date.
auto_extend_unit           | (read only) The unit of the SafeBox open period auto-extension. Accepted values: ```hours```, ```days```, ```weeks```, ```months```.
allow_manual_delete        | (read only) Indicates whether the content can be manually deleted or not after the SafeBox is closed.
allow_manual_close         | (read only) Indicates whether the SafeBox can be manually closed or not.
encrypt_attachments        | (read only) This attribute is always set to true: attachments are actually always encrypted.
consent_group_id           | (read only) The unique ID of the ConsentMessageGroup (see [ConsentMessageGroup](#consentmessagegroup) object).

\* The expiration information (SafeBox auto-close) can be set by specifying either a delay (value + unit) or an actual date (date + time + time zone).

### SecurityProfile
Represents the settings of a Security Profile.
All attributes are read only.
All attributes are composed of two properties: value and modifiable. The value field is as described below and the modifiable field indicates whether the value can be modified or not (let the user choose) at SafeBox creation.

Attribute                  | Definition
---------------------------|-----------
id                         | The unique ID of the Security Profile.
name                       | The name of the Security Profile.
description                | The description of the Security Profile.
created_at                 | The Security Profile creation date.
updated_at                 | The Security Profile last modification date.
allowed_login_attempts     | The number of login attempts that are allowed, beyond which the participant access is automatically revoked.
allow_remember_me          | Indicates whether the participant can be remembered or not on the device used to access the SafeBox.
allow_sms                  | Indicates whether the security code can be sent by SMS or not.
allow_voice                | Indicates whether the security code can be sent by voice call or not.
allow_email                | Indicates whether the security code can be sent by email or not.
code_time_limit            | The validity period of the security code once it is sent to the participant.
code_length                | The length (number of digits) of the security code sent to participants.
auto_extend_value          | The value of the SafeBox open period auto-extension when a reply is posted near the SafeBox closing date.
auto_extend_unit           | The unit of the SafeBox open period auto-extension. Accepted values: ```hours```, ```days```, ```weeks```, ```months```.
two_factor_required        | Indicates whether a security code is required or not to authenticate the participant.
encrypt_attachments        | This attribute is always set to true: attachments are actually always encrypted.
encrypt_message            | Indicates whether the messages within the SafeBox will be encrypted or not.
expiration_value           | The value of the SafeBox open period duration (after which the SafeBox is auto-closed).
expiration_unit            | The unit of the SafeBox open period duration. Accepted values: ```hours```, ```days```, ```weeks```, ```months```.
reply_enabled              | Indicates whether participants can reply or not to a SafeBox.
group_replies              | Indicates whether the Guest Participants can see each other or not in the SafeBox.
double_encryption          | Indicates whether Double Encryption is enabled or not.
retention_period_type      | The SafeBox content retention type applied when the SafeBox is closed. Accepted values: ```discard_at_expiration```,  ```retain_at_expiration```, ```do_not_discard```.
retention_period_value     | The value of the retention period.
retention_period_unit      | The unit of the retention period. Accepted values: ```hours```, ```days```, ```weeks```, ```months```, ```years```.
allow_manual_delete        | Indicates whether the content can be manually deleted or not after the SafeBox is closed.
allow_manual_close         | Indicates whether the SafeBox can be manually closed or not.
allow_for_secure_links     | Indicates whether the Security Profile can be used or not for Secure Links.
use_captcha                | Indicates whether a verification through Captcha is required for the Secure Link.
verify_email               | Indicates whether the verification of the email of the Secure Link user is required or not.
distribute_key             | Indicates whether a copy of the participant key will be sent or not by email to the SafeBox Owner when Double Encryption is enabled.
consent_group_id           | The unique ID of the ConsentMessageGroup (see [ConsentMessageGroup](#consentmessagegroup) object).


### UserSettings
Builds an object to retrieve the SendSecure options of the current user.
All attributes are read only.

Attribute                  | Definition
---------------------------|-----------
mask_note                  | Indicates whether the user wants the messages to be masked or not when accessing a SafeBox with message encryption enabled.
open_first_transaction     | Indicates whether the user wants the contents of the first SafeBox in the list to be automatically displayed or not when accessing the SendSecure interface.
mark_as_read               | Indicates whether the user wants the unread messages to be automatically marked as read or not when accessing a SafeBox.
mark_as_read_delay         | The delay (in seconds) after which the messages are automatically marked as read.
remember_key               | Indicates whether the user accepts or not that the participant key is remembered on the client side to allow subsequent accesses to SafeBoxes having Double Encryption enabled.
default_filter             | The default SafeBox list filter as defined by the user.
recipient_language         | The language in which the user needs the SafeBox recipients to be notified by email and access the SafeBox on their side.
secure_link                | The [PersonnalSecureLink](#personalsecurelink) object representing the Personal Secure Link information of the user.
created_at                 | The creation date of the user settings.
updated_at                 | The last modification date of the user settings.


# License

sendsecure-python is distributed under [MIT License](https://github.com/xmedius/sendsecure-python/blob/master/LICENSE).


# Credits

sendsecure-python is developed, maintained and supported by [XMedius Solutions Inc.](https://www.xmedius.com?source=sendsecure-python)
The names and logos for sendsecure-python are trademarks of XMedius Solutions Inc.

![XMedius Logo](https://s3.amazonaws.com/xmc-public/images/xmedius-site-logo.png)
