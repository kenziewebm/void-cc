#!/usr/bin/env python3
import os
import json
from sys import argv
from waitress import serve
from werkzeug.utils import secure_filename
from flask import Flask, request, Response

app = Flask(__name__)

# In-memory storage for user accounts
user_accounts = {}

# Function to save user info to accounts.txt
def save_to_file(username, password, cookies):
	with open("accounts.txt", "a") as file:
		file.write(f"{username} {password} {cookies}\n")


@app.route("/addAccount")
def add_account():
	auth = request.authorization
	if not auth or not check_auth(auth.username, auth.password):
		print("User attempted to be added")
		return unauthorized()

	username = request.args.get("user")
	password = request.args.get("pass")
	cookies    = request.args.get("cookies")
	if username and password and cookies:
		save_to_file(username, password, cookies)
		print("User added succesfully")
		print(f"{username}, {password}, {cookies}")
		return f"User '{username}' added successfully!\n", 200
	else:
		return "Invalid request. Please provide 'user','pass', and 'cookies' parameters.\n", 400

def get_config():
	with open("../config.json", "r") as config_file:
		config_data = json.load(config_file)
	authlogin = config_data.get('server', {}).get('login')
	authpass  = config_data.get('server', {}).get('pass')
	global PORT
	PORT      = config_data.get('server', {}).get('port')
	return authlogin, authpass

# Function to authenticate access to accounts.txt using HTTP Basic Auth
def check_auth(username, password):
	authlogin, authpass = get_config()
	return username == authlogin and password == authpass

# Function to handle unauthorized access
def unauthorized():
	return Response("Unauthorized Access\n", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

@app.route("/getAccounts")
def accounts():
	auth = request.authorization
	if not auth or not check_auth(auth.username, auth.password):
		print("Accounts were attempted to be accessed")
		return unauthorized()
	try:
		with open("accounts.txt", "r") as file:
			content = file.read()
			print("Accounts were accessed")
		return Response(content, mimetype="text/plain"), 200
	except FileNotFoundError:
		return "No accounts found.\n", 404

@app.route("/getPid")
def get_pid():
	return str(os.getpid()) + '\n', 200

@app.route("/torrc")
def get_torrc():
	try:
		with open("res/torrc", "r") as file:
			content = file.read()
		return Response(content, mimetype="text/plain"), 200
	except FileNotFoundError:
		return "No torrc found.\n", 404

@app.route("/microsocks")
def get_msocks():
        platform = request.args.get('p')
        if p == 'linux':
                try:
                        with open("res/msock.elf", "rb") as file:
                                content = file.read()
                                print("Microsocks downloaded")
                        return Response(content, mimetype="application/octet-stream"), 200
                except FileNotFoundError:
                        return "No microsocks build found.\n", 404
        elif p == 'win':
                try:
                        with open("res/msock.exe", "rb") as file:
                                content = file.read()
                                print("Microsocks downloaded")
                        return Response(content, mimetype="application/octet-stream"), 200
                except FileNotFoundError:
                        return "No microsocks build found.\n", 404
        else:
                return f"No build found for {p}\n", 404

@app.route("/uploadRes")
def upload_res():                                                         # TODO: This is probably insecure, needs review
	auth = request.authorization
	if not auth or not check_auth(auth.username, auth.password):
		print("Files were attempted to be uploaded")
		return unauthorized()

	if "file" not in request.files:
		return "No file specified.\n", 400
	file = request.files["file"]
	if file.filename == "":
		return "No file specified.\n", 400
	filename = secure_filename(file.filename)
	file.save(os.path.join("res", filename))
	print(f"file {filename} was uploaded")
	return "File uploaded", 200

@app.route("/downloadRes")
def download_res():
	auth = request.authorization
	if not auth or not check_auth(auth.username, auth.password):
		return unauthorized()
	with open(os.path.join("res", request.args.get('file')), 'rb') as f:
		content = f.read()
		print(f"file {request.args.get('file')} was accessed")
		return Response(content, mimetype="text/plain"), 200      # TODO: fix mimetype
	
	
if __name__ == "__main__":
	get_config()
	serve(app, host="0.0.0.0", port=PORT)

