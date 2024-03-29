# 这是一个非常简单的使用Web服务上传图片运行人脸识别的案例，后端服务器会识别这张图片是不是奥巴马，并把识别结果以json键值对输出
# 比如：运行以下代码
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
# 会返回：
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# 本项目基于Flask框架的案例 http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# 提示：运行本案例需要安装Flask，你可以用下面的代码安装Flask
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # 检测图片是否上传成功
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            print(f"pony: **************** upload filename is {file.filename}******************")
            # 图片上传成功，检测图片中的人脸
            return detect_faces_in_image(file)

    # 图片上传失败，输出以下html代码
    return '''
    <!doctype html>
    <title>Is this a picture of Obama?</title>
    <h1>Upload a picture and see if it's a picture of Obama!</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''


def detect_faces_in_image(file_stream):
    
    # 载入用户上传的图片
    img = face_recognition.load_image_file(file_stream)
    
    shape = img.shape
    
    img_width = shape[0]
    
    img_height = shape[1]
    
    #图像宽度和高度
    print(f"pony: img.width is {img_width},height is {img_height}")
    
    #定位第一个人脸   这里要做异常校验
    
    face_locations = face_recognition.face_locations(img)
    
    print(f"pony: face_locations is  {face_locations}")
    
    if face_locations == []:
            
        print(f"pony: there is no face in the img")    
        
        return "there is no face in the img"
        
    if len(face_locations) >1 :
            
        print(f"pony: there is more than one face in the img")    
        
        return "there is more than one face in the img"    
        
    face_width = face_locations[0][2]-face_locations[0][0]

    face_height = face_locations[0][1]-face_locations[0][3]
    
    print(f"pony: face_width is  {face_width},face_height is {face_height}")
        
    if face_width < img_width/5 and face_height < img_height/5 :
            
        print(f"pony: face area is too small")    
        
        return "face area is too small"      
 
    face_landmarks_list = face_recognition.face_landmarks(img,face_locations=face_locations)
    
    print(f"pony: face_landmarks_list is \n {face_landmarks_list}")

    # 讲识别结果以json键值对的数据结构输出

    return jsonify(face_landmarks_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
