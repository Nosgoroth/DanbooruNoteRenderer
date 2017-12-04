import os, sys, json, shutil
from pprint import pprint

import requests
from PIL import Image, ImageDraw
import imgkit





if True: #CONFIG
	CONFIG = lambda: None
	CONFIG.DOMAIN = "http://danbooru.donmai.us"





from html.parser import HTMLParser
class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.strict = False
		self.convert_charrefs= True
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)
def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()


def retrieveOrCacheJson(url, cachefile):
	if os.path.exists(cachefile):
		with open(cachefile, 'r') as f:
			return json.load(f)
	else:
		r = requests.get(url)
		d = r.json()
		with open(cachefile, 'w+') as f:
			json.dump(d, f)
		return d


def download_file(url, local_filename):
	try:
		r = requests.get(url, stream=True)
		with open(local_filename, 'wb') as f:
			shutil.copyfileobj(r.raw, f)
		return True
	except:
		raise



class DanbooruNote:
	rawdata = None

	id = None
	x = 0
	y = 0
	width = 0
	height = 0
	is_active = False
	body = ""

	def __init__(self, rawdata):
		self.rawdata = rawdata
		for k, v in rawdata.items():
			setattr(self, k, v)

	def render(self, outfile='out.png', padding=2):
		body = self.body

		textboxCss = {
			#"width": "%dpx" % width,
			"hyphens": "auto",
			"text-align": "center",
		}

		if self.width < 30 and self.width*3 < self.height:
			stripped = strip_tags(body)
			if len(stripped) > 0:
				lined = "<br/>".join(list(stripped))
				newbody = body.replace(stripped, lined)

				if newbody == body:
					body = lined
					textboxCss["font-size"] = "1.2em"
					textboxCss["line-height"] = "110%"
				else:
					body = newbody


		# Final variable computing
		width = self.width + (padding*2)
		height = self.height + (padding*2)
		cssString = ' '.join('{}: {};'.format(key, value) for key, value in textboxCss.items())

		# Making the html
		html = """<html><head>
		<meta name="imgkit-width" content="%d"/>
		<meta name="imgkit-format" content="png"/>
		<meta name="imgkit-quiet" content=""/>
		<meta name="imgkit-encoding" content="UTF-8"/>
		<style type="text/css">
			* {
				margin: 0 !important;
				padding: 0 !important;
				
			}
			html,body {
				font-family: "Wild Words", sans-serif;
				font-size: 14px;
				padding: %d !important;
			}
			#textbox { %s }
		</style>
		</head><div id="textbox">%s</div></html>
		""" % (width, padding, cssString, body)

		imgkit.from_string(html, outfile)


class DanbooruPost:

	postid = None
	postdata = None
	notedata = None
	notes = []

	def __init__(self, postid, debug=False):
		self.postid = postid
		self.debug = debug

	def getData(self):
		os.makedirs("cache", exist_ok=True)

		if self.debug: print("Retrieving info... ", end='', flush=True)
		self.retrieveInfo()
		if self.debug: print("done.")
		
		if self.debug: print("Retrieving image... ", end='', flush=True)
		self.retrieveOrCacheImage()
		if self.debug: print("done.")


	def render(self, output=None):
		self.renderNotes()
		self.saveToOutput(output=output)
		if self.debug: print("done.")

	def renderNotes(self):
		self._renderedImg = Image.open(self.getImageCacheFilepath())
		tw, th = self._renderedImg.size

		i = 0
		for note in self.notes:
			i += 1
			if self.debug: print("Rendering note %d of %d... " % (i, len(self.notes)), end='', flush=True)
			of = "cache/noterender_%d.png" % note.id
			note.render(padding=2, outfile=of)
			with Image.open(of) as _noteimg:
				w, h = _noteimg.size
				dx, dy = (w - note.width, h - note.height)
				x, y = (int(note.x - dx/2), int(note.y - dy/2))
				if x<0: x=0
				if y<0: y=0
				if x+w>tw: x=tw-w
				if y+h>th: y=th-h
				self._renderedImg.paste(_noteimg,(x,y))
			os.remove(of)
			if self.debug: print("done.")

	def saveToOutput(self, output=None):
		if self.debug: print("Saving output... ", end='', flush=True)
		self._renderedImg.save( output if output else self.getOutputFilepath(suffix="_rendered") )
		if self.debug: print("done.")


	def retrieveInfo(self):
		self.postdata = retrieveOrCacheJson(
			CONFIG.DOMAIN+"/posts/%d.json" % self.postid,
			"cache/post_%d.json" % self.postid
		)
		self.notedata = retrieveOrCacheJson(
			CONFIG.DOMAIN+"/notes.json?group_by=note&search[post_id]=%d" % self.postid,
			"cache/notes_%d.json" % self.postid
		)

		self.notes = []
		for notejson in self.notedata:
			self.notes.append(DanbooruNote(notejson))

	def getImageExtension(self):
		return self.postdata["large_file_url"].split(".")[-1]
		
	def getImageCacheFilepath(self, suffix=""):
		return "cache/image%s_%d.%s" % (suffix, self.postid, self.getImageExtension())

	def getOutputFilepath(self, suffix=""):
		return "output/%d%s.%s" % (self.postid, suffix, self.getImageExtension())

	def retrieveOrCacheImage(self):
		url = CONFIG.DOMAIN+self.postdata["large_file_url"]
		cachefile = self.getImageCacheFilepath()
		if not os.path.exists(cachefile):
			download_file(url, cachefile)




def main():
	try: id = int(sys.argv[1])
	except:
		print("No ID provided")
		return
	print("Running with", id)
	print()
	post = DanbooruPost(id, debug=True)
	post.getData()
	post.render()
	print()
	print("Run complete")


if __name__ == '__main__':
	main()
