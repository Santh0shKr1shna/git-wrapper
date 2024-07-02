import os
import concurrent.futures
import fnmatch

from datetime import datetime
startTime = datetime.now()

def find_git_repos(directory, exclude_dirs, results):
  for root, dirnames, filenames in os.walk(directory):
    # Skip excluded directories
    dirnames[:] = [d for d in dirnames if os.path.join(root, d) not in exclude_dirs]
    
    if '.git' in dirnames:
      results.append(os.path.join(root, '.git'))


def is_excluded(path, exclude_dirs):
  for exclude_dir in exclude_dirs:
    if path.startswith(exclude_dir):
      return True
  return False

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

def main():
  # Directory to start the search
  directory_to_search = '/' if os.name != 'nt' else 'C:\\'  # Root directory for Unix-like systems or 'C:\\' for Windows.
  
  # Directories to exclude from the search
  exclude_dirs = get_exclude_dirs()
  
  # Exclude AppData directory for the current user on Windows
  if os.name == 'nt':
    appdata_path = os.path.expandvars(r'%APPDATA%').replace('Roaming', '')
    exclude_dirs.append(appdata_path)
  
  # Normalize excluded directories for the current operating system
  exclude_dirs = [os.path.normpath(d) for d in exclude_dirs]
  
  # List to store the results
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
    futures = [executor.submit(find_git_repos, dir, exclude_dirs, results) for dir in initial_dirs]
    for future in concurrent.futures.as_completed(futures):
      future.result()  # Wait for all threads to complete
  
  if results:
    print("Git repositories found:")
    for repo_path in results:
      print(repo_path)
  else:
    print("No Git repositories found.")


if __name__ == "__main__":
  main()
  print("TIME: ", datetime.now() - startTime)