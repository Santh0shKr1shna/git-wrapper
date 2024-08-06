import flask

import search
import information
import json

from flask import Flask
from flask import request

app = Flask(__name__)

# Testing
@app.route('/local-repos', methods=['GET'])
def GET_Local_Repos():
  result = search.Search_multi_threaded()
  print(result)
  return json.JSONEncoder().encode(result)


@app.route('/repo-info', methods=['GET'])
def GET_Repo_Info():
  git_path = request.args.get("path")
  if git_path == "":
    return app.response_class(
      response=None,
      status=400,
      mimetype='application/json'
    )
  
  data = information.Get_repo_info(git_path)
  print(data)
  
  response = app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json'
  )
  return response
  
@app.route('/home', methods=['GET'])
def GET_Home():
  data = information.Get_home_page()
  print(data)
  
  response = app.response_class(
    response = json.dumps(data),
    status = 200,
    mimetype='application/data'
  )
  
  return response

@app.route('/execute', methods=['POST'])
def Execute():
  response = None
  status = None
  if request.method == "POST":
    command = request.form['command']
    print(command)
    
    data = "success"
    
    response = data
    status = 200
    
  else:
    response = "Method not allowed"
    status = 405
    
  return app.response_class(
    response=response,
    status=status,
    mimetype='application/json'
  )

def main():
  app.run()
  
if __name__ == "__main__":
  main()