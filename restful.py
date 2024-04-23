# using flask_restful 
from flask import Flask, jsonify, request , make_response
from flask_restful import Resource, Api 
import json
import subprocess
import socket
import os
from pathlib import Path
import requests
from time import sleep
#from background_thread import BackgroundThreadFactory, TASKS_QUEUE
  
# creating the flask app 
app = Flask(__name__) 
# creating an API object 
api = Api(app) 
  
# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class Hello(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
  
        return jsonify({'message': 'hello world'}) 
  
    # Corresponds to POST request 
    def post(self): 
          
        data = request.get_json()     # status code 
        instructions_buffalo = ""
        website = "https://google.com"
        portActive = True
        port = 9222

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            portActive = s.connect_ex(('localhost', port)) == 0

        print('Port 9222 status : ', portActive)
        if portActive == False:
            print('Launching chrome in remote debugging mode')
            os.system("nohup google-chrome --headless --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0 --user-data-dir=\"/home/prateek/.config/google-chrome\"&")
            sleep(2)


        #return jsonify({'data': data}), 200
        for key, value in data.items():
            if key == "instructions":
                instructions_buffalo = value
            if key == "website":
                website = value
            print(key, value)
        print(instructions_buffalo)
        if website == "":
            website = "https://google.com"
        
        with open('../SeeAct/data/online_tasks/input_task.json', 'w') as f:
            json.dump([{'confirmed_task': instructions_buffalo, 'website': website, 'task_id': 'demo'}], f)

        os.system('rm -r ../SeeAct/online_results/demo')
        subprocess.Popen(["python", "../SeeAct/src/seeact.py"])
        return make_response(jsonify({'data': data}), 200)
    
  
  
# another resource to calculate the square of a number 
class Square(Resource): 
  
    def get(self, num):
        my_dir = Path("../SeeAct/online_results/demo")
        status = Path("../SeeAct/online_results/demo/currentStatus.txt")
        result = Path("../SeeAct/online_results/demo/result.json") 
        if my_dir.is_dir():
            current_status = "Not available"
            result_data = "Pending"
            if status.is_file():
                y = open('../SeeAct/online_results/demo/currentStatus.txt', "r")
                current_status = y.read()
                print(current_status)
            if result.is_file():
                result_data = "Complete"
        #return make_response(jsonify(data), 200)
            return make_response(jsonify({'Result': result_data, 'currentStaus': current_status}), 200)
        return make_response(jsonify({'currentStaus': "Internal_Error"}), 500)
  
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Square, '/getStatus/<string:num>') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = False) 