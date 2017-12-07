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


import shutil



from flask import Flask, request, redirect, url_for, render_template
import os
import json
import glob
from uuid import uuid4

import logging
import traceback

"""log = logging.getLogger('werkzeug') #uncomment for silent flask
log.setLevel(logging.ERROR)
"""
jsglue = JSGlue()
app = Flask(__name__)
jsglue.init_app(app)
filebrowser = File_Browser.FileBrowser()

good_ip_addresses = ['127.0.0.1', '192.168.1.10', '192.168.2.100', '10.0.0.103','10.0.0.202']

index = '/' #+ str(uuid.uuid4())
port= 8000#randint(1,65535)

for i in range(5):
    print ('PUT THIS ON AFTER THE IP OF YOUR BROWSER ' + ':'+ str(port) +index)
 

def valid_ip_check_required(*args, **kwargs):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            
            if request.remote_addr in  good_ip_addresses:
                return function(*args, **kwargs)
            else:
                pass
                return function(*args, **kwargs)
                #return redirect("http://www.google.com")
            
        return wrapper
    return real_decorator


class FORM_index(Form):

	pass


"""@app.errorhandler(404)
def err404(error):
    return redirect("http://www.google.com")
"""
@app.errorhandler(500)
def err500(error):
    return redirect("http://www.google.com")

@app.route(index)
@valid_ip_check_required()
def index():
	return render_template('index.html')

@app.route('/_first_open')
def _first_open():
	return jsonify(dir_info=filebrowser.get_info())

@app.route('/_change_dir')
def _change_dir():
    
	directory = request.args.get('directory')
	filebrowser.change_dir(str(directory))
	return jsonify(dir_info=filebrowser.get_info())


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
    separated_paths = file_name
    list_of_paths = separated_paths.split('++++++++||+||+|+|+||+++')
    name_file = list_of_paths.pop() #the last

    file_path = '/' + ('/').join([x for x in list_of_paths])

        
    return send_from_directory(file_path, name_file,  as_attachment=True)


@app.route('/check_file', defaults={'file_name': None})
@app.route('/check_file/<string:file_name>')
def check_file(file_name):
    separated_paths = file_name
    list_of_paths = separated_paths.split('++++++++||+||+|+|+||+++')
    name_file = list_of_paths.pop() #the last

    file_path = '/' + ('/').join([x for x in list_of_paths])
    return send_from_directory(file_path, name_file)#,  as_attachment=True)

@app.route('/_create_dir')
def _create_dir():
    dir_name = request.args.get('new_dir_name')
    permission = request.args.get('permission_of_dir')
    dir_to_be_created = os.path.join(filebrowser.cur_dir_for_downloads(), dir_name)
    try:
            
        if int(permission) > 7777:
            return jsonify(message="Please set the appopriate permissions (ex: 755)")
    except ValueError:
        permission = 7666 #sorry for that evil number 

    try:
        os.mkdir(dir_to_be_created, int(permission))
        return jsonify(message="Dir Created!")
    except FileExistsError:

        return jsonify(message='Directory Already Exists!')

    

@app.route('/_refresh')
def _refresh():
    return jsonify(dir_info=filebrowser.get_info())

@app.route('/_delete_dir')
def _delete_dir():
    deleted_dir = filebrowser.cur_dir_for_downloads()
    shutil.rmtree(filebrowser.cur_dir_for_downloads(), ignore_errors=True)
    return jsonify(message=deleted_dir + "Was sent to the void.")

@app.route('/_delete_files')
def _delete_files():
    
    list_from_javascript = request.args
    list_from_javascript = list_from_javascript.getlist('list_of_files[]')
    for i in (list_from_javascript):
        print (i)
    return jsonify(message=request.args)
#//please put prompt when you login to prompt for the uuid pre generated for production use :)
#for personal use. its okay to ignore those uuid




say_thanks = "https://github.com/kirsle/flask-multi-upload"
#got this kewl ready made script for uplaods. thanks sir


@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    
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
        pass
        #return redirect(url_for("upload_complete", uuid=upload_key))
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
#end of the script from github :) why reinvent the wheel? loljk






app.run(host="0.0.0.0", port=port, threaded=True, debug=True)#, ssl_context='adhoc')
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
