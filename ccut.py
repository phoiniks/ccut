#!/usr/bin/python
#-*- coding: utf-8 -*-

#######################################
# phoiniks@grellopolis.de, 17.06.2015 #
#######################################

from sys import stderr, argv
from glob import glob
from argparse import ArgumentParser
from operator import itemgetter
from os.path import basename
from os import remove, getcwd
from time import sleep
import re
import logging

base = basename(getcwd()).upper()

logfile = base.upper() + ".LOG"

try:
    remove(logfile)
except:
    pass

logging.basicConfig(filename=logfile, filemode="w", level=logging.DEBUG, format="%(name)s %(message)s %(asctime)s %(lineno)d")
log = logging.getLogger(base)

log.info("start:")
                    
parser = ArgumentParser()
parser.add_argument('-t', '--type')
parser.add_argument('-f', '--fields')
parser.add_argument('-d', '--delimiter')
parser.add_argument('-x', '--extension')
parser.add_argument('-c', '--complement')


arguments = parser.parse_args()

manual = """
ALWAYS HAVE A LOOK AT THE DOCUMENTATION BEFORE USING CCUT.PY
FOR THE FIRST TIME!

CCUT.PY works just like Linux/UNIX standard cut, but enables you
to count selected fields. Its use, unlike cut's, is not restricted
to plain text files, but can also cope with text files that
contain byte strings (binary data). Unlike with cut you have to
use array notation when extracting chosen fields, so -f0 means the
first field of a line, while -f0,1 means: 1st and 2nd fields, and
so on.

While -d, -x, and -c flags are optional the -t and -f flags are
absolutely mandatory to make the program work.

If you want to extract a field with an extension, i.e., a field
that supposedly contains some kind of file suffix, the program will
try to split that field and then yield the suffix. You specify
this field by use of the -x flag. When using this flag without
there being an extension, the program will write the whole line
and the message \"NO EXTENSION\" to the log file, so that you'll
be informed about the contents of that field.

The program writes two timestamps into the log file: one at start,
the other at the end. Only if the two timestamps are present in the
file can you be sure that the program has completed its work. If
not, something has gone wrong!

Naming convention for the log file: CWD.LOG.
Naming convention for the csv file: CWD.CSV.

The CWD stands for C urrent W orking D irectory, so if you start
the program from within, say, /home/user, it will yield two files:

USER.LOG and USER.CSV.

While working the program displays the name of the file it's
currently reading on the console.

Usage: [./]ccut.py -tEXTENSION_of_input_file(s) -f9,10,11,... -x17 -c0,...

{-t=TYPE}
{-f=FIELD}
{-d=DELIMITER}
{-x=EXTENSION}
{-c=COMPLEMENT}

mandatory:\t-tEXTENSION_of_input_file(s)

mandatory:\t-fFIELD_1,FIELD_2,FIELD_3,...

optional:\t[-d\"DELIMITER\"]

optional:\t[-x\"FIELD, FROM WHICH TO EXTRACT THE EXTENSION\"]

optional:\t[-c\"FIELD_1,FIELD_2,FIELD_3,...]

If you leave out the -d flag, the pipe character (|) is chosen as delimiter.

Although you can leave out the -x and -c flags, it's usually best to use them,
in order to get examples for extension fields that don't contain
extension-like strings, because that's the reason I wrote ccut.py in the
first place!

"""

if not arguments.type:
    print("THE -t FLAG IS MANDATORY IN ORDER FOR THE PROGRAM TO KNOW, WHICH FILE EXTENSION TO CHOOSE!\n")
    sleep(3)
    print(manual)
    exit(-1)
    
if not arguments.fields:
    print("YOU MUST PROVIDE THE -f FLAG FOR GROUPING AND COUNTING THE FIELDS!")
    sleep(3)
    print(manual)
    exit(-1)

if not arguments.delimiter:
    print("-d FLAG (DELIMITER) NOT PROVIDED!")
    print("WILL USE PIPE (|) AS DELIMITER!\n")
    delimiter = "|"
else:
    delimiter = arguments.delimiter
    
if arguments.extension and not arguments.complement:
    print("-x FLAG REQUIRES -c FLAG IN ORDER TO MAKE SENSE!\n")
    exit(-1)

TYPE = "*" + arguments.type
refdats = glob(TYPE)

counter = {}
dictionary = {}
results = {}


def mkDict(line):

    line = line.strip()
    lst = line.split(delimiter)

    key = ""
    fields = []
    
    if "," in arguments.fields:
        fields = map(int, arguments.fields.split(","))
    else:
        key = lst[int(arguments.fields)]

    if len(fields) > 1:
        keyfields = itemgetter(*fields)(lst)
        key = "|".join(keyfields)
        
    if key in counter:
        counter[key] += 1
    else:
        counter[key] = 1

    options = []
    if arguments.extension and "." in lst[int(arguments.extension)]:
        extension = lst[int(arguments.extension)]
        extension = extension.split(".")[-1]
        options.append(extension)
    elif arguments.extension:
        log.info("NO EXTENSION: %s" %line)
        options.append("NO EXTENSION")

    if arguments.complement and "," in arguments.complement:
        complement = map(int, arguments.complement.split(","))
        complement = itemgetter(*complement)(lst)
        options += complement
    elif arguments.complement and "," not in arguments.complement:
        options.append(lst[int(arguments.complement)])

    dictionary[key] = [counter[key]] + options

    results.setdefault(key)

    results[key] = "|".join(map(str, dictionary[key]))


print("\n")

if __name__ == '__main__':

    for refdat in refdats[:]:
        stderr.write("\33[K%s\r" %(refdat))
        map(mkDict, open(refdat).readlines())
                    
    csvfile =  base.upper() + ".CSV"
    
    try:
        remove(csvfile)
    except:
        pass

    print("\33[2J")

    CSV = open(csvfile, "a")
    for key, value in results.items():
        CSV.write("%s|%s\n" %(key, value))
        print("%s|%s\n" %(key, value))
        print("***********************************************************************************************")     
        print("\n\tA L W A Y S   H A V E   A   L O O K   A T   %s!\n" %(logfile))
        print("***********************************************************************************************\n") 
    CSV.close()

    print("\n")

    log.info("end:")
