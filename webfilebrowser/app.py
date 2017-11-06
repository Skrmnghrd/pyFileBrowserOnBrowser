#!/usr/bin/python
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory, Blueprint, jsonify, send_from_directory
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, BooleanField
from functools import wraps
from os import path, urandom, mkdir, listdir, remove, system, chdir
from subprocess import check_output
from flask.ext.login import LoginManager, LoginManager, UserMixin, login_user, login_manager, login_required, logout_user, current_user, fresh_login_required
from urllib.parse import urlparse, urljoin
from flask_wtf.file import FileField
from flask_jsglue import JSGlue


import File_Browser

jsglue = JSGlue()
app = Flask(__name__)
jsglue.init_app(app)
filebrowser = File_Browser.FileBrowser()




class FORM_index(Form):

	pass


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/_first_open')
def _first_open():
	return jsonify(dir_info=filebrowser.get_info())

@app.route('/_change_dir')
def _change_dir():
	print ('STACK PASSED HERE')
    
	directory = request.args.get('directory')
	filebrowser.change_dir(str(directory))
	return jsonify(dir_info=filebrowser.get_info())

@app.route('/_back_')
def _back_():#ur generic cd ..
	filebrowser.change_dir('..')
	return jsonify(dir_info=filebrowser.get_info())

@app.route('/get_file', defaults={'file_name': None})
@app.route('/_get_file/<string:file_name>')
def _get_file(file_name):
    #file_name = request.args.get('file_name')
    for i in range(10):
        print(file_name)
    return send_from_directory(filebrowser.current_dir, file_name,  as_attachment=True)

app.debug = True

app.run(host="0.0.0.0", port=8000, debug=True, threaded=True)