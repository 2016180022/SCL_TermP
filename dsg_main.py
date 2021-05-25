#210521
#DSG

from tkinter import *
import urllib.request
import urllib.parse

import json
import http.client
import os

server = 'api.neople.co.kr'
apikey = 'rDbaGyKaYdUlFoFDidXiyOoeMB0mrR5M'
conn = http.client.HTTPSConnection(server)

class DSG:

	def __init__(self):
		self.board = Tk()
		self.board.title('DSG')
		self.board.geometry('600x800')
		self.board.resizable(False, False)
		self.serverId = ''
		self.charName = ''
		self.initUpperFrame()

		self.board.mainloop()
		
	def initUpperFrame(self):						#UpperFrame includes char search list
		# upperFrame = Frame(self.board)
		# upperFrame.pack(side = 'top')
		global serverLB
		serverLBScroll = Scrollbar(self.board)
		serverLBScroll.pack()
		serverLBScroll.place(x = 80, y = 20)
		serverLB = Listbox(self.board, width = 8, height = 3, yscrollcommand = serverLBScroll.set)
		serverLB.insert(0, '전체')
		serverLB.insert(1, '카인')
		serverLB.insert(2, '디레지에')
		serverLB.insert(3, '시로코')
		serverLB.insert(4, '프레이')
		serverLB.insert(5, '카시야스')
		serverLB.insert(6, '힐더')
		serverLB.insert(7, '안톤')
		serverLB.insert(8, '바칼')
		serverLB.pack()
		serverLB.place(x = 20, y = 20)
		serverLBScroll.config(command = serverLB.yview)
		
		global charNameEntry
		charNameEntry = Entry(self.board, width = 50)
		charNameEntry.pack()
		charNameEntry.place(x = 120, y = 20)
		
		#self.charName = charNameEntry.get()
		charSearchButton = Button(self.board, text = '검색', command = self.searchChar)
		charSearchButton.pack()
		charSearchButton.place(x = 480, y = 18)

	def searchChar(self):
		self.charName = charNameEntry.get()
		charName = self.charName

		if (charName == ""):
			print('Error: 캐릭터 이름을 입력해주세요.')
			return

		if serverLB.curselection() == ():
			serverIndex = 0
		else:
			serverIndex = serverLB.curselection()[0]

		if serverIndex == 0:
			self.serverId = 'all'
		elif serverIndex == 1:
			self.serverId = 'cain'
		
		charName = urllib.parse.quote(str(charName).encode('UTF-8'))
		conn.request('GET', '/df/servers/' + self.serverId + '/characters?characterName=' + charName + '&wordType=full&apikey=' + apikey)

		response = conn.getresponse()
		cLen = response.getheader('Content-Length')
		result = response.read(int(cLen)).decode('UTF-8')

		jsonData = self.parsingCharData(result)

		# if len(jsonData.jsonData['rows']) == 0:
		# 	print('Error: 데이터 읽어오기 실패')
		# 	return

		#print(result)

	def parsingCharData(self, JSON):
		jsonData = json.loads(JSON)

		if len(jsonData['rows']) == 0:
			print('Error: Json 파일 불러오기 실패!')
			return

		self.charIdLst = []
		self.charNameLst = []
		self.serverIdLst = []
		self.charLstCounts = len(jsonData['rows'])

		index = 0

		for i in range(self.charLstCounts):
			self.charIdLst.append(jsonData['rows'][i]['characterId'])
			self.charNameLst.append(jsonData['rows'][i]['characterName'])
			self.serverIdLst.append(jsonData['rows'][i]['serverId'])
			#self.charLv = jsonData['rows'][index]['level']
			#self.jobName = jsonData['rows'][index]['jobName']
			#self.jobGrowName = jsonData['rows'][index]['jobGrowName']

		for index in range(len(self.charIdLst)):
			self.getCharImage(self.serverIdLst[index], self.charIdLst[index], self.charNameLst[index])

		self.printCharImage()

	def getCharImage(self, serverId, charId, charName, size = 12):
		url = 'https://img-api.neople.co.kr/df/servers/' + serverId + '/characters/' + charId + '?zoom=' + str(size)
		outpath = 'images/'
		outfile = 'image_' + serverId + '_' + charName + '.png'

		if not os.path.isdir(outpath):
			os.makedirs(outpath)

		urllib.request.urlretrieve(url, outpath + outfile)

	def printCharImage(self):
		imageLst = []
		for i in range(self.charLstCounts):
			imageLst.append(PhotoImage(file = 'images/image_' + self.serverIdLst[i] + '_' + self.charNameLst[i] + '.png'))

		buttonLst = []
		for i in range(self.charLstCounts):
			buttonLst.append(Button(self.board, image = imageLst[i], bg = 'white', command = self.selectChar))
			buttonLst[i].image = imageLst[i]
			buttonLst[i].pack()
		# 	#buttonLst[i].place(x = )

	def selectChar(self):
		pass


demo = DSG()

