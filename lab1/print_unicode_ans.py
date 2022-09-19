# -*- coding: utf-8 -*-
import sys
import unicodedata

def print_unicode_table(words):
    print("decimal hex chr {0:^40}".format("name"))
    print("------- ----- --- {0:-<40}".format(""))

    code = ord(" ")
    end = min(0xD800, sys.maxunicode)

    while code < end:
        c = chr(code)
        name = unicodedata.name(c, "*** unknown ***")
        isWord = True
        for word in words:
            if word not in name.lower():
                isWord = False
                break
        if isWord:
            print("{0:7} {0:5X} {0:^3c} {1}".format(code, name.title()))
        code += 1
# End print_unicode_table

# Start main script
words = []
if len(sys.argv) > 1:
    if sys.argv[1] in ("-h", "--help"):
        print("usage: {0[0]} [string]".format(sys.argv[0]))
        words = None
    else:
        for word in sys.argv[1:]:
            words.append(word.lower())
if words is not None:
    print_unicode_table(words)
#End main script
