#!/usr/bin/python

# * Thu Jul 11 2013 Thomas Uphill <tuphill@costco.com> 
# - encrypt a password with sha512 by default
# - generate a crypt suitable for placement in /etc/shadow

import crypt
from random import randint
import string
import getpass
from optparse import OptionParser
import sys

# command line arguments
help_text = """%prog [options]
encrypt a password in a format suitable for /etc/shadow
sha512 is used by default
salt is calculated using randint if not supplied
"""
parser = OptionParser(usage=help_text)
parser.add_option("-s","--salt", dest="salt",action="store",type="string",
	help="encryption salt", metavar="salt")
parser.add_option("-p","--password", dest="passwd",action="store",type="string",
	help="password to encrypt", metavar="password")
parser.add_option("-a","--algorithm", dest="algo",action="store",type="string",
	help="algorithm to use (sha512, sha256, md5",metavar="algorithm")

(options,args) = parser.parse_args()

# generate salt
try:
  slen = len(options.salt)
  salt = options.salt
  if slen < 8:
    sys.stderr.write("WARNING: Salt length should be at least 8 characters\n")
except:
  salt_string = './' + string.ascii_letters + string.digits
  salt = ''.join([salt_string[randint(0,len(salt_string)-1)] for x in range(8)])

try:
  plen = len(options.passwd)
  passwd = options.passwd
  if plen < 8:
    sys.stderr.write("WARNING: Password should be at least 8 characters\n")
except:
  passwd = getpass.getpass()
  plen = len(passwd)
  if plen < 8:
    sys.stderr.write("WARNING: Password should be at least 8 characters\n")

try:
  len(options.algo)
  algos = {'sha512': 6,
    'sha256': 5,
    'md5': 1,
  }
  try: 
    algo = algos[options.algo]
  except:
    sys.stderr.write("ERROR: Unknown encryption algorithm %s" % options.algo)
    sys.exit(1)
except:
  algo = '6'
print crypt.crypt(passwd, "$%s$%s" % (algo,salt))
