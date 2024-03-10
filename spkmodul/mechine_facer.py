import face_recognition

class Face_Reco:
    def __init__(self) -> None:
        pass
    
    def FaceRecognition(self, img_compair, img, tolerance=0.4):
        image_compair = face_recognition.load_image_file(img_compair)
        image = face_recognition.load_image_file(img)
        try:
            face_encoding_compair = face_recognition.face_encodings(image_compair)[0]
            face_encoding = face_recognition.face_encodings(image)[0]
        except IndexError:
            raise Exception("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        
        results = face_recognition.compare_faces([face_encoding_compair], face_encoding, tolerance=tolerance)
        face_distances = face_recognition.face_distance([face_encoding_compair], face_encoding)
        return self.InsteadYesOrNo(results[0]), face_distances
    
    def InsteadYesOrNo(self, data):
        if data:return "Yes"
        else:return "No"