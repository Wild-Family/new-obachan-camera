from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

import dialogue

former_status = ""

def get_face(input_filename):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image)
        if not faces:
            dialogue.play_audio("nobody")
            return {'status': 'nobody', 'dialogue': dialogue.get_dialogue("nobody")}
        image.seek(0)
        face_status = highlight_faces(image, faces)
        return face_status

def detect_face(face_file, max_results=4):
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = types.Image(content=content)
    return client.face_detection(image=image).face_annotations

def highlight_faces(image, faces):
    if len(faces) == 1:
        box = None
        left_eye = None
        right_eye = None
        nose_tip = None
        joyLikelihood = None
        for face in faces:
            left_eye =  face.landmarks[0].position
            right_eye = face.landmarks[1].position
            nose_tip =  face.landmarks[7].position
            joyLikelihood = face.joy_likelihood
            box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
        return check_face_loc_lonely(box,left_eye,right_eye,nose_tip,joyLikelihood)
    else:
        box             = []
        left_eye        = []
        right_eye       = []
        nose_tip        = []
        joyLikelihood   = []
        for value in faces:
            left_eye.append(value.landmarks[0].position)
            right_eye.append(value.landmarks[1].position)
            nose_tip.append(value.landmarks[7].position)
            joyLikelihood.append(value.joy_likelihood)
            box.append([(vertex.x, vertex.y) for vertex in value.bounding_poly.vertices])
        return check_face_loc(box,left_eye,right_eye,nose_tip,joyLikelihood)

def check_face_loc_lonely(face_box,left_eye,right_eye,nose_tip,joyLikelihood):
    global former_status
    print(former_status)
    if (face_box[0][0]-face_box[1][0])*(face_box[1][1]-face_box[2][1]) < 150 * 150 :
        status = "forward"
        result = play_audio(status)
        return result #顔はもう少し上に
    if (face_box[0][0]-face_box[1][0])*(face_box[1][1]-face_box[2][1]) > 600 * 600 :
        status = "back"
        result = play_audio(status)
        return result
    if(face_box[0][0] > 1024*1/2) :
        status = "right"
        result = play_audio(status)
        return result #被写体は右に
    if(face_box[1][0] < 1024*1/2) :
        status = "left"
        result = play_audio(status)
        return result #被写体は左に
    if face_box[0][1] > 768*1/2 :
        status = "forward"
        result = play_audio(status)
        return result #顔はもう少し上に
    if face_box[3][1] < 768*1/2 :
        status = "back"
        result = play_audio(status)
        return result #顔はもう少し下に
    if(joyLikelihood == 1) :
        status = "smile"
        result = play_audio(status)
        return result #顔はもう少し下に
    result = play_audio("ok")
    return result

def check_face_loc(face_boxes,left_eyes,right_eyes,nose_tips,joyLikelihoods):
    global former_status
    print("2")
    for face_box in face_boxes:
        print(face_box)
        if(face_box[0][0] > 1024):
            status = "center"
            result = play_audio(status)
            return result
        if(face_box[1][0] < 0):
            status = "center"
            result = play_audio(status)
            return result
        if face_box[0][1] > 768:
            status = "forwards"
            result = play_audio(status)
            return result
        if face_box[3][1] < 0:
            status = "backs"
            result = play_audio(status)
            return result
    for joyLikelihood in joyLikelihoods:
        if(joyLikelihood == 1):
            status = "smiles"
            result = play_audio(status)
            return result
    result = play_audio("ok")
    return result

def play_audio(status):
    global former_status
    if former_status == status:
        status += " again"
    else:
        former_status = status
    text = dialogue.get_dialogue(status)
    dialogue.play_audio(status)
    
    return {"status": status, "dialogue": text}