from azure.servicebus import ServiceBusService, Message, Queue
import os, sys
import json
sys.path.append(os.getcwd())
import settings


bus_service = ServiceBusService(
    service_namespace='linebot-test',
    shared_access_key_name=settings.SHARED_ACCESS_KEY_NAME,
    shared_access_key_value=settings.SHARED_ACCESS_KEY
    )
bus_service.create_queue('test')

def get_message():
    msg = bus_service.receive_queue_message('test', peek_lock=False, timeout=20)
    if msg is not None and msg.body is not None:
        dic = json.loads(msg.body.decode('utf8'))
        return dic
    else:
        print('message queue time out?')
        return None

def main():
    while(True):
        msg = get_message()
        if msg is None:
            print("all queue might have been deleted?")
            break
        print(msg)

if __name__ == '__main__':
    main()