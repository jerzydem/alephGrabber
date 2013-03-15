import urllib3
import pdb  
from parse import *
httpManager = urllib3.PoolManager()
pdfListFile = 'pdf_files.txt'


def create_pdf_list(listFile):
  outfile = open(listFile, 'w')
	http = urllib3.PoolManager()
	adr = 'http://statlibr.stat.gov.pl/F/RCTMPHT6L17LTF6V1EQ58BTTDJMVUG6UF4N342RJY3F6HGNRUU-22024?func=short-jump&jump=000'

	bookNum = 1
	maxBook = 515

	while bookNum <= maxBook:
		r = http.request('GET', adr+ str(bookNum))
		print(r.status)

		res = findall('''<a href='javascript:open_window("{}");'><img src="/exlibris/aleph/u18_1/alephe/www_f_pol/icon/f-tn-{}.jpg" border=0 alt="{}">''',r.data)
		#pdb.set_trace()

		for line in res:
			if line[1] == 'pdf':
				outfile.write(line[0]+ ' ' + line[2].replace('.','_').replace(' ','_') + '\n')							

		print(res)
		bookNum+=10

	outfile.close()

def download_single_pdf(http, url, title):
	print(url)	

	r = http.request('GET', 'http://statlibr.stat.gov.pl' + url)
	r.status
	r.headers['server']
	adr = search('''<body onLoad=window.location="{}">''', r.data)
	pdfurl = 'http://statlibr.stat.gov.pl' + adr[0]

	r = http.request('GET', pdfurl)

	with open("pdf/"+title+".pdf", "wb") as file:
	    file.write(r.data)

def dwnFiles(listFile, httpMng):
	srcFile = open(listFile, 'r')
	for line in srcFile:
		res = line.split(' ')
#		print(res[0] + '\n' + res[1] + '\n\n')
		download_single_pdf(httpMng, res[0], res[1])	 
	srcFile.close()


#exurl = '''http://statlibr.stat.gov.pl/F/I6BVU7HD6IE7IEFP6PPVUPDCHDIG1A65RPE4IRFGQ4C6Y873II-46600?func=service&doc_library=CBS01&doc_number=000058306&line_number=0001&func_code=WEB-BRIEF&service_type=MEDIA'''
#create_pdf_list(pdfListFile)
#download_single_pdf( httpManager, exurl, "title1")
dwnFiles(pdfListFile, httpManager)




