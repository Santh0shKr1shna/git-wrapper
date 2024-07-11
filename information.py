import os
from time import strftime, localtime
import search

def read_git_file(git_path, *path_parts):
  """Read a file from the .git directory."""
  if '.git' not in git_path:
    git_path = git_path + "/.git"
  try:
    with open(os.path.join(git_path, *path_parts), 'r') as file:
      return file.read().strip()
  except FileNotFoundError:
    return None


def get_repo_status(git_path):
  """Get the status of the Git repository by reading the index and worktree."""
  original_cwd = os.getcwd()
  os.chdir(os.path.dirname(git_path))
  status = os.popen('git status --short').read()
  os.chdir(original_cwd)
  return status


def get_remote_connections(git_path):
  """Get the remote connections by reading the config file."""
  config = read_git_file(git_path, 'config')
  if not config:
    return "No remote configurations found."
  
  remotes = []
  lines = config.split('\n')
  remote_name, remote_url = "", ""
  for line in lines:
    if line.strip().startswith('[remote '):
      remote_name = line.strip().split('"')[1]
    if line.strip().startswith('url = '):
      remote_url = line.strip().split('= ')[1]
      remotes.append(f'{remote_name} {remote_url}')
  
  return "\n".join(remotes)


def get_head_info(git_path):
  """Get the current HEAD information by reading the HEAD file."""
  head = read_git_file(git_path, 'HEAD')
  if head and head.startswith('ref: '):
    return head[5:]
  return head


def get_last_commit(git_path):
  """Get the last commit information by reading the logs."""
  head_ref = get_head_info(git_path)
  if head_ref:
    commit_hash = read_git_file(git_path, head_ref)
    commit_info = read_git_file(git_path, 'logs', 'HEAD')
    if commit_info:
      last_commit_line = commit_info.split('\n')[-1]
      commit_details = last_commit_line.split()
      commit_hash = commit_details[1]
      author = " ".join(commit_details[2:4])
      local_time, timezone = commit_details[4:6]
      date = [strftime("%d-%m-%Y %H:%M:%S", localtime(int(local_time))), timezone]
      message = " ".join(commit_details[7:])
      return {
        "commit_hash": commit_hash,
        "author": author,
        "date": date,
        "message": message
      }
  return None


def get_branch_info(git_path):
  """Get branch information by reading the refs/heads directory."""
  branches = []
  for root, dirs, files in os.walk(os.path.join(git_path, 'refs', 'heads')):
    for file in files:
      branches.append(os.path.relpath(os.path.join(root, file), os.path.join(git_path, 'refs', 'heads')))
  return "\n".join(branches)


def Get_repo_info(git_path):
  response = {}
  if not os.path.isdir(git_path):
    print("Not inside a Git repository.")
    return response
  
  # response["status"] = get_repo_status(git_path)
  response["remotes"] = get_remote_connections(git_path)
  response["branches"] = get_branch_info(git_path)
  response["head"] = get_head_info(git_path)
  response["lastCommit"] = get_last_commit(git_path)
  
  return response

def Get_home_page():
  paths = search.Search_multi_threaded()
  if not paths:
    return []
  
  result = []
  for path in paths:
    result.append(Get_repo_info(path))
    
  return result

def main(git_path):
  if not os.path.isdir(git_path):
    print("Not inside a Git repository.")
    return
  
  print("Repository Status:\n", get_repo_status(git_path))
  print("\nRemote Connections:\n", get_remote_connections(git_path))
  print("\nCurrent HEAD:\n", get_head_info(git_path))
  commit_info = get_last_commit(git_path)
  if commit_info:
    print("\nLast Commit:",
          f'\nHash: {commit_info["commit_hash"]}'
          f'\nAuthor: {commit_info["author"]}'
          f'\nDate: {commit_info["date"][0]} {commit_info["date"][1]}'
          f'\nMessage: {commit_info["message"]}')
  else:
    print("\nLast Commit:\n No commits found.")
  print("\nBranches:\n", get_branch_info(git_path))

if __name__ == "__main__":
  print(Get_home_page())
#   main('C:\\Users\\Santhosh\\Desktop\\Projects\\StalkTalk\\.git')
