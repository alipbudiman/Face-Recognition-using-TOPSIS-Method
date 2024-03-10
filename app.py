from spkmodul import Face_Reco, OpenCV2, Spk, Database


from prettytable import PrettyTable
import numpy as np
from selenium import webdriver
import cv2, pprint, time, livejson, uuid, os, threading

from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename


if Database().use_firebase:
    from spkmodul import DatabaseManager as Dbms
else:
    from spkmodul import LocalDatabaseManager as Dbms

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app_db = Dbms()
socketio = SocketIO(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def manage_session():
    session_list = app_db.get_session_list()
    print(session_list)

def clear_directory(directory_path):
    try:
        # List all files in the directory
        files = os.listdir(directory_path)

        # Iterate through the files and delete each one
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
    
    except Exception as e:
        print(f"An error occurred: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checking_same_list(list1, list2):
    for x in list1:
        if x not in list2:
            return False
    return True

@app.route('/uploads/<path:path>',methods=['GET'])
def send_assets(path):
    return send_from_directory('uploads', path)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():

    file_name = []
    unique_id = str(uuid.uuid4() )+ "-" + str(time.time()).replace(".", "")
    os.mkdir(f'uploads/{unique_id}')

    for i in range(4):
        file_key = 'image' + str(i + 1)
        if file_key in request.files:
            file = request.files[file_key]
            if file.filename == '':
                os.rmdir(f'uploads/{unique_id}')
                return jsonify({
                    "status":500,
                    "message": 'Please upload image !'
                })
            
            # Save the file to the desired location or perform further processing
            s_file_name = secure_filename(file.filename)
            file.save(f'uploads/{unique_id}/{s_file_name}')
            file_name.append(s_file_name)
        else:
            os.rmdir(f'uploads/{unique_id}')
            return jsonify({
                "status":400,
                "message": f'Error: {file_key} not found in request'
            })
    
    app_db.save_session(unique_id, file_name)
    return redirect(f"/process?uuid={unique_id}")
    

@app.route("/process")
def process():
    return render_template("analyze.html")


@socketio.on('message_from_server')
def handle_message(uuid):
    time.sleep(1)
    try:files = os.listdir(f"uploads/{uuid}")
    except FileNotFoundError as e:
        socketio.emit('message_from_server', str(e))
        time.sleep(2.5)
        socketio.emit('redirect_client', "/")
        return
        

    sessionID = app_db.get_session_detail(uuid)
    if sessionID is None:
        try:os.rmdir(f"uploads/{uuid}")
        except:pass
        socketio.emit('message_from_server', "[113] Session Unknow or Expired!")
        time.sleep(2.5)
        socketio.emit('redirect_client', "/")
        return

    if not sessionID["process"]:
        app_db.session_update_proc_status(uuid)
    else:
        try:app_db.remove_session(uuid)
        except:pass
        try:os.rmdir(f"uploads/{uuid}")
        except:pass
        socketio.emit('message_from_server', "[117] Session Unknow or Expired!")
        time.sleep(2.5)
        socketio.emit('redirect_client', "/")
        return

    if sessionID is None:   
        socketio.emit('message_from_server', "[132] Session Unknow or Expired!")
        time.sleep(2.5)
        socketio.emit('redirect_client', "/")
        return
    
    if not checking_same_list(files, sessionID["files"]):
        
        os.rmdir(f"uploads/{uuid}")
        socketio.emit('message_from_server', "[140] Images Files Not Found. Please Try Again!")
        time.sleep(2.5)
        socketio.emit('redirect_client', "/")
        return

    images_compair = f'uploads/{uuid}/{(sessionID["files"])[0]}'
    images_list = [f'uploads/{uuid}/{(sessionID["files"])[1]}',f'uploads/{uuid}/{(sessionID["files"])[2]}',f'uploads/{uuid}/{(sessionID["files"])[3]}']

    imageA = cv2.imread(images_compair)
    images = [cv2.imread(images_list[0]), cv2.imread(images_list[1]), cv2.imread(images_list[2])]

    data = {
        "mse":[],
        "avg_standart_deviasi_1":[],
        "avg_standart_deviasi_2":[],
        "face_distances":[],
        "ml_detection":[]
    }


    for i, image in enumerate(images):
        time.sleep(1)
        socketio.emit('message_from_server', f"Compair Image A with Image {chr(66+i)} ")
        mse, mean1, std1, mean2, std2 = OpenCV2().calculate_similarity(imageA, image)
        res, fd = Face_Reco().FaceRecognition(images_compair, images_list[i])
        data["mse"].append(mse)
        time.sleep(1)
        socketio.emit('message_from_server', f"Image {chr(66+i)} Minimum Square Error: {mse}")
        
        
        data["avg_standart_deviasi_1"].append(float(mean2 - mean1))
        time.sleep(1)
        socketio.emit('message_from_server', f"Image {chr(66+i)} Average Standar Deviation 1: {float(mean2 - mean1)}")
        
        
        data["avg_standart_deviasi_2"].append(float(std1 - std2))
        time.sleep(1)
        socketio.emit('message_from_server', f"Image {chr(66+i)} Average Standar Deviation 2: {float(std1 - std2)}")
        
        
        data["face_distances"].append(float(fd))
        time.sleep(1)
        socketio.emit('message_from_server', f"Image {chr(66+i)} Average Face Distance: {float(fd)}")
        data["ml_detection"].append(res)

    matrix = {
        "a1":[],
        "a2":[],
        "a3":[],
    }

    pt = PrettyTable()
    pt.field_names = ["No","IMAGE", "MSE", "AVG STD DEVIATION 1", "AVG STD DEVIATION 2", "FACE DISTANCE", "ML DETECTION (IS SAME PERSON)"]
    for i, x in enumerate(images_list):
        mtrx = [
            (data["mse"])[i],
            (data["avg_standart_deviasi_1"])[i],
            (data["avg_standart_deviasi_2"])[i],
            (data["face_distances"])[i],
            (data["ml_detection"])[i],
        ]
        matrix[f"a{i + 1}"] = [
            (data["mse"])[i],
            (data["avg_standart_deviasi_1"])[i],
            (data["avg_standart_deviasi_2"])[i],
            (data["face_distances"])[i],
        ]

        pt.add_row([i + 1, x.split("/")[2]] + mtrx)
    
    pre = pt.get_string()
    socketio.emit('message_from_server', f"<pre>{pre}</pre>")
    spk, ref_rank = Spk().topsis(matrix)
    
    for x in spk:
        time.sleep(1)
        socketio.emit('message_from_server', f"<pre>{x}</pre>")

    rank_data = {}

    for y, rnk in enumerate(list(ref_rank)):
        i = int(rnk[1:])
        rank_data.update({
            f"rank{y+1}":{
                "image_id":f"image {chr(66+ i - 1)}",
                "image_path":f'{uuid}/{(sessionID["files"])[i]}',
                "mse":(data["mse"])[i-1],
                "avg_standart_deviasi_1":(data["avg_standart_deviasi_1"])[i-1],
                "avg_standart_deviasi_2":(data["avg_standart_deviasi_2"])[i-1],
                "face_distances":(data["face_distances"])[i-1],
                "ml_detection_is_same_person":(data["ml_detection"])[i-1],
                "refrence_point":ref_rank[rnk]
            }
        })
    
    socketio.emit('client_rank', rank_data)

    os.rmdir(f'uploads/{uuid}')

if __name__ == "__main__":
    app.run(port=5005,debug=False)
    
    