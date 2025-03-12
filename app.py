import cv2
import time
import numpy as np
from flask import Flask, Response, render_template
import os

try:
    from pyngrok import ngrok
    NGROK_AVAILABLE = True
except ImportError:
    NGROK_AVAILABLE = False

app = Flask(__name__)

camera = None

def create_error_frame(message):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    text_size = cv2.getTextSize(message, font, font_scale, thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2
    cv2.putText(frame, message, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
    ret, buffer = cv2.imencode('.jpg', frame)
    return buffer.tobytes()

def get_camera():
    global camera
    if camera is None:
        try:
            camera = cv2.VideoCapture(0)  # 可能需要调整索引，如 /dev/video0
            if not camera.isOpened():
                print("错误：无法访问摄像头设备，请检查设备连接和权限设置")
                return None
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        except Exception as e:
            print(f"初始化摄像头时发生错误: {str(e)}")
            return None
    return camera

def generate_frames():
    while True:
        camera = get_camera()
        if camera is None:
            error_frame = create_error_frame("无法访问摄像头设备")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + error_frame + b'\r\n')
            time.sleep(5)
            continue
        
        success, frame = camera.read()
        if not success:
            error_frame = create_error_frame("读取摄像头数据失败")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + error_frame + b'\r\n')
            time.sleep(1)
            continue
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def start_ngrok():
    if not NGROK_AVAILABLE:
        print("警告: 未安装 pyngrok，跳过 NGROK 内网穿透。")
        return None
    
    ngrok_auth_token = os.environ.get('NGROK_AUTH_TOKEN', None)
    
    # 尝试读取本地配置文件
    if not ngrok_auth_token:
        try:
            with open('.ngrok_token', 'r') as f:
                ngrok_auth_token = f.read().strip()
        except Exception as e:
            print(f"读取配置文件失败: {str(e)}")
    
    if not ngrok_auth_token:
        print("警告: 未设置NGROK_AUTH_TOKEN环境变量且缺少.ngrok_token文件")
        return None
    
    ngrok.set_auth_token(ngrok_auth_token)
    public_url = ngrok.connect(5000).public_url
    # print(f" * 通过 ngrok 访问: {public_url}")
    return public_url

if __name__ == '__main__':
    use_ngrok = os.environ.get('USE_NGROK', 'True').lower() in ['true', '1', 't']
    
    if use_ngrok:
        public_url = start_ngrok()
        if public_url:
            print(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
            print(f" *  外网访问链接: {public_url}   * ")
            print(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
