import os
from datetime import datetime
startTime = datetime.now()

def find_git_repos(directory, exclude_dirs):
  git_repos = []
  for root, dirnames, filenames in os.walk(directory):
    # Skip excluded directories
    dirnames[:] = [d for d in dirnames if os.path.join(root, d) not in exclude_dirs]
    
    if '.git' in dirnames:
      git_repos.append(root)
      dirnames.remove('.git')  # Do not traverse inside the .git directory
  
  return git_repos


def get_exclude_dirs():
  if os.name == 'nt':  # Windows
    exclude_dirs = [
      os.path.expandvars(r'%SYSTEMROOT%'),
      os.path.expandvars(r'%PROGRAMFILES%'),
      os.path.expandvars(r'%PROGRAMFILES(X86)%'),
      os.path.expandvars(r'%APPDATA%'),
      os.path.join(os.path.expandvars(r'%APPDATA%'), 'Local'),
      os.path.expandvars(r'%APPDATA%').replace("Roaming", ""),
      os.path.join(os.path.expandvars(r'%APPDATA%').replace("Roaming", ""), 'Local'),
      os.path.expandvars(r'%LOCALAPPDATA%'),
      'C:\\ProgramData',
      'C:\\Users\\Default',
      'C:\\Users\\Public'
    ]
  else:  # Unix-like systems
    exclude_dirs = [
      '/proc', '/sys', '/dev', '/run', '/var/lib', '/var/run', '/tmp',
      '/boot', '/mnt', '/media', '/lost+found', '/etc', '/bin', '/sbin',
      '/lib', '/lib64', '/usr', '/var/log'
    ]
  return [os.path.normpath(d) for d in exclude_dirs]


# Example usage:
if __name__ == "__main__":
  directory_to_search = '/'  # Root directory for Unix-like systems. Use 'C:\\' for Windows.
  
  exclude_dirs = get_exclude_dirs()
  
  # print(exclude_dirs)
  # exit()
  
  git_repos = find_git_repos(directory_to_search, exclude_dirs)
  
  if git_repos:
    print("Git repositories found:")
    for repo_path in git_repos:
      print(repo_path)
  else:
    print("No Git repositories found.")
  
  print("\n TIME: ", datetime.now() - startTime)