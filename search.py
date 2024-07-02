import os
import concurrent.futures

def demo():
  return [1,2,3]

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


directory_to_search = '/' if os.name != 'nt' else 'C:\\'
exclude_dirs = get_exclude_dirs()

def find_git_repos(directory, exclude_dirs):
  git_repos = []
  for root, dirnames, filenames in os.walk(directory):
    # Skip excluded directories
    dirnames[:] = [d for d in dirnames if os.path.join(root, d) not in exclude_dirs]
    
    if '.git' in dirnames:
      git_repos.append(root)
      dirnames.remove('.git')  # Do not traverse inside the .git directory
  
  return git_repos

def search_single_threaded():
  git_repos = find_git_repos(directory_to_search, exclude_dirs)
  
  if git_repos:
    print("Git repositories found:")
    for repo_path in git_repos:
      print(repo_path)
  else:
    print("No Git repositories found.")
    
  return git_repos

def is_excluded(path, exclude_dirs):
  for exclude_dir in exclude_dirs:
    if path.startswith(exclude_dir):
      return True
  return False


def find_git_repos_concurrent(directory, exclude_dirs, results):
  for root, dirnames, filenames in os.walk(directory):
    # Skip excluded directories
    dirnames[:] = [d for d in dirnames if os.path.join(root, d) not in exclude_dirs]
    
    if '.git' in dirnames:
      results.append(os.path.join(root, '.git'))

def search_multi_threaded():
  results = []
  
  # List to store initial directories to search
  initial_dirs = []
  for root, dirnames, _ in os.walk(directory_to_search):
    for dirname in dirnames:
      dirpath = os.path.join(root, dirname)
      if not is_excluded(dirpath, exclude_dirs):
        initial_dirs.append(dirpath)
    break  # Only need the top-level directories to start multithreading
  
  # Use ThreadPoolExecutor to search directories in parallel
  with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(find_git_repos_concurrent, dir, exclude_dirs, results) for dir in initial_dirs]
    for future in concurrent.futures.as_completed(futures):
      future.result()  # Wait for all threads to complete
  
  if results:
    print("Git repositories found:")
    for repo_path in results:
      print(repo_path)
  else:
    print("No Git repositories found.")
    
  return results