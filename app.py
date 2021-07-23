from werkzeug.utils import send_from_directory
import SbiClass
from flask import Flask, redirect, url_for, render_template, request, make_response
import os.path
from os import path
# import main2
import os
app = Flask(__name__,static_folder="frontend/build",static_url_path="/", template_folder="frontend/build")
# app.config['SERVER_NAME'] = "https://bank-automation.herokuapp.com/"
# option1 = Options()
# option1.add_argument("--disable-notifications")
# static_folder="frontend/build",static_url_path="/", template_folder="frontend/build"
path = os.getcwd()
path = path+"/chromedriver"
obj = SbiClass.SBI()
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')


@app.route('/api/submitCaptcha', methods=['POST'])
def home():
    val = request.get_json()
    success = obj.cap(val['cap'])
    return {"code": str(success)}


@app.route("/api/checkCaptcha", methods=['GET'])
def checkCap():
    if str(os.path.exists("captcha.png")) == "True":
        import base64
        with open("captcha.png", "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        return {'image': str(my_string)}
    return {'image': "0"}


@app.route('/api/submitOtp', methods=['POST'])
def OTP():
    val = request.get_json()
    success = obj.otp(val['OTP'])
    return {"code": str(success)}


@app.route('/api/loop3', methods=['POST'])
def loopIt():
    val = request.get_json()
    obj.loop3()
    return {"code": "success"}


@app.route('/api/changeDetails', methods=['POST'])
def changeSettings():
    val = request.get_json()
    obj.updateSettings(idd=val['idVal'], passs=val['passVal'])
    return {"code": "1"}


@app.route("/api/runScript", methods=['GET'])
def start():
    ans = 1
    if str(os.path.exists("captcha.png")) == "True":
        os.remove("captcha.png")
    if obj.checkCred() == 1:
        obj.start()
    else:
        ans = 0
    return {"code": str(ans)}


@app.route("/api/getDashboard", methods=['POST'])
def sbiVal():
    val = request.get_json()
    gdate = str(val['Date'])+'-'+str(val['Month'])+'-'+str(val['Year'])
    print(gdate)
    ans = SbiClass.history(gdate=gdate)
    print(ans)
    return {"code": str(ans)}


@app.route("/api/getImg", methods=['GET'])
def test():
    import base64
    with open("captcha.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    return {'image': str(my_string)}


@app.route("/api/status", methods=['GET'])
def st():
    st = obj.sessionVal()
    return {'st': str(st)}


@app.route("/", methods=['GET'])
def index():
    # return "hello"
    return app.send_static_file("index.html")
if __name__ == "__main__":
    app.run(debug=False)
