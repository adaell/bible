
import urllib.request
import sys

# Basic config
DEFAULT_TRANSLATION = 'ESV'
OUTPUT_WIDTH=80 # Width of console output. Set to 0 to disable wrapping
COLOURED_OUTPUT=True

# # #
BIBLEBOOKS=['Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth','1Samuel','2Samuel','1Kings','2Kings','1Chronicles','2Chronicles','Ezra','Nehemiah','Esther','Job','Psalms','Proverbs','Ecclesiastes','SongOfSolomon','Isaiah','Jeremiah','Lamentations','Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk','Zephaniah','Haggai','Zechariah','Malachi','Tobit','Judith','WisdomOfSolomon','Sirach','Baruch','LetterOfJeremiah','Susanna','BelAndTheDragon','1Maccabees','2Maccabees','1Esdras','3Maccabees','2Esdras','4Maccabees','Psalms','Matthew','Mark','Luke','John','Acts','Romans','1Corinthians','2Corinthians','Galatians','Ephesians','Philippians','Colossians','1Thessalonians','2Thessalonians','1Timothy','2Timothy','Titus','Philemon','Hebrews','James','1Peter','2Peter','1John','2John','3John','Jude','Revelation']
BIBLEBOOKS_ABV=['Gen','Exod','Lev','Num','Deut','Josh','Judg','Rth','1Sam','2Sam','1Kgs','2Kgs','1Chron','2Chron','Ezr','Neh','Esth','Jb','Ps','Prov','Ecc','Song','Isa','Jer','Lam','Ezek','Dan','Hos','Joe','Am','Obad','Jnh','Micah','Nah','Hab','Zeph','Hag','Zech','Mal','Tobit','Jdth','Wisd','Sir','Bar','Letter','Sus','Bel','1Macc','2Macc','1Esdr','3Macc','2Esdr','4Macc','Ps','Matt','Mrk','Luk','John','Act','Rom','1Cor','2Cor','Gal','Ephes','Phil','Col','1Thess','2Thess','1Tim','2Tim','Titus','Philem','Heb','James','1Pet','2Pet','1Jhn','2Jhn','3Jhn','Jude','Rev']
TRANSLATION_LIST=['KJ21','ASV','AMP','AMPC','BRG','CSB','CEB','CJB','CEV','DARBY','DLNT','DRA','ERV','EASY','EHV','ESV','ESVUK','EXB','GNV','GW','GNT','HCSB','ICB','ISV','PHILLIPS','JUB','KJV','AKJV','LSB','LEB','TLB','MSG','MEV','MOUNCE','NOG','NABRE','NASB','NASB1995','NCB','NCV','NET Bible','NIRV','NIV','NIVUK','NKJV','NLV','NLT','NMB','NRSVA','NRSVACE','NRSVCE','NRSVUE','NTFE','OJB','RGT','RSV','RSVCE','TLV','VOICE','WEB','WE','WYC','YLT']
NUMBERED_BOOKS=['Samuel','Kings','Chronicles','Corinthians','Thessalonians','Timothy','Peter','John']
NUMBERED_BOOKS_ABV=['Sam','Kgs','Chron','Cor','Thess','Tim','Pet','Jhn']

if COLOURED_OUTPUT is True:
	GREY='\033[1;30m'
	NORMAL='\033[0m'
else:
	GREY=''
	NORMAL=''

# a class for storing bible verse information
class bibleverse:
	def __init__(self):
		self.translation = DEFAULT_TRANSLATION
		self.book = None
		self.chapter = None
		self.verse = [None,None]

