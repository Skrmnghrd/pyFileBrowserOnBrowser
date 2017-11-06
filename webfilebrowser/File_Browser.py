from subprocess import check_output
from os import chdir, path
import re
class FileBrowser:

	def __init__(self):
		self.current_dir = self.show_current_dir()
		self.get_dirs_in_cwd()
		self.get_files_in_cwd()
	
	def get_info(self):
		return {
                    'current_dir' : self.current_dir,
                    'dirs_in_cwd' : self.dirs_in_cwd,
                    'files_in_cwd' : self.files_in_cwd
                    
                }
	def get_dirs_in_cwd(self):
		self.dirs_in_cwd = [x for x in check_output('ls -a', shell=True).decode().split('\n') if path.isdir(x) == True]

	def clear_dirs(self):
		self.dirs_in_cwd = [] #clear it
    
	def get_files_in_cwd(self):
		self.files_in_cwd = [x for x in check_output('ls -a', shell=True).decode().split('\n') if path.isdir(x) == False and x is not '']

	def show_current_dir(self):
		return re.sub('\n', '', check_output('pwd', shell=True).decode() )#remove the bahog b'lut \n hahaha

	def change_dir(self, dir_name):
		try:
			chdir(str(dir_name))
		except PermissionError:
			pass

		#except Exception as e:
		#	return 'FileNotFoundError'
		self.current_dir = self.show_current_dir()
		clear_dirs = self.clear_dirs()
		self.get_dirs_in_cwd()
		self.get_files_in_cwd()