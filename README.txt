CCUT.PY can be used to analize CSV-like files that contain path
lists and file names in order to count mimetypes, extensions, etc.

You will always find the most recent version on github.com!

Please read this documentation carefully!

A L W A Y S   W O R K   W I T H   A   C O P Y   O F   T H E   O R I G I N A L !

For security reasons make sure you always work with a copy of
the files you want to analize, copying them to a directory of your
choice! CCUT.PY only works correctly when invoked from the
directory your files are actually in!

CCUT.PY works just like Linux/UNIX standard cut, but enables you
to count selected fields. Its use, unlike cut's, is not restricted
to plain text files, it copes with text files that
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
and the message "NO EXTENSION" to the log file, so that you'll
be informed about the contents of that field, but only if you
provide the field where your example text is located, i.e. using
the -c flag -- because this is the distinctive feature by which
to tell the results apart! 

The program writes two timestamps into the log file: one at start,
the other at the end. Only if the two timestamps are present in the
log file can you be sure that the program has completed its work. If
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

mandatory:	-tEXTENSION_of_input_file(s)

mandatory:	-fFIELD_1,FIELD_2,FIELD_3,...

optional:	[-d"DELIMITER"]

optional:	[-x"FIELD, FROM WHICH TO EXTRACT THE EXTENSION"]

optional:	[-c"FIELD_1,FIELD_2,FIELD_3,...]

If you leave out the -d flag, the pipe character (|) is chosen as delimiter.

Although you can leave out the -x and -c flags, it's usually best to use them,
in order to get examples for extension fields that don't contain
extension-like strings, because that's the reason I wrote ccut.py in the
first place!
