#!/usr/bin/env python3



#################################################################################################################################################
#																		#
#																		#
#																		#
#			    _     _  _                    __  _     			  ____             _					#
#			   / \   | |(_) ___  ___   ___   / _|| |_   			 / ___|  ___    __| |  ___  ___				#
#			  / _ \  | || |/ __|/ __| / _ \ | |_ | __|  			| |     / _ \  / _` | / _ \/ __|			#
#			 / ___ \ | || |\__ \\__ \| (_) ||  _|| |_   			| |___ | (_) || (_| ||  __/\__ \			#
#			/_/   \_\|_||_||___/|___/ \___/ |_|   \__|  			 \____| \___/  \__,_| \___||___/			#
#																		#
#																		#
#################################################################################################################################################




import argparse
import requests
from binascii import unhexlify as unhex
import os
import datetime
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
import threading
import urllib


class FBVDownloader:

	def __init__(self, url, filename):
		self.url = url.replace('https://www.facebook.com', 'https://m.facebook.com')
		self.filename = filename
		self.response = requests.get(self.url)
		self.src_code = self.response.text
		self.stream_link = self.get_downloadable_link()
		self.video_src = requests.get(self.stream_link)
		self.videofile = self.video_src.content
		self.filesize = int(self.video_src.headers.get('Content-Length'))
		self.progress = 0


	def sanitize(self, url: str) -> str:
		url = url.replace('%25', '|*-|25|-*|')
		while '%' in url:
			hex_index = url.index('%')
			hex_char = url[hex_index:hex_index+3]
			url = url.replace(hex_char, unhex(hex_char[1:]).decode())

		return url.replace('|*-|25|-*|', '%')


	def get_downloadable_link(self) -> str:
		return self.sanitize([i.split('src=')[-1] for i in self.src_code.split(';') if '.mp4' in i][0])

	def download(self):
		with urllib.request.urlopen(self.stream_link) as response, open(self.filename, 'wb') as output:
			self.progress = 0
			chunk_size = 1024
			bytes_downloaded = 0
			while True:
				chunk = response.read(chunk_size)
				if not chunk:
					self.progress = 100
					break

				output.write(chunk)
				bytes_downloaded += len(chunk)
				current_size = os.path.getsize(self.filename)
				self.progress = current_size / self.filesize * 100


