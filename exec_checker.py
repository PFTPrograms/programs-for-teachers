import re


def writeok():
    print('Ok')


def writeerr():
    print('Error')


def writebad():
    print('Bad checker')


def exec_(c, data, onok=writeok, onerr=writeerr, onbad=writebad):
    try:
        r = re.compile(c)
    except re.error:
        onbad()
    else:
        if r.match(data):
            onok()
        else:
            onerr()
