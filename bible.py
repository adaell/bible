
import urllib.request
import sys

# Width of console output
TRANSLATION = 'NASB'
OUTPUT_WIDTH=80 

# a class for storing bible verse information
class bibleverse:
	def __init__(self):
		self.translation = TRANSLATION
		self.book = None
		self.chapter = None
		self.verse = [None,None]

# parses the console arguments and returns a bibleverse
def parseInput():
	import sys

	# wrong number of arguments
	if len(sys.argv) > 3:
		print("Invalid number of arguments. Was expecting two (Chapter Verse). Try `bible Genesis 2:3-4`")
		exit(1)

	# TODO

	verse = bibleverse()
	verse.book = "Genesis"
	verse.chapter = 1
	verse.verse = [2,3]
	return verse

# Takes a bibleverse and returns a url to the verse on biblegateway
def generateUrl(bibleverse):
	if(len(bibleverse.verse) == 1):
		chap = str(bibleverse.chapter) + "%3A" + str(bibleverse.verse[0])
	else:
		chap = str(bibleverse.chapter) + "%3A" + str(bibleverse.verse[0]) + '-' + str(bibleverse.verse[1])
	string = "https://www.biblegateway.com/passage/?search=" + bibleverse.book + "+" + chap + "&version=" + bibleverse.translation
	temp = "https://www.biblegateway.com/passage/?search=Genesis+1%3A2-3&version=NASB"
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
	if len(bibleverse.verse) > 0:
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
	# newstring += '\n'
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
		consoleout += '[' + chr(ord('a')+i) + ']'
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

