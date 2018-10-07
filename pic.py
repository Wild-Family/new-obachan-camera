import picamera
import os
import datetime

def take_pic(user_id):
    save_path = './'
    pic_name = user_id
    time = str(datetime.datetime.now())
    pic_loc  = save_path + pic_name + time + '.jpg'
    with picamera.PiCamera() as c:
        c.resolution = (1024,768)
        c.capture(pic_loc)
    return pic_loc

def remove_pic(user_id):
    save_path = './'
    pic_name = user_id
    pic_loc = save_path + pic_name
    res = os.remove(pic_loc)
