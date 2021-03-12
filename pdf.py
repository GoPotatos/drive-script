pages_number=45
folder1=r'C:/Users/user/Documents/split/before/'
folder2=r'C:/Users/user/Documents/split/after/'
id=""
json_file_location="credentials.json"
import os.path
import os
import re
import sys
import subprocess
from time import sleep
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth ,ServiceAccountCredentials
proxy = 'http://localhost:8080'
'''os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy'''
flag=sys.argv[1]
gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_location, scope)
drive = GoogleDrive(gauth)

list1=os.listdir(folder1)

def uploadFiles(files_list):
	for x in files_list:
		output_name=x
		output_path=folder1+output_name
		split_output_name="Split_"+output_name
		split_path=folder2+split_output_name
		print("Directory updated "+split_path)
		pages_range="1-"+str(pages_number)
		try:
			subprocess.check_call(["cmd","/c","pdftk",output_path,"cat",pages_range,"output",split_path])
		except:
			pass

		file2 = drive.CreateFile({'title': split_output_name, 
			"parents":  [{"id": id}], 
			"mimeType": "application/pdf"})

		file2.SetContentFile(split_path)
		file2.Upload()
		print(split_output_name+" Successfully Uploaded")

if flag=="2":
	#print("Flag")
	pdf_list=[x for x in list1 if re.search(".\.PDF$",x,re.IGNORECASE)]
	uploadFiles(pdf_list)
	sys.exit()




while True:
	list2=os.listdir(folder1)
	unique=[x for x in list2 if x not in list1 and re.search(".\.PDF$",x,re.IGNORECASE)]
	list1=os.listdir(folder1)
	
	if len(unique):
		uploadFiles(unique)
	sleep(2)
