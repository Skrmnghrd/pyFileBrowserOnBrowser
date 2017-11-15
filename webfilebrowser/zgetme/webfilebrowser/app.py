#!/usr/bin/python
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, send_from_directory, Blueprint, jsonify, send_from_directory
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, BooleanField
from functools import wraps
from os import path, urandom, mkdir, listdir, remove, system, chdir
from subprocess import check_output
#from flask.ext.login import LoginManager, LoginManager, UserMixin, login_user, login_manager, login_required, logout_user, current_user, fresh_login_required
from urllib.parse import urlparse, urljoin
from flask_wtf.file import FileField
from flask_jsglue import JSGlue
import uuid
from multiprocessing import Process
from time import sleep
from random import randint
import sys


import File_Browser







from flask import Flask, request, redirect, url_for, render_template
import os
import json
import glob
from uuid import uuid4


jsglue = JSGlue()
app = Flask(__name__)
jsglue.init_app(app)
filebrowser = File_Browser.FileBrowser()
index = '/' #str(uuid.uuid4())
print (index)

good_ip_addresses = ['127.0.0.1']

def valid_ip_check_required(*args, **kwargs):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if request.remote_addr in good_ip_addresses:
                pass
            else:
                sys.exit()
            
        return wrapper
    return real_decorator


class FORM_index(Form):

	pass


@app.route(index)
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

"""
Please finish the gum dat upload file :) 

"""

@app.route('/_back_')
def _back_():#ur generic cd ..
	filebrowser.change_dir('..')
	return jsonify(dir_info=filebrowser.get_info())


@app.route('/_upload')
def _upload():
	upload_file = request.files.getlist('upload_input')
	return jsonify(message="Upload okay!")


@app.route('/get_file', defaults={'file_name': None})
@app.route('/_get_file/<string:file_name>')
def _get_file(file_name):
    return send_from_directory(filebrowser.cur_dir_for_downloads(), file_name)#,  as_attachment=True)


"""
Below is the code for upload section
"""






say_thanks = "https://github.com/kirsle/flask-multi-upload"
#got this kewl ready made script for uplaods. thanks sir


@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":

        is_ajax = True

    # Target folder for these uploads.
    target = filebrowser.cur_dir_for_downloads() 
    try:
        pass
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        for i in range(10):
            print (is_ajax)
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return redirect(url_for("upload_complete", uuid=upload_key))
	 #put something here to refresh the list of files in current dir


@app.route("/files/<uuid>")
def upload_complete(uuid):
    """The location we send them to at the end of the upload."""

    # Get their files.
    root = "uploadr/static/uploads/{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template("files.html",
        uuid=uuid,
        files=files,
    )


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))







app.run(host="0.0.0.0", port=8000, threaded=True, debug=True)#, ssl_context='adhoc')
#def main():
"""	
	try:
		app.run(host="0.0.0.0", port=randint(1,65535), threaded=True, use_reloader=False)
	except:
		app.run(host="0.0.0.0", port=randint(1,65535), threaded=True, use_reloader=False)


a = {}
a.update({'test': Process(target=main)} )
a['test'].daemon=True
a['test'].start()
print(a['test'].is_alive())
sleep(10)
a['test'].terminate()
a['test'].join()
print(a['test'].is_alive())
"""
 
"""///*
assing a cookie to nth minits. 
create a function with cookie refresh lifetime when doing activity
w/0 activity. cookie counts down
if cookie xpyrd. kill the proess
and clear the dict
proces = {
	'uuid' : <process class here>
}

process['uuid_here'].daemon = True
if process['uuid_here'].is_alive() == False:
	del process['uuid']
	sleep (30) #and repeat

	secret url with password and a different port. 
	plus a random uuid for index.
"""
