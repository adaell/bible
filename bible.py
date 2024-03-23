
import urllib.request
import sys

# Width of console output
DEFAULT_TRANSLATION = 'LEB'
OUTPUT_WIDTH=80 

BIBLEBOOKS=['Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua','Judges','Ruth','1 Samuel','2 Samuel','1 Kings','2 Kings','1 Chronicles','2 Chronicles','Ezra','Nehemiah','Esther','Job','Psalms','Proverbs','Ecclesiastes','Song of Solomon','Isaiah','Jeremiah','Lamentations','Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah','Jonah','Micah','Nahum','Habakkuk','Zephaniah','Haggai','Zechariah','Malachi','Tobit','Judith','Wisdom Of Solomon','Sirach','Baruch','Letter of Jeremish','Susanna','Bel and the Dragon','1 Maccabees','2 Maccabees','1 Esdras','3 Maccabees','2 Esdras','4 Maccabees','Psalms','Matthew','Mark','Luke','John','Acts','Romans','1 Corinthians','2 Corinthians','Galatians','Ephesians','Philippians','Colossians','1 Thessalonians','2 Thessalonians','1 Timothy','2 Timothy','Titus','Philemon','Hebrews','James','1 Peter','2 Peter','1 John','2 John','3 John','Jude','Revelation']
BIBLEBOOKS_ABV=['Gen','Exod','Lev','Num','Deut','Josh','Judg','Rth','1 Sam','2 Sam','1 Kgs','2 Kgs','1 Chron','2 Chron','Ezr','Neh','Esth','Jb','Ps','Prov','Ecc','Song','Isa','Jer','Lam','Ezek','Dan','Hos','Joe','Am','Obad','Jnh','Micah','Nah','Hab','Zeph','Hag','Zech','Mal','Tobit','Jdth','Wisd','Sir','Bar','Letter','Sus','Bel','1 Macc','2 Macc','1 Esdr','3 Macc','2 Esdr','4 Macc','Ps','Laod','Matt','Mrk','Luk','John','Act','Rom','1 Cor','2 Cor','Gal','Ephes','Phil','Col','1 Thess','2 Thess','1 Tim','2 Tim','Titus','Philem','Heb','James','1 Pet','2 Pet','1 John','2 John','3 John','Jude','Rev']
TRANSLATION_LIST=['KJ21','ASV','AMP','AMPC','BRG','CSB','CEB','CJB','CEV','DARBY','DLNT','DRA','ERV','EASY','EHV','ESV','ESVUK','EXB','GNV','GW','GNT','HCSB','ICB','ISV','PHILLIPS','JUB','KJV','AKJV','LSB','LEB','TLB','MSG','MEV','MOUNCE','NOG','NABRE','NASB','NASB1995','NCB','NCV','NET Bible','NIRV','NIV','NIVUK','NKJV','NLV','NLT','NMB','NRSVA','NRSVACE','NRSVCE','NRSVUE','NTFE','OJB','RGT','RSV','RSVCE','TLV','VOICE','WEB','WE','WYC','YLT']

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

	# # wrong number of arguments
	# if len(sys.argv) > 3:
	# 	print("Invalid number of arguments. Was expecting two (Chapter Verse). Try `bible Genesis 2:3-4`")
	# 	exit(1)

	verse = bibleverse()
	for i in range(1,len(sys.argv)):
		arg = sys.argv[i]
		if arg in BIBLEBOOKS:
			verse.book = arg
			continue
		if arg in BIBLEBOOKS_ABV:
			verse_index = BIBLEBOOKS_ABV.index(arg)
			verse.book = BIBLEBOOKS[verse_index]
			continue
		if arg in TRANSLATION_LIST:
			verse.translation = arg
			continue
		# User has specified chapter and verse e.g. 5:6-7 or 5:6
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
		# User has specified a chapter number on its own
		if arg.isdigit() is True:
			verse.chapter = int(arg)
			continue

	sanity_check(verse)
	return verse

def sanity_check(bibleverse):
	if bibleverse.chapter == None:
		print("Did not understand what chapter")
		sys.exit(1)
	if bibleverse.book == None:
		print("Did not understand which book")
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

# Fetches a url and returns a html string
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
	if isinstance(bibleverse.verse,int) is False:
		string = '\n' + bibleverse.book + " " + str(bibleverse.chapter) + ":" + str(bibleverse.verse[0]) + "-" + str(bibleverse.verse[1])
	else:
		string = '\n' + bibleverse.book + " " + str(bibleverse.chapter) + ":" + str(bibleverse.verse)
	print(string)

# adds carriage returns to the string
def print_to_console(string):
	counter = 0
	newstring = '\n'
	for c in string:
		counter+=1
		newstring+=c
		if c == "\n": # if we just started a new line, reset the counter
			counter=0
		if counter >= OUTPUT_WIDTH: 
			if c == " ":
				newstring+='\n'
				counter = 0
	print(newstring)

# cleans up a the verse and prints to console
def parse_verse(htmllist):
	consoleout = ''
	skip = 0 # number of entries to skip
	for i in range(0,len(htmllist)):
		string = htmllist[i]
		if skip > 0:
			skip = skip - 1
			continue
		if(string == "("):
			skip = 2
			continue
		if(string == "]"):
			string = string + " "
		if(string == "Read full chapter"):
			break
		consoleout += string
	print_to_console(consoleout)

# cleans up a the footnotes and prints them to console
def parse_footnotes(footnotes):
	consoleout = ''
	# loop over footnotes
	for i in range(0,len(footnotes)):
		fn = footnotes[i]
		skip = True
		if i < 26:
			consoleout += '[' + chr(ord('a')+i) + ']'
		else:
			rem = i % 26
			div = int(i / 26)
			consoleout += '[' + chr(ord('a')+div-1) + chr(ord('a')+rem) + ']'
		for j in range(0,len(fn)):
			if fn[j] == 'Footnotes':
				continue
			if skip: # skips the first line
				skip = False
				continue
			consoleout += fn[j]
		consoleout += '\n'
	print_to_console(consoleout)


# parses the html and prints the verse to console
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
				parse_verse(data)
				break

# parses the html and prints the footnotes to console
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

