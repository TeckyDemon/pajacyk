import re
import requests
from os import _exit
from sys import stdout
from time import sleep
from random import choice
from argparse import ArgumentParser
from traceback import format_exc
from threading import Thread,Lock,Event

def logv(message):
	stdout.write('%s\n'%message)
	if message.startswith('[ERROR]'):
		_exit(1)
def log(message):
	global args
	if args.debug:
		logv(message)
def get_proxies():
	global args
	if args.proxies:
		proxies=open(args.proxies,'r').read().strip().split('\n')
	else:
		proxies=requests.get('https://www.proxy-list.download/api/v1/get?type=https&anon=elite').content.decode().strip().split('\r\n')
	log('[INFO] %d proxies successfully loaded!'%len(proxies))
	return proxies
def bot(id):
	global args,lock,exception,exception_event,proxies
	while True:
		try:
			with lock:
				if len(proxies)==0:
					proxies.extend(get_proxies())
				proxy=choice(proxies)
				proxies.remove(proxy)
			log('[INFO][%d] Connecting to %s'%(id,proxy))
			response=requests.get(
				'https://www.pajacyk.pl/wp-ajax.php',
				params={
					'kliki':1
				},
				proxies={
					'https':proxy
				}
			)
			logv(response.content.decode())
		except (OSError,KeyboardInterrupt):pass
		except:
			exception=format_exc()
			exception_event.set()

if __name__=='__main__':
	try:
		parser=ArgumentParser()
		parser.add_argument('-t','--threads',type=int,help='set number of the threads',default=15)
		parser.add_argument('-p','--proxies',help='set the path to the list with the proxies')
		parser.add_argument('-d','--debug',help='show all logs',action='store_true')
		args=parser.parse_args()
		lock=Lock()
		exception_event=Event()
		proxies=[]
		for i in range(args.threads):
			t=Thread(target=bot,args=(i+1,))
			t.daemon=True
			t.start()
		exception_event.wait()
		logv('[ERROR] %s'%exception)
	except KeyboardInterrupt:_exit(0)
	except:_exit(1)
