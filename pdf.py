pages_number=45
folder1=r'D:\pdf-splitter\\'
folder2=r'D:\pdf-splitter\split\\'
id=""
json_file_location="credentials.json"
from PyPDF2 import PdfFileReader as reader, PdfFileWriter as writer
import os.path
import os
import re
from time import sleep
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth ,ServiceAccountCredentials
from apiclient.discovery import build
proxy = 'http://localhost:8080'

gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_location, scope)
drive = GoogleDrive(gauth)

list1=os.listdir(folder1)
while True:
	list2=os.listdir(folder1)
	unique=[x for x in list2 if x not in list1]
	list1=os.listdir(folder1)
	
	if len(unique) and re.search(".\.PDF$",unique[0],re.IGNORECASE):
		output_name=unique[0]
		print("Directory updated "+output_name)
		pdf=reader(folder1+output_name)
		outputWriter=writer()
		for x in range(pages_number):
			outputWriter.addPage(pdf.getPage(x))
			
		with open(folder2+output_name,"wb")as outputPDF:		
			outputWriter.write(outputPDF)
			outputPDF.close()

		file2 = drive.CreateFile({'title': output_name, 
			"parents":  [{"id": id}], 
			"mimeType": "application/pdf"})

		file2.SetContentFile(folder2+output_name)
		file2.Upload()
		print(" Successfully Uploaded "+output_name+)
	sleep(2)