class WindowMode:

	def __init__(self):
		self.root = Tk()
		self.root.geometry('600x150')
		self.root.resizable(False, False)
		img = '''iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABd1BMVEX////W8f970P4+u/4hsf580f7X8f/5/f92zP0XqPsWqPwWqPsWp/wYqPt4zf36/f/5/P9QuvsUo/kUovoUo/pRu/tzxvsSnfYTnfgTnviY1fzc8f4ipPgTnvd3x/vV7f0SmfQRmfac1ftQtPgTmvTX7v13w/kPlfMQlPQQlfQgnPXo9f74/P8nn/UxpPYQlfN6xPkyoPEOj/AOj/IOkPKe0vpjt/c0ofIWke8Ni+4NivDm8/3l8/0Ni/Dy+f5hs/UXku8UjewLh+4Lhe4Lhu5Np/MLhu0VjuwsluwJguoKgezh8P0The0Jgusul+1ssvEHfucIfOkIfOqu1Pj6/P9pr/JutPHU6PsIfuQGe+fl8f0HeOgHeegIfeTW6ftjrO4EeOQFduUFc+UFdOYFc+ZmrO/5/P47k+gDdOIEcuIEceQEcOQEb+MDdeI8lOj6/P75+/5fpusEdN8CcOACb+ECbuFhp+zQ4/ljp+skg+IKdd9kpuvR4/nkEebJAAAAAWJLR0QAiAUdSAAAAAlwSFlzAAAOwwAADsMBx2+oZAAAAAd0SU1FB+cDHAEsMx3Zc+IAAADoSURBVBjTY2AAAkYmZhYWZlY2Bghg5+Dk4ubh4ebi5eMH8QUEhYRFwEBYSJQdKCAmLiEpKSklLSMpKSsux8Agr6AIAkoMyiBKRZVBTV1DU1NTS1tHV09LU1/dgMHQyNjExMQUbLyZsZE5g4WllbWNrR1YwN7K0oHB0cmZgcEF4gBXNyd3Bg9PLwYGLzDf28fL14/BPyCQgSEoOATooNDAwIAwhvCIyKioaAiIiYyNY2CIT0hMSk5KSQESiQmpQJ1p6RmZWdk5OdlZmbl5+SCzCgqLiktKS0uKi8ryof4tr6isqqqsrgGxAee0LsPhAoZyAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIzLTAzLTI4VDAxOjQ0OjUxKzAwOjAwu65NPgAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMy0wMy0yOFQwMTo0NDo1MSswMDowMMrz9YIAAAAZdEVYdFNvZnR3YXJlAHd3dy5pbmtzY2FwZS5vcmeb7jwaAAAAAElFTkSuQmCC'''
		img_set = PhotoImage(data=img)
		self.root.iconphoto(True, img_set)
		self.loaded = False
		
		if os.name == 'posix':
			self.root.title(f'{__file__.split(os.sep)[-1].split(".")[0].title()}')
		else:
			self.root.title(f'Alissoft Facebook Video Downloader')
		
		self.widgets()
		self.root.mainloop()


	def widgets(self):

		self.lbl_URL = Label(self.root, text='URL:').place(x=10,y=10)
		self.entry_URL = Entry(self.root)
		self.entry_URL.place(x=50,y=10,width=530)
		self.entry_URL.focus_set()

		self.btn_load = Button(self.root, text='Load', command=self.load)
		self.btn_load.place(x=180, y=40, width=80)

		self.btn_download = Button(self.root, text='Download', command=self.press_download, state='disabled')
		self.btn_download.place(x=300, y=40, width=80)


	def load(self):
		c = 1
		while True:
			c += 1
			try:
				if not self.loaded:
					url = self.entry_URL.get()
					filename = filedialog.asksaveasfilename(initialdir='./', title='Choose a title and folder', filetypes=(('MP4 Files', '*.mp4'),))
					if not filename:
						break
					elif filename.split('.')[-1] != 'mp4':
						filename += '.mp4'

					try:
						self.video = FBVDownloader(url, filename)
					except:
						messagebox.showwarning(title='URL error', message='Not a valid Facebook URL or the video is restricted.')
						break

					self.loaded = True
					self.btn_download['state'] = 'normal'

					self.entry_downloadable_link = Entry(self.root, fg='blue')
					self.entry_downloadable_link.delete(0, END)
					self.entry_downloadable_link.insert(0, self.video.stream_link)
					self.entry_downloadable_link.place(x=10, y=80, width=500)

					self.btn_open = Button(self.root, text='Open', command=lambda: webbrowser.open(self.video.stream_link))
					self.btn_open.place(x=520, y=75, width=50)
					break
				else:
					self.loaded = False

			except IndexError:
				warning = Toplevel(self.root)
				warning.wm_overrideredirect(True)
				Label(warning, text='Error').pack()
				lbl_warning = Label(warning, text='Wait a few seconds before you retry...').pack()
				Label(warning, text=f"Number of times you've tried: {c}").pack()
				btn_retry = Button(warning, text='Retry', command=lambda: warning.destroy())
				self.load()


	def press_download(self):
		t1 = threading.Thread(target=self.video.download)
		t1.setDaemon(True)
		t1.start()
		self.pg_bar = ttk.Progressbar(self.root, orient='horizontal', length=580, mode='determinate')
		self.pg_bar.place(x=10, y=120)
		self.loaded = False
		self.btn_download['state'] = 'disabled'

		while self.video.progress != 100:
			self.pg_bar['value'] = self.video.progress
			self.root.update_idletasks()



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Facebook Video Downloader')
	parser.add_argument('-u', '--url', type=str, help='URL for the video you want to download', required=False)
	parser.add_argument('-f', '--filename', type=str, help='Filename including the path', required=False)
	parser.add_argument('-d', '--download', help='Downloads the video', required=False, action='store_true')
	parser.add_argument('-l', '--link', help='Get link to the downloadable video stream', required=False, action='store_true')
	args = parser.parse_args()


	if {args.url, args.filename, args.download, args.link} != {None, False}:
		if args.url:
			if not args.filename:
				filename = ''.join([i for i in args.url if i.isalnum()])
			else:
				filename = args.filename
			if filename.split('.')[-1] != 'mp4':
				filename += '.mp4'

			downloader = FBVDownloader(args.url, filename)
			
			if args.download:
				downloader.download()
			if args.link:
				print(downloader.get_downloadable_link())
		else:
			print(f'[!] You have to specify a Facebook URL!\nUse: {__file__} -u URL\n-f FILENAME (optional)\n-d [to download file]\n-l [to get link to the downloadable content]')
	else:
		WindowMode()
