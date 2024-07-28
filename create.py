from PyPDF2 import PdfReader, PdfWriter
import PyPDF2
import xml.etree.ElementTree as ET
import os
import re

writer = PdfWriter()

current_item = None
current_page = 0

def addPage(file_path):
    global current_page

    ignore_cases = ['sias.html']
    
    for next_ignore_case in ignore_cases:
        if (next_ignore_case in file_path):
            print(next_ignore_case + ' ignored')
            return -1

    file_path = file_path.replace('../', '')

    case1 = 'relay.html?page='
    case2 = 'routing.html?page='
    case3 = 'ps.html?code='
    case4 = 'overall.html?code='
    case5 = 'sds.html'

    cases = [[case1, ''], [case2, ''], [case3, 'print/'],  [case4, 'overall/'],  [case5, 'sds']]

    for next_case in cases:
        if (next_case[0] in file_path):
            print(file_path)
            file_path = file_path.replace(next_case[0], next_case[1])
            file_path = file_path + '.pdf'
            break

    if ('system.html?code=' in file_path):
        path1 = file_path.replace('system.html?code=', 'system/')
        path1 = path1 + '.pdf'
        print(path1)
        path2 = file_path.replace('system.html?code=', 'text/')
        path2 = path2 + '.pdf'
        i = addPage(path1)
        addPage(path2)
        return i
    
    if ('ncf/nm0280e/sias_2.html' in file_path):
        print(file_path)
        path = file_path.replace('sias_2.html', 'htmlweb/pdf')
        dir_list = os.listdir(path)
        first_file = True
        i = -1
        for next in dir_list:
            fpath = path + '/' + next
            if (os.path.isfile(fpath)):
                if (first_file):
                    first_file = False
                    i = addPage(fpath)
                addPage(fpath)
             
        return i

    if ('ewd/em0280e/sias_2.html' in file_path):
        print(file_path)
        path = file_path.replace('sias_2.html', 'htmlweb/ewd/contents')
        pdf_dirs = ['/relay/pdf', '/routing/pdf', '/system/pdf']
        i = -1
        first_file = True

        for pdf_dir in pdf_dirs:
            next_path = path + pdf_dir
            dir_list = os.listdir(next_path)
            
            for next in dir_list:
                fpath = path + '/' + next
                print(fpath)
                if (os.path.isfile(fpath)):
                    print(fpath)
                    if (first_file):
                        first_file = False
                        i = addPage(fpath)
                    addPage(fpath)
                
        return i
    print(file_path)
    reader = PdfReader(file_path)
    first = True
    index =  -1

    for next_page in reader.pages:
        writer.add_page(next_page)
        if (first):
            first = False
            index = current_page
        
        current_page = current_page + 1

    return index

def processItem(node):
    global current_item
    global current_page

    print(current_page)

    new_index = -1

    for attr in node:
        if (attr.tag == 'url'):
            file_path = attr.text
            new_index = addPage(file_path)

    for attr in node:
        if (attr.tag == 'title'):
            if (new_index > -1):
                writer.add_outline_item(attr.text, new_index, current_item, None)

def processMenu(node):
    global current_item
    global current_page

    for attr in node:
        if (attr.tag == 'title'):
            current_item = writer.add_outline_item(attr.text, current_page, current_item, None)

    for attr in node:
        if (attr.tag == 'item'):
            processItem(attr)

    for attr in node:
        if (attr.tag == 'menu'):
            processMenu(attr)

    current_item = None

tree = ET.parse('contents/pdf.xml')
root = tree.getroot()
for child in root:
    processMenu(child)

result_pdf = open('test.pdf', 'wb')
writer.write(result_pdf)
result_pdf.close()
