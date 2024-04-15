# using flask_restful 
from flask import Flask, jsonify, request , make_response
from flask_restful import Resource, Api 
import json
import subprocess
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

        #return jsonify({'data': data}), 200
        for key, value in data.items():
            if key == "instructions":
                instructions_buffalo = value
            if key == "website":
                website = value
            print(key, value)
        print(instructions_buffalo)
        
        with open('../SeeAct/data/online_tasks/input_task.json', 'w') as f:
            json.dump([{'confirmed_task': instructions_buffalo, 'website': website, 'task_id': 'demo'}], f)

        subprocess.Popen(["python", "/home/prateek/workspace/SeeAct/src/seeact.py"])
        #agent = GPTSeleniumAgent(instructions_buffalo,"/home/prateek/workspace/browserpilot/chromedriver", 
         #                {"--profile-directory":"Default"}, "/home/prateek/.config/google-chrome",
          #               False, False,"gpt-3.5-turbo","gpt-3.5-turbo", None,
           #              False,"",None, False)
        #agent.run()
        return make_response(jsonify({'data': data}), 200)
  
  
# another resource to calculate the square of a number 
class Square(Resource): 
  
    def get(self, num): 
        y = open('../SeeAct/online_results/demo/currentStatus.txt', "r")
        data = y.readlines()
        print(data)
        #return make_response(jsonify(data), 200)
        return make_response(jsonify({'currentStaus': data}), 200)
  
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Square, '/getStatus/<string:num>') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = False) 