# parses the console arguments and returns a bibleverse
def parseInput():
	import sys

	lBIBLEBOOKS = [x.lower() for x in BIBLEBOOKS]
	lBIBLEBOOKS_ABV = [x.lower() for x in BIBLEBOOKS_ABV]
	lNUMBERED_BOOKS = [x.lower() for x in NUMBERED_BOOKS]
	lNUMBERED_BOOKS_ABV = [x.lower() for x in NUMBERED_BOOKS_ABV]
	lTRANSLATION_LIST = [x.lower() for x in TRANSLATION_LIST]

	# modifies the verse heading for numbered books
	args = sys.argv
	for i in range(1,len(args)-1):
		line0 = args[i]
		line1 = args[i+1]
		if line0.isdigit() is True and line1.isdigit() is False:
			if line1.lower() in lNUMBERED_BOOKS:
				args[i+1] = line0+line1
				del args[i]
				break

	# Parses the input
	verse = bibleverse()
	for i in range(1,len(args)):
		arg = args[i]
		if arg.lower() in lBIBLEBOOKS:
			idx = lBIBLEBOOKS.index(arg.lower())
			verse.book = BIBLEBOOKS[idx]
			continue
		if arg.lower() in lBIBLEBOOKS_ABV:
			idx = lBIBLEBOOKS_ABV.index(arg)
			verse.book = BIBLEBOOKS[idx]
			continue
		if arg.lower() in lTRANSLATION_LIST:
			verse.translation = arg
			continue
		# User has specified chapter and verse e.g. Joshua 5:6-7 or Joshua  5:6
		if ':' in arg:
			chap_verse_info = arg.split(":")
			verse.chapter = int(chap_verse_info[0])
			if '-' in chap_verse_info[1]:
				vnums = chap_verse_info[1].split('-')
				verse.verse = [int(vnums[0]),int(vnums[1])]
				if(verse.verse[0] > verse.verse[1]):
					print("The first verse is larger than the second")
					sys.exit(1)
			else:
				verse.verse = int(chap_verse_info[1])
			continue
		# User has specifed the verse numbers separately to the chapter number e.g. Exodus 5 7-8
		if '-' in arg:
			chap_verse_info = arg.split("-")
			verse.verse = [int(chap_verse_info[0]),int(chap_verse_info[1])]
			if(verse.verse[0] > verse.verse[1]):
				print("The first verse is larger than the second")
				sys.exit(1)
		# User has specified a chapter number and/or verse number on its own e.g. Gen 5 6
		if arg.isdigit() is True and verse.chapter is None:
			verse.chapter = int(arg)
			continue
		if arg.isdigit() is True and verse.chapter is not None:
			verse.verse = int(arg)
			continue
		continue

	sanity_check(verse)
	return verse

def sanity_check(bibleverse):
	if bibleverse.chapter == None:
		print("\nI do not understand what chapter you want.\n")
		sys.exit(1)
	if bibleverse.book == None:
		print("\nI do not understand which book you want.\n")
		sys.exit(1)

# Takes a bibleverse and returns a url to the verse on biblegateway
def generateUrl(bibleverse):
	if(bibleverse.verse == [None,None]):
		chap = str(bibleverse.chapter)
	elif(isinstance(bibleverse.verse,int)):
		chap = str(bibleverse.chapter) + "%3A" + str(bibleverse.verse)
	else:
		chap = str(bibleverse.chapter) + "%3A" + str(bibleverse.verse[0]) + '-' + str(bibleverse.verse[1])
	string = "https://www.biblegateway.com/passage/?search=" + bibleverse.book + "+" + chap + "&version=" + bibleverse.translation
	return string

# Fetches a url and returns a string with the html text
def fetchUrl(url_string):
	import urllib.request
	with urllib.request.urlopen(url_string) as response:
   		html = response.read()
   		html = html.decode()
   		html = html.splitlines()
   		return html
	return html

# A biblegateway html parser
from html.parser import HTMLParser
class bibleParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		self.start_tag = tag
		self.attrs=[]
		for attr in attrs:
			self.attrs.append(attrs)
	def handle_endtag(self, tag):
		self.end_tag = tag
	def handle_data(self, data):
		self.data.append(data)
	def reset_data(self):
		self.data = []
	def handle_comment(self, data):
		self.comment = data
	def handle_entityref(self, name):
		c = chr(name2codepoint[name])
		self.named_ent = c
	def handle_charref(self, name):
		if name.startswith('x'):
			c = chr(int(name[1:], 16))
		else:
			c = chr(int(name))
		self.num_ent = c
	def handle_decl(self, data):
		self.decl = data

# Prints the bible chapter and verse to the console
def print_title(bibleverse):
	if bibleverse.book[0].isdigit() is True:
		titlestring = bibleverse.book[0] + ' ' + bibleverse.book[1:]
	else:
		titlestring = bibleverse.book

	if bibleverse.verse == [None,None]:
		string = '\n' + titlestring + " " + str(bibleverse.chapter)
	elif isinstance(bibleverse.verse,int) is False:
		string = '\n' + titlestring + " " + str(bibleverse.chapter) + ":" + str(bibleverse.verse[0]) + "-" + str(bibleverse.verse[1])
	else:
		string = '\n' + titlestring + " " + str(bibleverse.chapter) + ":" + str(bibleverse.verse)
	print(string)

# adds carriage returns to string every OUTPUT_WIDTH characters
# then prints string to console
def print_to_console(string):
	if OUTPUT_WIDTH != 0:
		counter = 0
		# newstring = '\n'
		newstring = ''
		escape = False
		for c in string:
			if c == '\x1b':
				escape = True
			if escape is False:
				counter+=1
			if escape is True and c == 'm':
				escape = False

			newstring+=c
			if c == "\n": # if we just started a new line, reset the counter
				counter=0
			if counter >= OUTPUT_WIDTH: 
				if c == " ":
					newstring+='\n'
					counter = 0
		print(newstring)
	else:
		print(string)

