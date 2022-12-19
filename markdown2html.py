#!/usr/bin/python3
"""This module defines a scrip that takes an argument 2 strings"""
from sys import argv, stderr
from os.path import exists
from hashlib import md5
import re

if __name__ == "__main__":

    if len(argv) <= 3:
        print("Usage: ./markdown2html.py README.md README.html \n", file=stderr, end="")
        exit(1)

    if not exists(argv[1]):
        print("Missing {}".format(argv[1]), file=stderr)
        exit(1)

    with open(argv[1], 'r', encoding='utf-8') as markdown:
        with open(argv[2], 'w', encoding='utf-8') as html:

            isUnorderedOpen, isOrderedOpen, isParagraphOpen = False, False, False
            numberUnorderedList, numberOrderedList,  = 0, 0
            numberHeading, numberParagraph = 0, 0

            index = markdown.readlines()
            count = 0

            for line in index:
                count += 1

                # Parsing bold and emphasis text
                line = line.replace("**", "<b>", 1)
                line = line.replace("**", "</b>", 1)
                line = line.replace("__", "<em>", 1)
                line = line.replace("__", "</em>", 1)

                # Converting in MD5
                findRegex = re.findall(r'\[\[.+?\]\]', line)
                if findRegex:
                    line = line.replace(findRegex[0],
                                        md5(findRegex[0].encode()).hexdigest())

                # Removing '(', ')' 'C', 'c'
                findRegex2 = re.findall(r'\(\(.+?\)\)', line)
                if findRegex2:
                    line = line.translate({ord(i): None for i in '()Cc'})

                header = line.strip().count('#')
                unordered = line.strip().count('-')
                ordered = line.strip().count('*')

                # Translate Headings Markdown
                if header > 0:

                    # Check style before
                    if numberUnorderedList > 0 and numberHeading == 0:
                        html.write("</ul>\n")
                        numberUnorderedList = 0
                        isUnorderedOpen = False
                    elif numberOrderedList > 0 and numberHeading == 0:
                        html.write("</ol>\n")
                        numberOrderedList = 0
                        isOrderedOpen = False
                    elif numberParagraph > 0 and numberHeading == 0:
                        html.write("</p>\n")
                        numberParagraph = 0
                        isParagraphOpen = False

                    # Create header
                    title = line.lstrip('# ').rstrip("\n")
                    html.write("<h{}>{}</h{}>\n".format(header, title, header))
                    numberHeading += 1

                # Translate Unordered List Markdown
                elif unordered == 1:

                    # Check style before
                    if numberOrderedList > 0 and numberUnorderedList == 0:
                        html.write("</ol>\n")
                        numberOrderedList = 0
                        isOrderedOpen = False
                    elif numberParagraph > 0 and numberUnorderedList == 0:
                        html.write("</p>\n")
                        numberParagraph = 0
                        isParagraphOpen = False

                    # Create unordered list
                    title = line.lstrip('- ').rstrip("\n")
                    if not isUnorderedOpen:
                        html.write("<ul>\n")
                        isUnorderedOpen = True
                    html.write("\t<li>{}</li>\n".format(title))
                    numberUnorderedList += 1
                    if count == len(index) and numberUnorderedList > 0:
                        html.write("</ul>\n")
                        isUnorderedOpen = False

                # Translate Ordered List Markdown
                elif ordered == 1:

                    # Check style before
                    if numberUnorderedList > 0 and numberOrderedList == 0:
                        html.write("</ul>\n")
                        numberUnorderedList = 0
                        isUnorderedOpen = False
                    elif numberParagraph > 0 and numberOrderedList == 0:
                        html.write("</p>\n")
                        numberParagraph = 0
                        isParagraphOpen = False

                    # Create ordered list
                    title = line.lstrip('* ').rstrip("\n")
                    if not isOrderedOpen:
                        html.write("<ol>\n")
                        isOrderedOpen = True
                    html.write("\t<li>{}</li>\n".format(title))
                    numberOrderedList += 1
                    if count == len(index) and numberOrderedList > 0:
                        html.write("</ol>\n")
                        isOrderedOpen = False

                # Translate Paragraph Markdown
                elif header == 0 and unordered == 0 and ordered == 0:

                    # Check style before
                    if numberUnorderedList > 0 and numberParagraph == 0:
                        html.write("</ul>\n")
                        numberUnorderedList = 0
                        isUnorderedOpen = False
                    elif numberOrderedList > 0 and numberParagraph == 0:
                        html.write("</ol>\n")
                        numberOrderedList = 0
                        isOrderedOpen = False
                    if index[count - 1] == "\n" and numberParagraph == 0:
                        continue

                    # Create paragraph
                    numberParagraph += 1
                    if not isParagraphOpen:
                        html.write("<p>{}".format(line.rstrip("\n")))
                        isParagraphOpen = True
                    elif index[count - 1] == "\n" and numberParagraph > 0:
                        html.write("</p>\n")
                        numberParagraph = 0
                        isParagraphOpen = False
                    elif numberParagraph > 1:
                        html.write("<br/>{}".format(line.rstrip("\n")))
                    if count == len(index):
                        html.write("</p>\n")
                        isParagraphOpen = False
    exit(0)
