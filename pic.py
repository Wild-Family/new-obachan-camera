import picamera

def take_pic(user_id):
    save_path = './'
    pic_name = user_id + '.jpg'
    pic_loc  = save_path + pic_name
    with picamera.PiCamera() as c:
        c.resolution = (1024,768)
        c.capture(pic_loc)
    return pic_loc
