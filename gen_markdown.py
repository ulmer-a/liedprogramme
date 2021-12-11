#! /usr/bin/python3

from os import walk
import re

def start_table(name):
    print("## %s" % (name))

def node(text):
    print("- %s: " % (text))

def subnode(text):
    print("%s" % (text))

basepath = "www/files"
html_basepath = "files/"

f = []
for (dirpath, dirnames, filenames) in walk(basepath):
    f.extend(filenames)
    break
f = sorted(f)

def splitup_regular(filename):
    date = filename.split('_')[1].split('.')[0]
    code = filename.split('_')[0]
    type = code[0]
    year = code[-1]
    num = int(code[1:-1])
    return (type, num, year, date)

def handle_regular(letter, description):
    list_jahreskreis = {}
    jahreskreis = re.compile("%c[0-9]+[A-Z]_[0-9]{4}-[0-9]{2}-[0-9]{2}\.pdf" % (letter))
    for file in f:
        m = jahreskreis.match(file)
        if not m:
            continue
        jkn = int(m.group().split('_')[0][1:-1])
        if jkn in list_jahreskreis:
            list_jahreskreis[jkn].append(file)
        else:
            list_jahreskreis[jkn] = [ file ]

    for so in list_jahreskreis:
        node("[%d.] %s" % (so, description))
        str = ""
        for filename in list_jahreskreis[so]:
            type, num, year, date = splitup_regular(filename)
            str += "  - [%c (%s)](%s%s)\n" % (year, date, html_basepath, filename)
        subnode(str)

def handle_hochfest():
    list_hochfest = {}
    hochfest = re.compile("S[0-9]+[A-Z]_[A-Za-z-]+_[0-9]{4}-[0-9]{2}-[0-9]{2}\\.pdf")
    for file in f:
        m = hochfest.match(file)
        if not m:
            continue
        jkn = int(m.group().split('_')[0][1:-1])
        if jkn in list_hochfest:
            list_hochfest[jkn].append(file)
        else:
            list_hochfest[jkn] = [ file ]

    for so in list_hochfest:
        node("%s" % (list_hochfest[so][0].split('_')[1].replace('-', ' ')))
        str = ""
        for filename in list_hochfest[so]:
            year = filename.split('_')[0][-1]
            date = filename.split('_')[2].split('.')[0]
            str += "  - [%c (%s)](%s%s)\n" % (year, date, html_basepath, filename)
        subnode(str)

start_table("Sonntage im Advent")
handle_regular('A', "Adventsonntag")

start_table("Sonntage in der Weihnachtszeit")
handle_regular('W', "Sonntag nach Weihnachten")

start_table("Sonntage in der Fastenzeit")
handle_regular('F', "Fastensonntag")

start_table("Sonntage in der Osterzeit")
handle_regular('O', "Sonntag in der Osterzeit")

start_table("Feste und Hochfeste")
handle_hochfest()

start_table("Rorate")
handle_regular('R', "Rorate")

start_table("Sonntage im Jahreskreis")
handle_regular('J', "Sonntag im Jahreskreis")
