from azure.servicebus import ServiceBusService, Message, Queue
import os, sys
import json
sys.path.append(os.getcwd())
import settings

sbs = ServiceBusService(
    service_namespace='linebot-test',
    shared_access_key_name=settings.SHARED_ACCESS_KEY_NAME,
    shared_access_key_value=settings.SHARED_ACCESS_KEY
    )
sbs.create_queue('test')
msg_dict = {
	'user_id': '12345abcde'
}
msg_json = json.dumps(msg_dict, indent=4)
msg = Message(msg_json)
sbs.send_queue_message('test', msg)