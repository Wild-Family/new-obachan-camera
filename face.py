from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

def get_face(input_filename):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image)
        if not faces:
            return "nobody"
        image.seek(0)
        return highlight_faces(image, faces)


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
    if (face_box[0][0]-face_box[1][0])*(face_box[1][1]-face_box[2][1]) < 150 * 150 :
        if former_status == "forward":
            
            return "forward again"
        former_status = "forward"
        
        return "forward" #顔はもう少し上に
    if (face_box[0][0]-face_box[1][0])*(face_box[1][1]-face_box[2][1]) > 600 * 600 :
        if former_status == "back":
            
            return "back again"
        former_status = "back"
        
        return "back" #顔はもう少し下に
    if(face_box[0][0] > 1024*1/2) :
        if former_status == "right":
            
            return "right again"
        former_status = "right"
        
        return "right" #被写体は右に
    if(face_box[1][0] < 1024*1/2) :
        if former_status == "left":
            
            return "left again"
        former_status = "left"
        
        return "left" #被写体は左に
    if face_box[0][1] > 768*1/2 :
        if former_status == "forward":
        
            return "forward again"
        former_status = "forward"
        
        return "forward" #顔はもう少し上に
    if face_box[3][1] < 768*1/2 :
        if former_status == "back":
        
            return "back again"
        former_status = "back"
        
        return "back" #顔はもう少し下に
    if(joyLikelihood == 1) :
        if former_status == "smile":
        
            return "smile again"
        former_status = "smile"
        print("笑顔になって")
        
        return "smile"
    return "os"

def check_face_loc(face_boxes,left_eyes,right_eyes,nose_tips,joyLikelihoods):
    global former_status
    print("2")
    for face_box in face_boxes:
        print(face_box)
        if(face_box[0][0] > 1024):
            if former_status == "center":
                center_again.play()
                return "center again"
            former_status = "center"
            center.play()
            return "center"
        if(face_box[1][0] < 0):
            if former_status == "center":
                center_again.play()
                return "center again"
            former_status = "center"
            center.play()
            return "center"
        if face_box[0][1] > 768:
            if former_status == "forwards":
                forwards_again.play()
                return "forwards again"
            former_status = "forwards"
            forwards.play()
            return "forwards"
        if face_box[3][1] < 0:
            if former_status == "backs":
                backs_again.play()
                return "backs again"
            former_status = "backs"
            backs.play()
            return "backs"
    for joyLikelihood in joyLikelihoods:
        if(joyLikelihood == 1):
            if former_status == "smiles":
                smiles_again.play()
                return "smiles again"
            former_status = "smiles"
            smiles.play()
            return "smiles"
    return "ok"
