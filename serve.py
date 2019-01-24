from flask import send_file, Flask, send_from_directory, render_template, jsonify
from flask_api import status
from flask_cors import CORS
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

import base64
app = Flask(__name__)
CORS(app)

# users_ref = db.collection('users').document('userid1').get()
# print(users_ref.get('isActive'))
# db.collection('users').document('userid1').set({'isActive' : True}, merge=True)

# def addDriverListener():
# 	while True:
# 		try : 
# 			driver.find_element_by_tag_name('body')
# 			print("Its' good")
# 		except InvalidSessionIdException :
# 			print('InvalidSessionIdException')
# 		except WebDriverException : 
# 			print('WebDriverException')
# 		except Exception as e :
# 			print('#####################failed')
# 		time.sleep(2)

def firebaseSetup():
	global db 
	# Use a service account
	cred = credentials.Certificate('./wtsapproject-cd387d40d4a1.json')
	firebase_admin.initialize_app(cred)
	db = firestore.client()


# @app.route('/image')
# def get_image():
# 	filename = 'qr_code.png'
# 	with open(filename, "rb") as image_file:
# 		# data = image_file.read()
# 		# encoded_string = data.encode("base64")
# 		encoded_string = base64.b64encode(image_file.read())
# 	return encoded_string

@app.route('/start')
def startWsp():
	try :
		options = Options()
		# options.headless = True
		global driver
		driver = webdriver.Firefox(options=options, executable_path="geckodriver.exe")
		# driver.implicitly_wait(5)
		print("Firefox Headless Browser Invoked")
		driver.get('https://web.whatsapp.com')
		# addDriverListener()
		return jsonify({'msg':'Connected','data':''}), 200
	except Exception as e:
		return jsonify({'msg':'Exception','data':str(e)}), 404

@app.route('/scan')
def scanQR():
	qr_base64 = ""
	try:
		driver
	except Exception as e:
		return jsonify({'msg':'Please connect to whatsapp first.','data' : ''}), 404
	
	try:
		#before scanning always check if realod qr is visible
		# reload_qr = WebDriverWait(driver, 1).until(
		# expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "._2zblx")))
		driver.find_element_by_css_selector("._2zblx").click()
		# if reload_qr :
		driver.refresh()
		return jsonify({'msg':'try again', 'data' : 'NULL'}), 200
		
	except Exception as e:
		try:
			#qr_code image
			print('waiting ')
			qr_image_tag = WebDriverWait(driver, 10).until(
			expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "._2EZ_m img")))
			# qr_image_tag = driver.find_element_by_css_selector("._2EZ_m img")
			qr_base64 = qr_image_tag.get_attribute("src")
			# driver.get_screenshot_as_file("qr_code.png")
			print('wait done')
			# print('found :' + qr_base64)
			# encoded_string = get_image()

			 # org = driver.find_element_by_id('org')

		except Exception as e: 
			print('scan qr error')
			print(e)
			return jsonify({'msg':'Exception found ','data' :e}), 404

		
		
	# return qr_base64
	return jsonify({'msg': '', 'data' : qr_base64}), 200
		


@app.route("/")
def apiRunning():
	return "<h1>Working...</h1>"
	
@app.route('/whatsappmated/<path:path>')
def serve_files(path):
	print("******"+path)
	return send_from_directory('./', path)
	
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")


firebaseSetup()