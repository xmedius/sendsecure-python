**XMediusSENDSECURE (SendSecure)** is a collaborative file exchange platform that is both highly secure and simple to use.
It is expressly designed to allow for the secured exchange of sensitive documents via virtual SafeBoxes.

SendSecure comes with a **Web API**, which is **RESTful**, uses **HTTPs** and returns **JSON**.

Specific libraries have been published for various languages:
[C#](https://github.com/xmedius/sendsecure-csharp),
[Java](https://github.com/xmedius/sendsecure-java),
[JavaScript](https://github.com/xmedius/sendsecure-js),
[PHP](https://github.com/xmedius/sendsecure-php),
**Python**
and
[Ruby](https://github.com/xmedius/sendsecure-ruby).

# sendsecure-python

**This library allows you to use the SendSecure Web API via Python.**

With this library, you will be able to:
* Authenticate SendSecure users
* Create new SafeBoxes

# Table of Contents

* [Installation](#installation)
* [Quick Start](#quickstart)
* [Usage](#usage)
* [License](#license)
* [Credits](#credits)

<a name="installation"></a>
# Installation

## Prerequisites

- Python version 2.7, 3.4 or 3.5
- The SendSecure service, provided by [XMedius](https://www.xmedius.com/en/products?source=sendsecure-python) (demo accounts available on demand)

## Install Package

```python
TBD
```

<a name="quickstart"></a>
# Quick Start

## Authentication (Retrieving API Token)

Authentication is done using an API Token, which must be first obtained based on SendSecure enterprise account and user credentials.
Here is the minimum code to get such a user-based API Token.

```python
from SendSecure import *
endpoint = 'https://portal.xmedius.com'
token = Client.get_user_token('deathstar', 'darthvader', 'd@Rk$1De', endpoint)
```

## SafeBox Creation

Here is the minimum required code to create a SafeBox – with 1 recipient, a subject, a message and 1 attachment.
This example uses the user's *default* security profile (which requires to be set in the account).

### With SafeBox Helper Class

```python
    try:
        user_email = 'darthvader@empire.com'
        token = 'USER|e0c1cf59-c047-4545-9d6f-bb810b36ae4f'
        enterprise_account = 'deathstar'
        endpoint = 'https://portal.xmedius.com'

        safebox = Safebox(user_email)
        safebox.subject = 'Family matters'
        safebox.message = 'Son, you will find attached the evidence.'

        recipient = Recipient('lukeskywalker@rebels.com')
        safebox.recipients.append(recipient)

        attachment = Attachment('Birth_Certificate.pdf', 'application/pdf')
        safebox.attachments.append(attachment)

        client = Client(token, enterprise_account, endpoint)
        safebox_response = client.submit_safebox(safebox)
    except Exception, details:
        print details
```

<!-- ### Without SafeBox Helper Class

```python
TBD
```
 -->
<a name="usage"></a>
# Usage

## Helper Methods

### Get User Token
```
get_user_token(enterprise_account, username, password, device_id, device_name, application_type, endpoint, one_time_password)
```
Creates and returns an API Token for a specific user within a SendSecure enterprise account.
Calling this method again with the exact same params will always return the same Token.

Param              | Type   | Definition
-------------------|--------|-----------
enterprise_account | String | The SendSecure enterprise account
username           | String | The username of a SendSecure user of the current enterprise account
password           | String | The password of this user
device_id          | String | The unique ID of the device used to get the Token 
device_name        | String | The name of the device used to get the Token
application_type   | String | The type/name of the application used to get the Token ("SendSecure Python" will be used by default if empty)
endpoint           | String | The URL to the SendSecure service ("https://portal.xmedius.com" will be used by default if empty)
one_time_password  | String | The one-time password of this user (if any)

### Client Object Constructor
```
__init__(self, api_token, enterprise_account, endpoint, locale)
```

Param              | Type   | Definition
-------------------|--------|-----------
api_token          | String | The API Token to be used for authentication with the SendSecure service
enterprise_account | String | The SendSecure enterprise account
endpoint           | String | The URL to the SendSecure service ("https://portal.xmedius.com" will be used by default if empty)
locale             | String | The locale in which the server errors will be returned ("en" will be used by default if empty)

### Get Enterprise Settings
```
get_enterprise_settings(self)
```
Returns all values/properties of the enterprise account's settings specific to SendSecure.

### Get Default Security Profile
```
get_default_security_profile(self, user_email)
```
Returns the default security profile (if it has been set) for a specific user, with all its setting values/properties.

Param      | Type   | Definition
-----------|--------|-----------
user_email | String | The email address of a SendSecure user of the current enterprise account

### Get Security Profiles
```
get_security_profiles(self, user_email)
```
Returns the list of all security profiles available to a specific user, with all their setting values/properties.

Param      | Type   | Definition
-----------|--------|-----------
user_email | String | The email address of a SendSecure user of the current enterprise account

### Initialize SafeBox
```
initialize_safebox(self, safebox)
```
Pre-creates a SafeBox on the SendSecure system and returns the updated Safebox object with the necessary system parameters filled out (GUID, public encryption key, upload URL).

Param      | Type    | Definition
-----------|---------|-----------
safebox    | Safebox | A Safebox object to be initialized by the SendSecure system

### Upload Attachment
```
upload_attachment(self, safebox, attachment)
```
Uploads the specified file as an Attachment of the specified SafeBox and returns the updated Attachment object with the GUID parameter filled out.

Param       | Type       | Definition
------------|------------|-----------
safebox     | Safebox    | An initialized Safebox object
attachment  | Attachment | An Attachment object - the file to upload to the SendSecure system

### Commit SafeBox
```
commit_safebox(self, safebox)
```
Finalizes the creation (commit) of the SafeBox on the SendSecure system.
This actually "Sends" the SafeBox with all content and contact info previously specified.

Param      | Type    | Definition
-----------|---------|-----------
safebox    | Safebox | A Safebox object already initialized, with security profile, recipient(s), subject and message already defined, and attachments already uploaded. 

### Submit SafeBox
```
submit_safebox(self, safebox)
```
This method is a high-level combo that initializes the SafeBox, uploads all attachments and commits the SafeBox.

Param      | Type    | Definition
-----------|---------|-----------
safebox    | Safebox | A non-initialized Safebox object with security profile, recipient(s), subject, message and attachments (not yet uploaded) already defined. 


## Helper Modules

### Safebox

### SafeboxResponse

### Attachment

### Recipient

### ContactMethod

### SecurityProfile

### EnterpriseSettings

### ExtensionFilter

<a name="license"></a>
# License

sendsecure-python is distributed under [MIT License](https://github.com/xmedius/sendsecure-python/blob/master/LICENSE).

<a name="credits"></a>
# Credits

sendsecure-python is developed, maintained and supported by [XMedius Solutions Inc.](https://www.xmedius.com?source=sendsecure-python)
The names and logos for sendsecure-python are trademarks of XMedius Solutions Inc.

![XMedius Logo](https://s3.amazonaws.com/xmc-public/images/xmedius-site-logo.png)
