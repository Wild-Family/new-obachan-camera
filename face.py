from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

former_status = ""

def get_face(input_filename):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image)
        if not faces:
            return {'status': 'nobady', 'dialogue':"顔が写っとらへんで！どこに居るんや！！"}
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
        if former_status == "forward":
            return {"status": "forward again", "dialogue": "前やゆうとるやろ！！"}
        former_status = "forward"
        
        return {"status": "forward", "dialogue": "もうちょい前来てや〜！" } #顔はもう少し上に
    if (face_box[0][0]-face_box[1][0])*(face_box[1][1]-face_box[2][1]) > 600 * 600 :
        if former_status == "back":
            return {"status": "back again", "dialogue": "もうちょい後ろやゆうとるやろが！！！"}
        former_status = "back"
        return {"status": "back", "dialogue": "もうちょい後ろ下がってや〜！"} #顔はもう少し下に
    if(face_box[0][0] > 1024*1/2) :
        if former_status == "right":
            return {"status": "right again", "dialogue": "もうちょい右やて！！！"}
        former_status = "right"
        return {"status": "right", "dialogue": "もうちょい右行ってくれや〜"} #被写体は右に
    if(face_box[1][0] < 1024*1/2) :
        if former_status == "left":
            return {"status": "left again", "dialogue": "もうちょい左やて！！！"}
        former_status = "left"
        return {"status": "left", "dialogue": "もうちょい左行ってくれや〜"} #被写体は左に
    if face_box[0][1] > 768*1/2 :
        if former_status == "forward":
            return {"status": "forward again", "dialogue": "前やゆうとるやろ！！"}
        former_status = "forward"
        return {"status": "forward", "dialogue": "もうちょい前来てや〜！" } #顔はもう少し上に
    if face_box[3][1] < 768*1/2 :
        if former_status == "back":
            return {"status": "back again", "dialogue": "もうちょい後ろやゆうとるやろが！！！"}
        former_status = "back"
        return {"status": "back", "dialogue": "もうちょい後ろ下がってや〜！"} #顔はもう少し下に
    if(joyLikelihood == 1) :
        if former_status == "smile":
            return {"status": "smile again", "dialogue": "もっとええ顔しろや！笑えや！！！！"}
        former_status = "smile"
        return {"status": "smile", "dialogue": "もうちょい笑ってや〜！"} #顔はもう少し下に
    return {"status": "ok", "dialogue": "よっしゃ！撮ったるで！！"}

def check_face_loc(face_boxes,left_eyes,right_eyes,nose_tips,joyLikelihoods):
    global former_status
    print("2")
    for face_box in face_boxes:
        print(face_box)
        if(face_box[0][0] > 1024):
            if former_status == "center":
            
                return {"status": "center again", "dialogue": "お前らもっと真ん中よれや！"}
            former_status = "center"
            
            return {"status": "center", "dialogue": "みんな離れすぎや！もうちょい真ん中寄ってや〜"}
        if(face_box[1][0] < 0):
            if former_status == "center":
            
                return {"status": "center again", "dialogue": "お前らもっと真ん中よれや！"}
            former_status = "center"
            
            return {"status": "center", "dialogue": "みんな離れすぎや！もうちょい真ん中寄ってや〜"}
        if face_box[0][1] > 768:
            if former_status == "forwards":
            
                return {"status": "forward again", "dialogue": "お前ら前やゆうとるやろ！！"}
            former_status = "forwards"
            
            return {"status": "forward", "dialogue": "みんなもうちょい前来てや〜！" }
        if face_box[3][1] < 0:
            if former_status == "backs":
                return {"status": "backs again", "dialogue": "お前ら後ろやゆうとるやろ！！"}
            former_status = "backs"
            
            return {"status": "backs", "dialogue": "みんなもうちょい後ろ行ってや〜！" }
    for joyLikelihood in joyLikelihoods:
        if(joyLikelihood == 1):
            if former_status == "smiles":
                return {"status": "smiles again", "dialogue": "なんやその顔！お前ら笑えやゆうとるやろ！"}
            former_status = "smiles"
            return {"status": "smiles", "dialogue": "みんなもうちょい笑ってや〜!" }
    return {"status": "ok", "dialogue": "OKや！撮ったるで〜！！"}
