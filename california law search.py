import tkinter as tk
from tkinter import ttk
from tkinter import *
from xhtml2pdf import pisa    
import numpy as np 
import warnings, tkFileDialog, shutil, sys, os

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import time, re
from selenium import webdriver
from bs4 import BeautifulSoup

# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            sourceHtml,                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err


# url = "http://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=HSC&sectionNum=1439.51.&highlight=true&keyword=transgender+gender%20identity"
url = "http://leginfo.legislature.ca.gov/faces/codes.xhtml"
driver = webdriver.Chrome("C:\chromedriver")
driver.get(url)
driver.find_element_by_xpath('//*[@id="j_idt92:textsearchtab"]').click()
search_box = driver.find_element_by_name('codeSearchForm:or_one')
search_box.send_keys("transgender")
search_box = driver.find_element_by_name('codeSearchForm:or_two')
search_box.send_keys("gender identity")
search_box = driver.find_element_by_name('codeSearchForm:selectAll').click()
search_box = driver.find_element_by_name('codeSearchForm:execute_search').click()


time.sleep(np.random.rand()*2) #some websites with good security AIs (read, "not government websites") will check if you're performing actions faster than a human could and at a very steady speed, so random pauses like this will help you avoid that problem. in this program they're mostly useless, however.

with open("newfile.txt", 'w') as outfile: 
	while True:
		for link in [1,2,3,4,5,6,7,8,9,10]:
			driver.find_element_by_xpath('//*[@id="j_idt146:dtable"]/tbody/tr['+str(link)+']/td/div/a').click()
			soup = BeautifulSoup(driver.page_source, "html.parser")
			lawtext = soup.find(id="codeLawSectionNoHead")
			outfile.write(str(lawtext))
			outfile.write("<p></p><hr><p></p>")
			driver.back()
		try:
		    driver.find_element_by_name('datanavform:nextTen').click()
		except: break

outputFilename = "laws.pdf"

with open('newfile.txt', 'r') as myfile:
	data=myfile.read().replace('\n', '')
	convertHtmlToPdf(data, outputFilename)