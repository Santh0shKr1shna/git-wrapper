import flask

from search import Search_multi_threaded
from information import Get_repo_info
import json

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/local-repos', methods=['GET'])
def GET_Local_Repos():
  result = Search_multi_threaded()
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
  
  data = Get_repo_info(git_path)
  print(data)
  
  response = app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json'
  )
  return response
  

def main():
  app.run()
  
if __name__ == "__main__":
  main()