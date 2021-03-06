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

        result = Client.get_user_token(enterprise_account, username, password,
            device_id, device_name, application_type, endpoint)
        print('User token:', result['token'])
        print('User id:', result['user_id'])
    except Exception as details:
        print(details)
