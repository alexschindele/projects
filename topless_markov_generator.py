__author__ = "alexander.schindele"

import os
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET


fname_source = r'C:\messages.htm'
fname_dest   = r'C:\Users\alexschindele\Documents.txt'


# with open(fname_source, encoding="utf8") as source, open(fname_dest,  "w", encoding="utf8") as dest:
#
#     context = ET.iterparse(source, events=("start", "end"))
#
#     # turn it into an iterator
#     context = iter(context)
#     # get the root element
#
#     for event, elem in context:
#         if event == "end":
#             if "class" in elem.attrib and elem.attrib["class"] == "user":
#                 if elem.text is not None:
#                     dest.write(elem.text + "\n")
#             if elem.tag == "p":
#                 if elem.text is not None:
#                     dest.write(elem.text + "\n")

names = ["Chris Schindele", "Miwako Schindele Murayama"]
folder = r"C:\Users\alexschindele\Documents"
# names = ["Chamsi Hssaine", "Anthony Shu", "Alex Schindele", "Stephen Li", "Kai Okada", "Zach Atkins", "Joy Zou", "Mikhail Khodak", "Michael Chang"]
# names = ["Anna Mazarakis", "Oliver Kim", "Shreshth Mehrotra", "Adharsh Kumar"]
# for name in names:
#     fname_write = name + ".txt"
#     fname = os.path.join(folder, fname_write)
#     output = open(fname, "w", encoding="utf8")
#     file = open(fname_dest, encoding="utf8")
#     for line in file:
#         line = line.replace("\n", "")
#         if line == name:
#             output.write(file.readline())
#     output.close()
#     file.close()

import markovify
name = "Miwako Schindele Murayama"
name = name + ".txt"
fname = os.path.join(folder, name)
# Get raw text as string.
with open(fname, encoding="utf") as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text)

# Print five randomly-generated sentences
for i in range(3):
    print(text_model.make_sentence())

# # Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
#     print(text_model.make_short_sentence(140))