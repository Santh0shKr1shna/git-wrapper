from search import search_multi_threaded
import json

from flask import Flask
app = Flask(__name__)

@app.route('/local-repos', methods=['GET'])
def GET_Local_repos():
  result = search_multi_threaded()
  print(result)
  return json.JSONEncoder().encode(result)

def main():
  app.run()
  
if __name__ == "__main__":
  main()