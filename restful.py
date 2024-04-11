# using flask_restful 
from flask import Flask, jsonify, request , make_response
from flask_restful import Resource, Api 
from browserpilot.agents.gpt_selenium_agent import GPTSeleniumAgent
  
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
        instructions_buffalo = """Go to Google.com
Find all textareas.
Find the first visible textarea.
Click on the first visible textarea.
Type in "buffalo buffalo buffalo buffalo buffalo" and press enter.
Wait 2 seconds.
Find all anchor elements that link to Wikipedia.
Click on the first one.
Wait for 10 seconds.
"""

        #return jsonify({'data': data}), 200
        for key, value in data.items():
            if key == "instructions":
                instructions_buffalo = value;
            print(key, value)
        print(instructions_buffalo)
        agent = GPTSeleniumAgent(instructions_buffalo,"/home/prateek/workspace/browserpilot/chromedriver", 
                         {"--profile-directory":"Default"}, "/home/prateek/.config/google-chrome",
                         False, False,"gpt-3.5-turbo","gpt-3.5-turbo", None,
                         False,"",None, False)
        agent.run()
        return make_response(jsonify({'data': data}), 200)
  
  
# another resource to calculate the square of a number 
class Square(Resource): 
  
    def get(self, num): 
  
        return jsonify({'square': num**2}) 
  
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Square, '/square/<int:num>') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = False) 