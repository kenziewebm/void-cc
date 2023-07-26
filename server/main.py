#!/usr/bin/env python3
import json
from sys import argv
from os import getpid
from flask import Flask, request, Response

app = Flask(__name__)

# In-memory storage for user accounts
user_accounts = {}

# Function to save user info to accounts.txt
def save_to_file(username, password, token):
    with open("accounts.txt", "a") as file:
        file.write(f"{username} {password} {token}\n")

@app.route("/addAccount")
def add_account():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return unauthorized()

    username = request.args.get("user")
    password = request.args.get("pass")
    token    = request.args.get("token")
    if username and password and token:
        save_to_file(username, password, token)
        return f"User '{username}' added successfully!\n"
    else:
        return "Invalid request. Please provide 'user','pass', and 'token' parameters.\n"

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
        return unauthorized()
    try:
        with open("accounts.txt", "r") as file:
            content = file.read()
        return Response(content, mimetype="text/plain")
    except FileNotFoundError:
        return "No accounts found.\n", 404

@app.route("/getPid")
def get_pid():
	return str(getpid()) + '\n'

if __name__ == "__main__":
    get_config()
    app.run(host="0.0.0.0", port=PORT)

