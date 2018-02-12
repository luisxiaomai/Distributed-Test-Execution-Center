# Distributed test execution center  ![projectStatus](https://img.shields.io/badge/status-In--Development-red.svg)

<div align=center ><img src="https://github.com/luisxiaomai/Images/blob/master/Distributed_Test_Center/testcenter.gif"/></div>

## Local Run

  [Python 3+](https://www.python.org/downloads/) need be installed

  [Redis](https://redis.io/) need be installed

  Install dependencies
  ```
  pip install -r requirements.txt
  ```
  Launch distributed task worker
  ```
  celery  -A celery_app worker --loglevel=info
  ```
  Test Task Execution Definition
  
  > For demo purpose, I defined **executepuppeteer** task in celery_app/task1.py. [Node,Npm](  https://nodejs.org/en/download/) need be installed
  ```	
    npm i --save puppeteer
  ```
  Launch server
  ```	
  python manage.py runserver
  ```
  Navigate to http://127.0.0.1:5000

## Done
- Execution history with search feature
- Case selection with search feature
- Parell execution
- Status check
- Log Path
- Task level failure handle
- Task timeout
- Server side processing with pagination, sort, filter

## Todo
- Case level failure handle
- Jenkins job execution integration
- Execution record details page
- Optimize deployment, dockerlize

