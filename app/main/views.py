from flask import render_template, send_from_directory, request, jsonify, redirect, url_for, make_response, send_file, current_app
from ..models import Record
from ..utils import path_to_dict
from .. import db
from . import main
import os, time, shutil, glob, subprocess, threading
from subprocess import call
from celery_app import task1
from datetime import datetime

@main.route("/", methods=["GET","POST"])
def index():
    recordList = Record.query.all()
    return render_template("index.html",recordList=recordList)

@main.route("/runnigRecords", methods=["GET"])
def runnigRecords():
    recordList = Record.query.filter_by(status="in_process").all()
    temp = []
    for x in recordList:
        temp.append(x.to_json())
    return jsonify(runningRecords = temp)

@main.route("/records", methods=["GET"])
def records():
    recordList = Record.query.all()
    temp = []
    for x in recordList:
        temp.append(x.to_json())
    return jsonify(data = temp)

@main.route("/async_execute", methods=["POST"])
def async_execute():
    name = request.form["caseName"]
    task = task1.executepuppeteer.delay(name)
    print("return task id %s"%task.id)
    record = Record(name=name, task_id=task.id,start_time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),status="in_process")
    db.session.add(record)    
    return jsonify({}), 202, {'Location':url_for("main.task_status",task_id=task.id)}

@main.route("/task_status",methods=["GET","POST"])
def task_status():
    task_id = request.args.get("task_id",0)
    task = task1.executepuppeteer.AsyncResult(task_id)
    print(task)
    if task.state == 'PENDING':
        response = {
            'state':task.state,
            'status':'Pending...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state':task.state,
            'end_time':datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        response.update(task.result)
    else:
        response = {
            'state':task.state,
            'status':str(task.info)
        }
    return jsonify(response)

@main.route("/update_task", methods=["GET","POST"])
def update_task():
    task_id = request.form["task_id"]
    end_time = request.form["end_time"]
    record = Record.query.filter_by(task_id=task_id).first()
    record.status = request.form["status"]
    record.end_time = end_time
    db.session.add(record)
    return jsonify(status="ok")

@main.route("/tree", methods=["GET","POST"])
def tree():
    return render_template("tree.html")

@main.route("/cases",methods=["GET"])
def cases():
    json_d = []
    json_d.append(path_to_dict('/Users/i072687/Desktop/cases'))
    return  jsonify(json_d)