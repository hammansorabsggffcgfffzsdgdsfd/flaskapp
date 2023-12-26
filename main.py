from flask import Flask, render_template, Response, request
from camera import VideoCamera


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/upload', methods=['POST'])#from api flutter
def upload_image():
  file = request.files['file']
  file.save('uploaded_file.jpg')  # Or handle video format
  return 'File uploaded successfully!'



@app.route('/realtime', methods=['POST'])#from api flutter
def upload_image_realtime():
  file = request.files['file']
  file.save('uploaded_file.jpg')  # Or handle video format
  return 'File uploaded successfully!'



@app.route('/dashboard', methods=['GET'])#from api flutter
def dashboard():
  file = request.files['file']
  file.save('uploaded_file.jpg')  # Or handle video format
  return 'File uploaded successfully!'



if __name__ == '__main__':
    app.run()
    
    # app.run(host='localhost', debug=True)
