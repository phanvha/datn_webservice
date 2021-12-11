
def send_fcm(fcm_tokens, title=None, body=None, data_message=None):
    push_service = FCMNotification(api_key=app.config['FCM_KEY'])
    try:
        if type(fcm_tokens) is list:
            print(fcm_tokens, data_message)
            result = push_service.notify_multiple_devices(registration_ids=fcm_tokens, data_message=data_message)
            print(result, '++++++++++++++', flush=True)
        else:
            print(fcm_tokens, 'single device', data_message)
            result = push_service.notify_single_device(registration_id=fcm_tokens, data_message=data_message)
            print(result, flush=True)
    except errors.InvalidDataError as e:
        print(e, flush=True)