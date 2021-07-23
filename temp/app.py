from flask import Flask, redirect, url_for, render_template, request,make_response
import os.path
from os import path
# import main2
import os
app = Flask(__name__,static_folder="../build",static_url_path="/",template_folder="../build")
import SbiClass
# option1 = Options()
# option1.add_argument("--disable-notifications")

path = os.getcwd()
path=path+"/chromedriver"
obj = SbiClass.SBI()
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')
@app.route('/')
def index():
    return app.send_static_file('index.html')
    
@app.route('/api/submitCaptcha', methods=['POST'])
def home():
    val= request.get_json()
    success = obj.cap(val['cap'])
    return {"code" : str(success)}

@app.route("/api/checkCaptcha", methods=['GET'])
def checkCap():
    if str(os.path.exists("captcha.png")) == "True":
        import base64
        with open("captcha.png", "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        return {'image':str(my_string)}
    return {'image':"0"}

@app.route('/api/submitOtp', methods=['POST'])
def OTP():
    val= request.get_json()
    success =  obj.otp(val['OTP'])
    return {"code": str(success)}

@app.route('/api/loop3', methods=['POST'])
def loopIt():
    val= request.get_json()
    obj.loop3()
    return {"code":"success"}

@app.route("/api/runScript", methods=['GET'])
def start():
    obj.start()
    return {"code":"success"}

@app.route("/api/getImg", methods=['GET'])
def test():
    import base64
    with open("captcha.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    return {'image':str(my_string)}

@app.route("/api/status", methods=['GET'])
def st():
    st = obj.sessionVal()
    return {'st':str(st)}

if __name__ == "__main__":
    app.run(debug=False)