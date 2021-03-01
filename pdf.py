pages_number=45
folder1=r'D:\pdf-splitter\\'
folder2=r'D:\pdf-splitter\split\\'
id=""
json_file_location="credentials.json"
from PyPDF2 import PdfFileReader as reader, PdfFileWriter as writer
import os.path
import os
import re
import sys
from time import sleep
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth ,ServiceAccountCredentials
proxy = 'http://localhost:8080'

#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy
flag=sys.argv[1]
gauth = GoogleAuth()
scope = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_location, scope)
drive = GoogleDrive(gauth)

list1=os.listdir(folder1)
if flag=="2":
	#print("Flag")
	pdf_list=[x for x in list1 if re.search(".\.PDF$",x,re.IGNORECASE)]
	for x in pdf_list:
		output_name=x
		split_output_name="Split_"+output_name
		print("Directory updated "+output_name)
		pdf=reader(folder1+output_name)
		outputWriter=writer()
		for x in range(pages_number):
			outputWriter.addPage(pdf.getPage(x))
			
		with open(folder2+split_output_name,"wb")as outputPDF:		
			outputWriter.write(outputPDF)
			outputPDF.close()

		file2 = drive.CreateFile({'title': split_output_name, 
			"parents":  [{"id": id}], 
			"mimeType": "application/pdf"})

		file2.SetContentFile(folder2+split_output_name)
		file2.Upload()
		print(split_output_name+" Successfully Uploaded")
	sys.exit()




while True:
	list2=os.listdir(folder1)
	unique=[x for x in list2 if x not in list1 and re.search(".\.PDF$",x,re.IGNORECASE)]
	list1=os.listdir(folder1)
	
	if len(unique):
		for x in unique:
			output_name=x
			split_output_name="Split_"+output_name
			print("Directory updated "+output_name)
			pdf=reader(folder1+output_name)
			outputWriter=writer()
			for x in range(pages_number):
				outputWriter.addPage(pdf.getPage(x))
				
			with open(folder2+split_output_name,"wb")as outputPDF:		
				outputWriter.write(outputPDF)
				outputPDF.close()

			file2 = drive.CreateFile({'title': split_output_name, 
				"parents":  [{"id": id}], 
				"mimeType": "application/pdf"})

			file2.SetContentFile(folder2+split_output_name)
			file2.Upload()
			print(split_output_name+" Successfully Uploaded")
	sleep(2)
