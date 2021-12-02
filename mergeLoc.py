#! /usr/bin/env python3
import os
import re
import xml.etree.ElementTree as ET

xmlArrs = {"Saury.xml",
           "Saury-ja-JP.xml",
           "Saury-ko-KR.xml",
           "Saury-zh-CN.xml",
           "Saury-zh-Hant.xml",
           "Saury-ar.xml",
           "Saury-de.xml",
           "Saury-es.xml",
           "Saury-fr.xml",
           "Saury-hi.xml",
           "Saury-ru.xml"}

docDirectory = os.getenv("HOME")+"/Documents/"
print(docDirectory)


def appendChild(originList, root, fileName):
    for text in root.findall('./texts/text'):
        originList.append(text)
        print("key = " + text.get("name"))
    return


def writeFile(fileName):
    nameRegex = re.sub('\(.*\)',"",fileName)
    #文件路径
    destFilePath = docDirectory + "localization_merged/"
    #创建文件夹
    if not os.path.exists(destFilePath):
        os.makedirs(destFilePath)

    tree = ET.parse(docDirectory+"localization_wanna_merge/"+fileName)
    root = tree.getroot()

    treeOrigin = ET.parse(docDirectory + "localization/" + fileName)
    rootOrigin = treeOrigin.getroot()
    listOrigin = rootOrigin.find('./texts')

    appendChild(listOrigin, root, fileName)

    #destTree = ET.ElementTree(rootOrigin)
    #destTree.write(destFilePath + fileName, "UTF-8")

    treeOrigin.write(destFilePath + fileName, "UTF-8")
    return

for name in xmlArrs:
    writeFile(name)