# cleans up a string with footnotes information and prints them to console
def parse_footnotes(footnotes):
	if len(footnotes) == 0:
		print()
		sys.exit(0)

	import re
	consoleout = '\n' + GREY
	# loop over footnotes
	for i in range(0,len(footnotes)):
		fn = footnotes[i]
		skip = True
		# Footnote numbering/lettering
		if i < 26:
			consoleout += '[' + chr(ord('a')+i) + ']'
		else:
			rem = i % 26
			div = int(i / 26)
			consoleout += '[' + chr(ord('a')+div-1) + chr(ord('a')+rem) + ']'

		# TODO
		# # Italics
		# for j in range(0,len(fn)):
		# 	if 'Literally' == fn[j][0:9]:
		# 		fn[j]=re.sub('Literally','\x1B[3mLiterally\x1B[0m',fn[j])
		# 		continue
		# 	if 'Hebrew' == fn[j][0:6]:
		# 		fn[j]=re.sub('Hebrew','\x1B[3mHebrew\x1B[0m',fn[j])	
		# 		continue
		# 	fn[j]=re.sub('Lit','\x1B[3mLit\x1B[0m',fn[j])
		# 	fn[j]=re.sub('Heb','\x1B[3mHeb\x1B[0m',fn[j])
		# 	fn[j]=re.sub('I.e.','\x1B[3mI.e.\x1B[0m',fn[j])
		# 	fn[j]=re.sub('Or','\x1B[3mOr\x1B[0m',fn[j])

		# Add to consoleout
		for j in range(0,len(fn)):
			if fn[j] == 'Footnotes':
				continue
			if skip: # skips the first line
				skip = False
				continue
			consoleout += fn[j]
		consoleout += '\n' 
	consoleout += NORMAL
	print_to_console(consoleout)

# makes some cosmetic changes to the output string 
def fixFormating(string):
	import re
	newstring = '\n'
	skip = 0
	
	for i in range(1,len(string)-1):
		if skip > 0: # skip some lines
			skip -= 1
			continue
		sentence = string[i]

		# Put newline before and after chapter headings
		sentenceN1 = string[i-1]
		sentenceP1 = string[i+1]
		if sentenceN1 == ' ' and sentence != ' ' and '\xa0' in sentenceP1:
			if i > 1:
				newstring += '\n\n'
			sentence = sentence + '\n\n'

		#skip these letters
		if sentence == '(':
			skip = 2
			continue

		if sentence == '[':
			newstring += GREY + ' ['
			continue
		if sentence == ']':
			newstring += ']' + NORMAL
			continue
		if sentence[0].isdigit() is True:
			number = ''
			for c in sentence:
				if c.isdigit() is False:
					break
				number += c
			newstring += GREY + number + ' ' + NORMAL
			continue

		if '\xa0' in sentence and sentence[0].isdigit() is False:
			sentence = ' '

		if sentence == 'Read full chapter':
			break
		newstring += sentence

	return newstring

# parses the html verse string and prints the verse to console
def parseAndPrintHtml(string):
	parser = bibleParser()
	startPrinting = False
	for i in range(0,len(string)):
		line = string[i]
		parser.reset_data()
		parser.feed(line)
		temp = parser.get_starttag_text()
		if(temp == '<div class="passage-text">'):
			startPrinting = True
			continue
		if startPrinting is True:
			data = parser.data
			if len(data) == 0:
				continue
			else:
				data=fixFormating(data)
				print_to_console(data)
				break
	if startPrinting is False:
		print("\nI could not locate this verse.\n")
		sys.exit(1)

# parses the html footnote string and prints the footnotes to console
def parseAndPrintFootnotes(string):
	parser = bibleParser()
	startPrinting = False
	footnotes=[]
	for i in range(0,len(string)):
		line = string[i]
		parser.reset_data()
		parser.feed(line)
		temp = parser.get_starttag_text()
		if(temp == '<div class="footnotes">'):
			startPrinting = True
			continue
		if startPrinting is True:
			data = parser.data
			if 'end of footnote' in line:
				break
			if len(data) == 0:
				continue
			else:
				footnotes.append(data)
				continue
	parse_footnotes(footnotes)

def main():
	verse = parseInput()
	url = generateUrl(verse)
	html = fetchUrl(url)
	print_title(verse)
	parseAndPrintHtml(html)
	parseAndPrintFootnotes(html)

# Run the main program
main()

