from azure.servicebus import ServiceBusService, Message, Queue
import settings
import time
import requests
import json
import sys
import face
import pic
import dialogue


start_url = 'https://new-obachan-bot.herokuapp.com/user/{userId}/start'
status_url = 'https://new-obachan-bot.herokuapp.com/user/{userId}/status'
post_url  = 'https://new-obachan-bot.herokuapp.com/user/{userId}/post' 

bus_service = ServiceBusService(
    service_namespace='linebot-test',
    shared_access_key_name=settings.SHARED_ACCESS_KEY_NAME,
    shared_access_key_value=settings.SHARED_ACCESS_KEY
    )
bus_service.create_queue('test')

def get_message():
    msg = bus_service.receive_queue_message('test', peek_lock=True)
    if msg is not None and msg.body is not None:
        dic = json.loads(msg.body.decode('utf8'))
        return dic
    else:
        print('message queue time out?')
        return None

def pop_message():
    msg = bus_service.receive_queue_message('test', peek_lock=False)
    if msg is not None and msg.body is not None:
        dic = json.loads(msg.body.decode('utf8'))
        return dic
    else:
        print('message queue time out?')
        return None

def request_get(url, user_id, params=''):
    res = requests.get(url.format(userId=user_id), params=params)
    if res.status_code == 200:
        dic = res.json()
        return dic
    else:
        print('[Error]: {0} of status code is not 200({1}). '.format(url.format(userId=user_id), res.status_code))
        sys.exit(1)
    
def request_post_with_image(url, user_id, pic_loc):
    files = {'pic': open(pic_loc, "rb")}
    res = requests.post(url.format(userId=user_id), files=files)
    if res.status_code == 200:
        dic = res.json()
        return dic
    else:
        print('[Error]: {0} of status code is not 200 '.format(url))
        sys.exit(1)

if __name__ == "__main__":
    user_id = None
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
        print(start_dic)
        display_name = start_dic['display_name']

        dialogue.call_my_name(display_name)
        
       # Informimg picture status and dialogue
        while not take_flag:
            pic_loc = pic.take_pic(user_id)  
            face_info = face.get_face(pic_loc)
            print(face_info)
            if face_info['status'] == "ok":
                take_flag = True
            else:
                pic.remove_pic(pic_loc)
            # GET request with params
            status_dic = request_get(status_url, user_id, face_info)

        # Taking 本番 picture
        if take_flag:
            dialogue.count_down()
            pic_loc = pic.take_pic(user_id)
            post_dic = request_post_with_image(post_url, user_id, pic_loc)
            dialogue.play_audio("end")
            #message = post_dic['message']
            take_flag = False
            pop_message()
            pic.remove_pic(pic_loc)
        
        time.sleep(1)
