
import urllib.request
import sys

# parse the input


class bibleverse:
	def __init__():
		translation = NASB
		book = NULL
		chapter = NULL
		verse = [NULL,NULL]

	# def parse(string):

def parseInput():
	# TODO
	verse = bibleverse
	verse.book = "Genesis"
	verse.chapter = 1
	verse.verse = [2,3]
	return verse

def generateUrl(bibleverse):
	# TODO
	return "https://www.biblegateway.com/passage/?search=Genesis+1%3A2-3&version=NASB"

def fetchUrl(string):
	# TODO
	return "hello world"

def parseAndPrintHtml(string):
	# TODO
	print(string)

def main():
	verse = parseInput()
	url = generateUrl(verse)
	html = fetchUrl(url)
	parseAndPrintHtml(html)

main()

