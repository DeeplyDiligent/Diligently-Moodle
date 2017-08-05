from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import codecs
import datetime
import os
import difflib
import re
import subprocess
from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time
import datetime

def show_diff(seqm):
    """Unify operations between two compared strings seqm is a difflib.SequenceMatcher instance whose a & b are strings"""
    output= []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append("<ins>" + seqm.b[b0:b1] + "</ins>")
        elif opcode == 'delete':
            output.append("<del>" + seqm.a[a0:a1] + "</del>")
        elif opcode == 'replace':
            output.append("<del>" + seqm.a[a0:a1] + "</del>")
            output.append("<ins>" + seqm.b[b0:b1] + "</ins>")
        else:
            raise RuntimeError("unexpected opcode")
    return ''.join(output)

baseurl = "http://moodle.vle.monash.edu/my/"


checklist = ['http://moodle.vle.monash.edu/course/view.php?id=38460','http://moodle.vle.monash.edu/course/view.php?id=38656','http://moodle.vle.monash.edu/course/view.php?id=38055','http://moodle.vle.monash.edu/course/view.php?id=38062']
sitemainreg = {}

mydriver = webdriver.PhantomJS(r"C:\Users\deep\Apps\ChromeDriver\phantomjs-2.1.1-windows\bin\phantomjs.exe")

#mydriver = webdriver.Chrome()
mydriver.get(baseurl)
username = mydriver.find_element_by_id("userNameInput")
password = mydriver.find_element_by_id("passwordInput")

username.send_keys("dbha0003")
password.send_keys("$1Kiddies7")

mydriver.find_element_by_id("submitButton").click()

# for site in checklist:
#     mydriver.get(site)
#
#     elem = mydriver.find_element_by_id('page-header')
#     h1 = elem.find_elements_by_tag_name('h1')
#     sitename = (h1[0].get_attribute('innerHTML')[0:7])
#
#     elem = mydriver.find_element_by_css_selector('#region-main')
#     mainarea = elem.get_attribute('innerHTML')
#     mainarea = re.sub(r"(yui)\w+",'someyuithing',mainarea)
#     sitemainreg[sitename]=str(mainarea)
#
#     completeName = os.path.join('./sites/', sitename+".html")
#     try:
#         File = open(completeName,encoding='utf-8').read()
#     except FileNotFoundError:
#         File=''
#
#     sm= difflib.SequenceMatcher(None, File, sitemainreg[sitename])
#     sitemainreg[sitename] = (show_diff(sm))
#     if not(mainarea==sitemainreg[sitename]):
#         print('there are changes to '+sitename)
#         w.ShowWindow("Moodle Changes","Change in "+sitename)
#         completeName = os.path.join('./sites/', sitename+"_CHANGED.html")
#         file_object = codecs.open(completeName, "w", "utf-8")
#         html = sitemainreg[sitename]
#         file_object.write(html)
#         completeName = os.path.join('./sites/', sitename+".html")
#         file_object = codecs.open(completeName, "w", "utf-8")
#         html = mainarea
#         file_object.write(html)
#         completeName = os.path.join('./sites/', sitename+"_OLD.html")
#         file_object = codecs.open(completeName, "w", "utf-8")
#         html = File
#         file_object.write(html)
# mydriver.find_element_by_id('expandable_branch_20_38460').click()
# time.sleep(2)
subjects = ['ECC1000','FIT1049','FIT1013','ACC1200']
namesofsitestowrite = []
already_clicked = []
for j in range(1,10):
    elements = mydriver.find_elements_by_css_selector("p.tree_item.branch")
    elementswithicons = mydriver.find_elements_by_css_selector("p.tree_item.branch.hasicon")
    elemids = [i.get_property("id") for i in elements if i.get_property("id") != '' and 'expandable' in i.get_property("id")]
    idforelementswithicons = [i.get_property("id") for i in elementswithicons if i.get_property("id") != '' and 'expandable' in i.get_property("id")]
    for id in idforelementswithicons:
        if id in elemids:
            elemids.remove(id)
    for i in elemids:
        if i not in already_clicked:
            print(i)
            already_clicked.append(i)
            pattern = "\>(.*?)\<"
            writingofelement = re.search(pattern,mydriver.find_element_by_id(i).get_attribute('innerHTML')).group(1)
            if j!=1 or (j==1 and any(word in writingofelement for word in subjects)):
                if j == 1:
                    namesofsitestowrite.append([writingofelement,i])
                # print inside of i
                print(writingofelement)
                locate = mydriver.find_element_by_id(i)
                action = webdriver.ActionChains(mydriver)
                action.move_to_element_with_offset(locate, 0, 10)
                action.click()
                action.perform()
                try:
                    element = WebDriverWait(mydriver, 3).until(
                        EC.presence_of_element_located((By.ID, i+"_group"))
                    )
                except:
                    print("Element "+writingofelement+" with id "+i+" cannot expand!")
html = "<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />"
for i in namesofsitestowrite:
    html += '<h1>'+i[0]+'</h1>'
    html += mydriver.find_element_by_id(i[1]+"_group").get_attribute('innerHTML')
    html += '<br><br>'
i = datetime.datetime.now()
completeName = os.path.join('./sites/', "moodle "+i.strftime('%Y.%m.%d %H.%M.%S')+".html")
file_object = codecs.open(completeName, "w", "utf-8")
file_object.write(html)
print(completeName + " has been written!")
