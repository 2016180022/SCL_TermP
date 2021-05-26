#210521
#DSG

from tkinter import *
import tkinter.font as tkfont
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
		self.charFont = tkfont.Font(family = 'D2coding', size = 12)
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

		global initialLabel
		initialLabel = Label(self.board, text = '캐릭터를 입력해주세요', font = tkfont.Font(family = 'D2coding', size = 20))
		initialLabel.pack()
		initialLabel.place(x = 160, y = 200)

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
		elif serverIndex == 2:
			self.serverId = 'diregie'
		elif serverIndex == 3:
			self.serverId = 'siroco'
		elif serverIndex == 4:
			self.serverId = 'prey'
		elif serverIndex == 5:
			self.serverId = 'casillas'
		elif serverIndex == 6:
			self.serverId = 'hilder'
		elif serverIndex == 7:
			self.serverId = 'anton'
		elif serverIndex == 8:
			self.serverId = 'bakal'
		
		charName = urllib.parse.quote(str(charName).encode('UTF-8'))
		conn.request('GET', '/df/servers/' + self.serverId + '/characters?characterName=' + charName + '&wordType=full&apikey=' + apikey)
		header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

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
		initialLabel.destroy()
		self.imageLst = []
		imageText = []
		serverText = []
		for i in range(self.charLstCounts):
			image = PhotoImage(file = 'images/image_' + self.serverIdLst[i] + '_' + self.charNameLst[i] + '.png')
			self.imageLst.append(image)
			imageText.append(self.charNameLst[i])

			if self.serverIdLst[i] == 'cain':
				serverText.append('카인')
			elif self.serverIdLst[i] == 'bakal':
				serverText.append('바칼')
			elif self.serverIdLst[i] == 'anton':
				serverText.append('안톤')
			elif self.serverIdLst[i] == 'casillas':
				serverText.append('카시야스')
			elif self.serverIdLst[i] == 'diregie':
				serverText.append('디레지에')
			elif self.serverIdLst[i] == 'hilder':
				serverText.append('힐더')
			elif self.serverIdLst[i] == 'prey':
				serverText.append('프레이')
			elif self.serverIdLst[i] == 'siroco':
				serverText.append('시로코')

		global buttonLst, textLst, serverLst
		buttonLst = []
		textLst = []
		serverLst = []
		for i in range(self.charLstCounts):
			x = i % 5
			y = i // 5
			buttonLst.append(Button(self.board, width = 100, height = 150, image = self.imageLst[i], bg = 'white', command = lambda index = i : self.selectChar(index)))
			buttonLst[i].image = self.imageLst[i]
			buttonLst[i].pack()
			buttonLst[i].place(x = 25 + (x * 110) , y = 100 + (y * 200))
			textLst.append(Label(self.board, text = imageText[i], bg = 'white', font = self.charFont))
			textLst[i].pack()
			textLst[i].place(x = 26 + (x * 110), y = 101 + (y * 200))
			serverLst.append(Label(self.board, text = serverText[i], bg = 'white'))
			serverLst[i].pack()
			serverLst[i].place(x = 26 + (x * 110), y = 121 + (y * 200))

	def selectChar(self, index):
		self.charId = self.charIdLst[index]
		self.charName = self.charNameLst[index]
		self.serverId = self.serverIdLst[index]
		self.charImage = self.imageLst[index]

		if self.serverIdLst[index] == 'cain':
			self.serverName = '카인'
		elif self.serverIdLst[index] == 'bakal':
			self.serverName = '바칼'
		elif self.serverIdLst[index] == 'anton':
			self.serverName = '안톤'
		elif self.serverIdLst[index] == 'casillas':
			self.serverName = '카시야스'
		elif self.serverIdLst[index] == 'diregie':
			self.serverName = '디레지에'
		elif self.serverIdLst[index] == 'hilder':
			self.serverName = '힐더'
		elif self.serverIdLst[index] == 'prey':
			self.serverName = '프레이'
		elif self.serverIdLst[index] == 'siroco':
			self.serverName = '시로코'

		self.charIdLst.clear()
		self.charNameLst.clear()
		self.serverIdLst.clear()

		for i in range(self.charLstCounts):
			buttonLst[i].destroy()
			textLst[i].destroy()
			serverLst[i].destroy()

		self.printCharInfo()

	def printCharInfo(self):
		charImageLabel = Label(self.board, image = self.charImage)
		charImageLabel.pack()
		charImageLabel.place(x = 25, y = 100)
		charNameLabel = Label(self.board, font = self.charFont, text = self.charName)
		charNameLabel.pack()
		charNameLabel.place(x = 50, y = 320)
		charServerLabel = Label(self.board, text = self.serverName)
		charServerLabel.pack()
		charServerLabel.place(x = 50, y = 340)

		infoNameLabelLst = []
		infoNameLst = ['모자', '머리', '얼굴', '상의', '하의', '신발', '목가슴', '허리', '피부', '무기']
		infoItemLabelLst = []
		infoCheckLst = []

		self.getCharInfo()

		for i in range(10):
			x = 200
			y = 80 + i * 30
			infoNameLabelLst.append(Label(self.board, text = infoNameLst[i], font = self.charFont))
			infoNameLabelLst[i].pack()
			infoNameLabelLst[i].place(x = x, y = y)
			infoItemLabelLst.append(Label(self.board, text = self.infoNameLst[i]))
			infoItemLabelLst[i].pack()
			infoItemLabelLst[i].place(x = x + 60, y = y + 2)
			infoCheckLst.append(Checkbutton(self.board, command = lambda index = i : self.infoCheck(index)))
			infoCheckLst[i].pack()
			infoCheckLst[i].place(x = x + 300, y = y + 1)

	def getCharInfo(self):
		conn.request('GET', '/df/servers/' + self.serverId + '/characters/' + self.charId + '/equip/avatar?apikey=' + apikey)
		response = conn.getresponse()
		cLen = response.getheader('Content-Length')
		result = response.read(int(cLen)).decode('UTF-8')

		Info = json.loads(result)

		print(Info)

		self.infoIdLst = []
		self.infoNameLst = []

		for index in range(8):
			self.infoIdLst.append(Info['avatar'][index]['clone']['itemId'])
			self.infoNameLst.append(Info['avatar'][index]['clone']['itemName'])
			#print(self.infoIdLst[index], self.infoNameLst[index])
		self.infoIdLst.append(Info['avatar'][8]['itemId'])
		self.infoNameLst.append(Info['avatar'][8]['itemName'])
		if 'clone' in Info['avatar'][10]:
			self.infoIdLst.append(Info['avatar'][10]['clone']['itemId'])
			self.infoNameLst.append(Info['avatar'][10]['clone']['itemName'])
		else:
			self.infoIdLst.append(Info['avatar'][10]['itemId'])
			self.infoNameLst.append(Info['avatar'][10]['itemName'])

		self.getWeaponInfo()

	def getWeaponInfo(self):
		conn.request('GET', '/df/servers/' + self.serverId + '/characters/' + self.charId + '/equip/equipment?apikey=' + apikey)
		response = conn.getresponse()
		cLen = response.getheader('Content-Length')
		result = response.read(int(cLen)).decode('UTF-8')

		Info = json.loads(result)

		if 'skin' in Info['equipment'][0]:
			self.infoIdLst[9] = Info['equipment'][0]['skin']['itemId']
			self.infoNameLst[9] = Info['equipment'][0]['skin']['itemName']
		else:
			if self.infoIdLst[9] == None:
				self.infoIdLst[9] = Info['equipment'][0]['itemId']
				self.infoNameLst[9] = Info['equipment'][0]['itemName']

	def infoCheck(self, index):
		pass


demo = DSG()

