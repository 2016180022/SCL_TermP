#DSG

from tkinter import *
import tkinter.font as tkfont
import urllib.request
import urllib.parse

import json
import http.client
import os

import dsg_teller
import grap

import threading
import sys
from tkinter import messagebox
import folium
from cefpython3 import cefpython as cef

server = 'api.neople.co.kr'
apikey = 'rDbaGyKaYdUlFoFDidXiyOoeMB0mrR5M'
conn = http.client.HTTPSConnection(server)
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

class DSG:

	def __init__(self):
		self.board = Tk()
		self.board.title('DSG')
		self.board.geometry('600x800')
		self.board.resizable(False, False)
		self.charFont = tkfont.Font(family = 'D2coding', size = 12)
		self.serverId = ''
		self.charName = ''
		self.charLstCounts = 0
		self.labelCheck = 0
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

	def delSearchUI(self, charCounts):

		for i in range(charCounts):
			buttonLst[i].destroy()
			textLst[i].destroy()
			serverLst[i].destroy()

	def searchChar(self):
		if self.charLstCounts > 0:
			self.delSearchUI(self.charLstCounts)

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
		conn.request('GET', '/df/servers/' + self.serverId + '/characters?characterName=' + charName + '&wordType=full&apikey=' + apikey, None, header)
		
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

		self.delSearchUI(self.charLstCounts)

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

		self.printCharInfo()

	def printCharInfo(self):
		global charImageLabel, charServerLabel, charNameLabel
		charImageLabel = Label(self.board, image = self.charImage)
		charImageLabel.pack()
		charImageLabel.place(x = 25, y = 100)
		charNameLabel = Label(self.board, font = self.charFont, text = self.charName)
		charNameLabel.pack()
		charNameLabel.place(x = 50, y = 320)
		charServerLabel = Label(self.board, text = self.serverName)
		charServerLabel.pack()
		charServerLabel.place(x = 50, y = 340)

		global infoNameLabelLst, infoNameLst, infoItemButtonLst, infoCheckLst
		infoNameLabelLst = []
		infoNameLst = ['모자', '머리', '얼굴', '상의', '하의', '신발', '목가슴', '허리', '피부', '무기']
		infoItemButtonLst = []
		self.infoCheckLst = []

		self.getCharInfo()

		self.isCheckLst = []
		for i in range(10):
			self.isCheckLst.append(IntVar())
			x = 200
			y = 80 + i * 30
			infoNameLabelLst.append(Label(self.board, text = infoNameLst[i], font = self.charFont))
			infoNameLabelLst[i].pack()
			infoNameLabelLst[i].place(x = x, y = y)
			infoItemButtonLst.append(Button(self.board, text = self.infoNameLst[i], command = lambda index = i : self.infoCheck(index)))
			infoItemButtonLst[i].pack()
			infoItemButtonLst[i].place(x = x + 60, y = y + 2)
			self.infoCheckLst.append(Checkbutton(self.board, variable = self.isCheckLst[i]))
			self.infoCheckLst[i].pack()
			self.infoCheckLst[i].place(x = x + 300, y = y + 1)

		self.cfNameLabel = Label(self.board, text = '', font = self.charFont)
		self.dictItem = {}
		self.bucketNameLabel = Label(self.board, text = '총 아바타 구매 가격', font = self.charFont)
		self.bucketNameLabel.place(x = 50, y = 500)
		self.bucketListLabel = Label(self.board, text = '', font = self.charFont)
		self.bucketListLabel.place(x = 50, y = 520)
		self.bucketAddbutton = Button(self.board, text = '장바구니 추가', command = self.checkBucketList)
		self.bucketAddbutton.place(x = 50, y = 550)

		self.graphTitleLabel = Label(self.board, text = '경매장 시세', font = self.charFont)
		self.graphTitleLabel.place(x = 400, y = 560)

		self.gmailButton = Button(self.board, text = 'Gmail보내기', command = self.sendGMail)
		self.gmailButton.place(x = 50, y = 600)

		self.telegramButton = Button(self.board, text = 'Telegram 실행', command = self.turnTelegram)
		self.telegramButton.place(x = 50, y = 650)

		self.mapButton = Button(self. board, text = '지도 열기', command = self.openMap)
		self.mapButton.place(x = 50, y = 700)

		self.showroomButton = Button(self.board, text = '던파쇼룸 바로가기', command = self.goShowroom)
		self.showroomButton.place(x = 50, y = 750)

	def delCharInfo(self):
		for i in range(len(infoNameLst)):
			infoNameLabelLst[i].destroy()
			infoItemButtonLst[i].destroy()
			self.infoCheckLst[i].destroy()

	def getCharInfo(self):
		conn.request('GET', '/df/servers/' + self.serverId + '/characters/' + self.charId + '/equip/avatar?apikey=' + apikey)
		response = conn.getresponse()
		cLen = response.getheader('Content-Length')
		result = response.read(int(cLen)).decode('UTF-8')

		Info = json.loads(result)

		self.infoIdLst = []
		self.infoNameLst = []

		for index in range(8):
			self.infoIdLst.append(Info['avatar'][index]['clone']['itemId'])
			self.infoNameLst.append(Info['avatar'][index]['clone']['itemName'])
			#print(self.infoIdLst[index], self.infoNameLst[index])
		self.infoIdLst.append(Info['avatar'][8]['itemId'])
		self.infoNameLst.append(Info['avatar'][8]['itemName'])
		if len(Info['avatar']) > 10:
			if 'clone' in Info['avatar'][10]:
				self.infoIdLst.append(Info['avatar'][10]['clone']['itemId'])
				self.infoNameLst.append(Info['avatar'][10]['clone']['itemName'])
			else:
				self.infoIdLst.append(Info['avatar'][10]['itemId'])
				self.infoNameLst.append(Info['avatar'][10]['itemName'])
		else:
			self.infoIdLst.append('None')
			self.infoNameLst.append('None')

		self.getWeaponInfo()

	def getWeaponInfo(self):
		conn.request('GET', '/df/servers/' + self.serverId + '/characters/' + self.charId + '/equip/equipment?apikey=' + apikey)
		response = conn.getresponse()
		cLen = response.getheader('Content-Length')
		result = response.read(int(cLen)).decode('UTF-8')

		Info = json.loads(result)

		if 'skin' in Info['equipment'][0]:
			self.infoIdLst[-1] = Info['equipment'][0]['skin']['itemId']
			self.infoNameLst[-1] = Info['equipment'][0]['skin']['itemName']
		else:
			if self.infoIdLst[-1] == None:
				self.infoIdLst[-1] = Info['equipment'][0]['itemId']
				self.infoNameLst[-1] = Info['equipment'][0]['itemName']

	def infoCheck(self, index):
		itemId = self.infoIdLst[index]
		conn.request('GET', '/df/auction?itemId=' + itemId + '&sort=unitPrice:asc,reinforce:<reinforce>,auctionNo:<auctionNo>&limit=3&apikey=' + apikey)
		response = conn.getresponse()
		cLen = response.getheader('Content-Length')
		result = response.read(int(cLen)).decode('UTF-8')

		Info = json.loads(result)
		self.unitPrice = []
		for i in range(len(Info['rows'])):
			self.unitPrice.append(Info['rows'][i]['currentPrice'])

		if self.unitPrice == []:
			self.dictItem[self.infoNameLst[index]] = 0
		else:
			self.dictItem[self.infoNameLst[index]] = self.unitPrice[0]
		self.bucketListPrice = 0

		self.getItemImage(itemId)
		self.getMarketPrice(itemId)

		self.itemImage = PhotoImage(file = 'images/image_item_' + itemId + '.png')

		if self.labelCheck == 0:
			self.cfImageLabelLst = []
			self.cfPriceLabelLst = []
			self.warningLabel = Label(self.board, text = '', font = self.charFont)
			for i in range(3):
				self.cfImageLabelLst.append(Label(self.board))
				self.cfPriceLabelLst.append(Label(self.board, text = ''))
			self.labelCheck += 1

		if self.unitPrice != []:
			self.printItemInfo(index)
			self.drawGraph()
		else:
			self.printItemInfo(-1)

	def getItemImage(self, itemId):
		'https://img-api.neople.co.kr/df/items/<itemId>'
		url = 'https://img-api.neople.co.kr/df/items/' + itemId
		outpath = 'images/'
		outfile = 'image_item_' + itemId + '.png'

		if not os.path.isdir(outpath):
			os.makedirs(outpath)

		urllib.request.urlretrieve(url, outpath + outfile)

	def printItemInfo(self, index):
		if index == -1:
			self.warningLabel.configure(text = '아이템을 찾을 수 없습니다')
			self.warningLabel.place(x = 50, y = 400)
			if self.cfNameLabel['text'] != '':
				self.delItemInfo()
		else:
			self.delItemInfo(-1)
			if self.cfNameLabel['text'] == '':
				self.cfNameLabel.configure(text = self.infoNameLst[index])
				self.cfNameLabel.place(x = 50, y = 400)
				self.cfLabel = Label(self.board, text = '경매장 최저가')
				self.cfLabel.place(x = 50, y = 420)
				self.cfPriceLabel = Label(self.board, text = str(self.unitPrice[0]) + '골드', font = self.charFont)
				self.cfPriceLabel.place(x = 50, y = 445)
				self.cfAuctionTitleLabel = Label(self.board, text = '매물 현황', font = self.charFont)
				self.cfAuctionTitleLabel.place(x = 410, y = 400)
				for i in range(len(self.unitPrice)):
					self.cfImageLabelLst[i].configure(image = self.itemImage)
					self.cfImageLabelLst[i].place(x = 380, y = 440 + i * 40)
					self.cfPriceLabelLst[i].configure(text = str(self.unitPrice[i]) + '골드')
					self.cfPriceLabelLst[i].place(x = 430, y = 445 + i * 40)
			else:
				self.cfNameLabel.configure(text = self.infoNameLst[index])
				self.cfLabel.configure(text = '경매장 최저가')
				self.cfPriceLabel.configure(text = str(self.unitPrice[0]) + '골드')
				for i in range(len(self.unitPrice)):
					self.cfImageLabelLst[i].configure(image = self.itemImage)
					self.cfPriceLabelLst[i].configure(text = str(self.unitPrice[i]) + '골드')

	def delItemInfo(self, ftype = 0):
		if ftype == 0:
			self.cfNameLabel.configure(text = '')
			self.cfLabel.configure(text = '')
			self.cfPriceLabel.configure(text = '')
			self.cfAuctionTitleLabel.configure(text = '')
			for i in range(3):
				self.cfImageLabelLst[i].configure(image = '')
				self.cfPriceLabelLst[i].configure(text = '')
		elif ftype == -1:
			self.warningLabel.configure(text = '')

	def checkBucketList(self):
		for i in range(len(self.infoNameLst)):
			if self.isCheckLst[i].get() == 1:
				self.bucketListPrice += self.dictItem[self.infoNameLst[i]]
		self.bucketListLabel.configure(text = self.bucketListPrice)

	def drawGraph(self):
		self.graphCanvas = Canvas(self.board, width= 200, height= 150, bg = 'white')
		self.graphCanvas.place(x = 350, y = 590)
		self.graphCanvas.delete('graph')
		self.graphCanvas.create_line(12, 140, 192, 140, width= 2, tags = 'graph')
		self.graphCanvas.create_line(12, 10, 12, 140, width= 2, tags = 'graph')

		p = []
		pp = []
		y = []
		for i in range(len(self.marketPrice)):
			p.append(grap.tdivision(self.marketPrice[i]))
		for i in range(len(p)):
			pp.append(p[i] - min(p))
		
		if (max(pp) < 150):
			for i in range(len(pp)):
				y.append(pp[i])
		else:
			rate = grap.hdivision(max(pp))
			for i in range(len(pp)):
				y.append(pp[i] // rate)

		if (len(y)) > 2:
			self.graphCanvas.create_line(12 + 45, 130 - y[0], 12 + 45 + 45, 130 - y[1], width = 2, tags = 'graph', fill = 'red')
		if (len(y)) > 3:
			self.graphCanvas.create_line(12 + 45 + 45, 130 - y[1], 12 + 45 + 45 + 45, 130 - y[2], width = 2, tags = 'graph', fill = 'red')
			self.graphCanvas.create_line(12 + 45 + 45 + 45, 130 - y[2], 12 + 45 + 45 + 45 + 45, 130 - y[3], width = 2, tags = 'graph', fill = 'red')
		self.graphCanvas.create_text(12 + 30, 130 - min(y), text = min(self.marketPrice), tags = 'graph')
		self.graphCanvas.create_text(12 + 30, 130 - max(y), text = max(self.marketPrice), tags = 'graph')
		
	def getMarketPrice(self, itemId):
		conn.request('GET', '/df/auction-sold?itemId=' + itemId + '&limit=4&apikey=' + apikey)
		response = conn.getresponse()
		cLen = response.getheader('Content-Length')
		result = response.read(int(cLen)).decode('UTF-8')

		Info = json.loads(result)

		self.marketPrice = []
		
		for i in range(len(Info['rows'])):
			self.marketPrice.append(Info['rows'][i]['unitPrice'])
		
	def sendGMail(self):
		import mimetypes
		import mysmtplib
		from email.mime.base import MIMEBase
		from email.mime.text import MIMEText

		#global value
		host = "smtp.gmail.com" # Gmail STMP 서버 주소.
		port = "587"

		senderAddr = "dsg.depart@gmail.com"     # 보내는 사람 email 주소.
		recipientAddr = "vjsl159@gmail.com"   # 받는 사람 email 주소.

		msg = MIMEBase("multipart", "alternative")
		msg['Subject'] = "DSG 영수증 알림"
		msg['From'] = senderAddr
		msg['To'] = recipientAddr

		#장바구니 불러오기
		namelst = list(self.dictItem.keys())
		pricelst = list(self.dictItem.values())
		text = ''
		for i in range(len(self.infoNameLst)):
			if self.isCheckLst[i].get() == 1:
				text += namelst[i] + ': ' + str(pricelst[i]) + '골드\n'

		# MIME 문서를 생성합니다.
		HtmlPart = MIMEText(text, 'plain', _charset = 'UTF-8' )

		# 만들었던 mime을 MIMEBase에 첨부 시킨다.
		msg.attach(HtmlPart)

		# 메일을 발송한다.
		s = mysmtplib.MySMTP(host,port)
		#s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login("dsg.depart@gmail.com","dsg.depart.program")
		s.sendmail(senderAddr , [recipientAddr], msg.as_string())
		s.close()

	def turnTelegram(self):
		dsg_teller.run()

	def showMap(self, frame):
		sys.excepthook = cef.ExceptHook
		window_info = cef.WindowInfo(frame.winfo_id())
		window_info.SetAsChild(frame.winfo_id(), [0,0,800,600])
		cef.Initialize()
		browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
		cef.MessageLoop()

	def openMap(self):
		window = Tk()
		frame = Frame(window, width=800, height=600)
		frame.pack()
		
		# 지도 저장
		m = folium.Map(location=[33.4727133,126.4854080], zoom_start=16)
		m.save('map.html')

		# 브라우저를 위한 쓰레드 생성
		thread = threading.Thread(target=self.showMap, args=(frame,))
		thread.daemon = True
		thread.start()

		window.mainloop()

	def goShowroom(self):
		pass
	
demo = DSG()

