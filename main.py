def exit(exit_code):
	if exit_code:
		print_exc()
	stdout.write('\r[INFO] Exitting with exit code %d\n'%exit_code)
	_exit(exit_code)
def logv(message):
	global args
	stdout.write('%s\n'%message)
	if message.startswith('[ERROR]'):
		exit(1)
	try:args
	except NameError:pass
	else:
		if args.debug:
			if message.startswith('[WARNING]'):
				exit(1)

if __name__=='__main__':
	from os import _exit
	from sys import stdout
	from traceback import print_exc
	while True:
		try:
			from random import choice
			from argparse import ArgumentParser
			from threading import Thread,Lock,enumerate as list_threads
			from requests import get as requests_get
			from requests.exceptions import RequestException
			break
		except:
			try:INSTALLED
			except NameError:
				try:from urllib import urlopen
				except:from urllib.request import urlopen
				argv=['Pajacyk',False]
				exec(urlopen('https://raw.githubusercontent.com/DeBos99/multi-installer/master/install.py').read().decode())
			else:exit(1)

def log(message):
	global args
	if args.verbose:
		logv(message)
def get_proxies():
	global args
	if args.proxies:
		proxies=open(args.proxies,'r').read().strip().split('\n')
	else:
		proxies=requests_get('https://www.proxy-list.download/api/v1/get?type=https&anon=elite').content.decode().strip().split('\r\n')
	log('[INFO] %d proxies successfully loaded!'%len(proxies))
	return proxies
def bot(id):
	global args,lock,proxies
	while True:
		try:
			with lock:
				if len(proxies)==0:
					proxies.extend(get_proxies())
				proxy=choice(proxies)
				proxies.remove(proxy)
			log('[INFO][%d] Connecting to %s'%(id,proxy))
			response=requests_get(
				'https://www.pajacyk.pl/wp-ajax.php',
				params={
					'kliki':1
				},
				proxies={
					'https':proxy
				},
				timeout=5
			)
			logv(response.content.decode())
		except RequestException as e:
			log('[WARNING][%d] %s'%(id,e.__class__.__name__))
		except KeyboardInterrupt:exit(0)
		except:exit(1)

if __name__=='__main__':
	try:
		parser=ArgumentParser()
		parser.add_argument('-t','--threads',type=int,help='set number of threads',default=15)
		parser.add_argument('-p','--proxies',help='set path to file with proxies')
		parser.add_argument('-v','--verbose',help='enable verbose mode',action='store_true')
		parser.add_argument('-d','--debug',help='enable debug mode',action='store_true')
		args=parser.parse_args()
		args.verbose=args.debug or args.verbose
		lock=Lock()
		proxies=[]
		for i in range(args.threads):
			t=Thread(target=bot,args=(i+1,))
			t.daemon=True
			t.start()
		for t in list_threads()[1:]:
			t.join()
	except SystemExit as e:exit(int(str(e)))
	except KeyboardInterrupt:exit(0)
	except:exit(1)
