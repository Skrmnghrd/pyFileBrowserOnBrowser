from subprocess import check_output
from os import chdir, path, system
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
                    'files_in_cwd' : self.files_in_cwd,
					'clean_format_dir': self.cur_dir_for_downloads()
                    
                }
	def get_dirs_in_cwd(self):
		self.dirs_in_cwd = [x for x in check_output('ls -a', shell=True).decode().split('\n') if path.isdir(x) == True]

	def clear_dirs(self):
		self.dirs_in_cwd = [] #clear it
    
	def get_files_in_cwd(self):
		self.files_in_cwd = [x for x in check_output('ls -a', shell=True).decode().split('\n') if path.isdir(x) == False and x is not '']

	def show_current_dir(self):
		present_dir = re.sub('\n', '', check_output('pwd', shell=True).decode() )
		try:

			return present_dir + re.sub(present_dir, '', check_output('ls -ld $(pwd) --time-style=+""', shell=True).decode() ) 
		except:
			return present_dir
			
	   #use html tags on json
	#remove the bahog b'lut \n hahaha
	def cur_dir_for_downloads(self):
		return re.sub('\n', '', check_output('pwd', shell=True).decode() )
	def change_dir(self, dir_name):
		try:

			for i in range(10):
				print (dir_name)			
			chdir(str(dir_name))
		except PermissionError:
			self.current_dir = "Insufficent Privilege Please check terminal and type in sudo password or run this with sudo (not advisable)"
			
			self.files_in_cwd = ["Insufficent Privilege Please check terminal and type in sudo password or run this with sudo (not advisable)"]
			
			return

			"""		except FileNotFoundError:
			self.current_dir = "File not found. Must have been deleted or you r just drunk :)"
 
			self.files_in_cwd = ['File not found. Must have been deleted or you r just drunk :)']			
			return"""
		self.current_dir = self.show_current_dir()
		clear_dirs = self.clear_dirs()
		self.get_dirs_in_cwd()
		self.get_files_in_cwd()