from flask import render_template, send_from_directory, request, jsonify, redirect, url_for, make_response, send_file, current_app
from ..models import Record
from ..utils import path_to_dict,toJson
from .. import db, cases_folder
from . import main
import os, time, shutil, glob, subprocess, threading
from subprocess import call
from celery_app import task1
from datetime import datetime
from sqlalchemy import desc, asc

@main.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

@main.route("/execution", methods=["GET","POST"])
def execution():
    recordList = Record.query.all()
    print(cases_folder)
    return render_template("execution.html",recordList=recordList)

@main.route("/statistics", methods=["GET","POST"])
def statistics():
    return render_template("statistics.html")

@main.route("/details", methods=["GET","POST"])
def details():
    record_id = request.args.get("id",0)
    return render_template("detailsExecution.html", record_id = record_id)

@main.route("/detailsTree", methods=["GET","POST"])
def detailsTree():
    record_id = request.args.get("id")
    record = Record.query.get_or_404(record_id)
    info = {}
    info["status"] = record.status
    info["start_time"] = record.start_time
    info["end_time"] = record.end_time

    return jsonify(toJson(record.test_cases,info))

@main.route("/runnigRecords", methods=["GET"])
def runnigRecords():
    recordList = Record.query.filter_by(status="in_process").all()
    temp = []
    for x in recordList:
        temp.append(x.to_json())
    return jsonify(runningRecords = temp)

@main.route("/records", methods=["GET"])
def records():
    draw = int(request.args.get("draw"))
    start = int(request.args.get("start"))
    length =  int(request.args.get("length"))
    order_column_index = request.args.get("order[0][column]")
    order_seq = request.args.get("order[0][dir]")
    searchValue =request.args.get("search[value]") 
    sort_map = {0:Record.id, 3:Record.start_time,4:Record.end_time}   
    totalRecordList = Record.query.all() 
    #sort
    sort_item = sort_map.get(int(order_column_index))
    if searchValue:
        recordList = Record.query.filter(Record.id.like("%"+searchValue+"%") | Record.test_cases.like("%"+searchValue+"%") | Record.owner.like("%"+searchValue+"%") |
                                         Record.start_time.like("%"+searchValue+"%") | Record.status.like("%"+searchValue+"%") ).order_by(Record.id.desc()).all()
    else:
        recordList = Record.query.order_by(desc(sort_item)).all() if order_seq == "desc" else Record.query.order_by(asc(sort_item)).all()
    temp = []
    if len(recordList)-start >length:
        for i in range(length):
            temp.append(recordList[start+i].to_json())
    else:
        for i in range(len(recordList)-start):
            temp.append(recordList[start+i].to_json())       
    return jsonify(draw = draw, recordsTotal=len(totalRecordList),recordsFiltered=len(recordList),data = temp )

@main.route("/async_execute", methods=["POST"])
def async_execute():
    caseList = request.get_json()["caseList"]
    print(caseList)
    #caseList = request.form.getlist("caseList[]")
    task = task1.executepuppeteer.delay(caseList)
    record = Record(test_cases=','.join(str(case) for case in caseList),task_id=task.id,start_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),status="in_process")
    db.session.add(record)    
    executionRecord = Record.query.filter_by(task_id=task.id).all()
    temp = []
    for x in executionRecord:
        temp.append(x.to_json())
    return jsonify(executionRecord=temp), 202, {'Location':url_for("main.task_status",task_id=task.id), "task_id":task.id}

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
    elif task.state == 'PROGRESS':
         response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
        }
    elif task.state == 'SUCCESS':
        response = {
            'state':task.state,
            'end_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        response.update(task.result)
    else:
        response = {
            'state':task.state,
            'status':str(task.info),
            'end_time':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'log_path':"#"
        }
    return jsonify(response)

@main.route("/update_task", methods=["GET","POST"])
def update_task():
    task_id = request.form["task_id"]
    end_time = request.form["end_time"]
    log_path = request.form["log_path"]
    record = Record.query.filter_by(task_id=task_id).first()
    record.status = request.form["state"]
    if request.form.get("message"):
        record.message = request.form["message"]
    record.end_time = end_time
    record.log_path = log_path
    db.session.add(record)
    return jsonify(status="ok")

@main.route("/tree", methods=["GET","POST"])
def tree():
    return render_template("tree.html")

@main.route("/cases",methods=["GET"])
def cases():
    json_d = []
    json_d.append(path_to_dict(cases_folder))
    print(json_d)
    return  jsonify(json_d)

@main.route("/recordStatistics",methods=["GET"])
def recordStatistics():
    recordStatistics = {}
    recordStatistics["success_count"] = Record.query.filter_by(status="SUCCESS").count()
    recordStatistics["failure_count"] = Record.query.filter_by(status="FAILURE").count()
    return  jsonify(recordStatistics)