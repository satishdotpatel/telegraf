#!/bin/python
import re
import sys
import socket
import argparse
Print = sys.stdout.write

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", help="domain name (e.g. foo)", required=True)
parser.add_argument("-p", "--proxy", help="IP address of mediaproxy server", required=False)
parser.add_argument("-o", "--org", help="organization name", required=False)

args = parser.parse_args()
# Parse Domain
if args.domain:
    domain = args.domain
else:
    die('Must set a Domain. Please see the help page.')

# Set org if different from vivox.com
if args.org:
    org = args.org
else:
    org = 'vivox.com'

# Set proxy if one is given otherwise default to proxy.$domain.$org
if args.proxy:
    proxy = args.proxy

# initializ variables
header = 'mproxystats,domain='

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
total = 0
for i in (25060, 25062, 25064, 25066, 25068, 25070, 25072, 25074):
  conn.connect((proxy, i))
  conn.send('status\n')
  data = conn.recv(16777216)
  conn.close()
  conn = socket.socket()

  count = 0

  for line in data.split('\n'):
     if line.startswith('stream '):
          count += 1
        # print line
  #print count
  total = count + total

#print "total:", total

Print (header)
Print (domain)
Print (" ")
print "mproxystats={0}".format(total)
