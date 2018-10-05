from azure.servicebus import ServiceBusService, Message, Queue
import settings
import time
import requests
import json
import sys

start_url = '/user/{userId}/start'
staus_url = '/user/{userId}/status'
post_url  = '/user/{userId}/post' 


bus_service = ServiceBusService(
    service_namespace='linebot-test',
    shared_access_key_name=settings.SHARED_ACCESS_KEY_NAME,
    shared_access_key_value=settings.SHARED_ACCESS_KEY
    )
bus_service.create_queue('test')


def get_message():
    msg = bus_service.receive_queue_message('test', peek_lock=True)
    if msg is not None:
        dic = json.loads(msg.body.decode('utf8'))
        return dic
    else:
        print('message queue time out?')
        return None


def request_get(url, user_id, params=''):
    res = requests.get(url.format(userId=user_id), params=params)
    if res.status_code == 200:
        dic = json.loads(res.json())
        return dic
    else:
        print('[Error]: {0} of status code is not 200 '.format(url))
        sys.exit(1)
    
def request_post_with_image(url, user_id, pic_loc):
    files = {'pic': open(pic_loc, "rb")}
    res = requests.post(url.format(userId=user_id), files=files)
      if res.status_code == 200:
        dic = json.loads(res.json())
        return dic
    else:
        print('[Error]: {0} of status code is not 200 '.format(url))
        sys.exit(1)


if __name__ == "__main__":
    user_id　=　None
    display_name = None
    take_flag = False

    while True:
        # Getting message from MQ
        message_dic = get_message()
        if message_dic is None:
            continue
        else:
            user_id = message_dic['user_id']

        # Getting display_name,, and Informimg server of taking picture
        start_dic = request_get(start_url, user_id)
        display_name = start_dic['display_name']
        
       # Informimg picture status 
        while not take_flag:
              status = get_face()
              if status == "OK":
                  take_flag = True
              # GET request with params
              params = { 'status': status } #example: {'statius'; 'right'}
              status_dic = request_get(status_url, user_id, params)

        # Taking 本番 picture
        if take_flag:
            pic_loc = take_pic()
            post_dic = request_post_with_image(post_url, user_id, pic_loc)
            #message = post_dic['message']
            take_flag = True
        
        time.sleep(1)
        
        
        
        
    
    
