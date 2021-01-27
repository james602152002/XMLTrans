#! /usr/bin/env python3
import os
import xml.etree.ElementTree as ET

xmlArrs = {"Saury.xml","Saury-ja-JP.xml",
        "Saury-ko-KR.xml","Saury-zh-CN.xml",
        "Saury-zh-TW.xml"}

docDirectory = os.getenv("HOME")+"/Documents/"
print(docDirectory)

def folderNameSwitcher(arg):
    switcher={
            "Saury.xml":"values",
            "Saury-ja-JP.xml":"values-ja-rJP",
            "Saury-ko-KR.xml":"values-ko-rKR",
            "Saury-zh-CN.xml":"values-zh-rCN",
            "Saury-zh-TW.xml":"values-zh-rTW"
            }
    return switcher.get(arg,"values")

def isNoColor(key):
    switcher={
            "ConflictCounts":True,
            "RecordsCount":True,
            "DeadlineInHoursCnt":True,
            "DeadlineDate":True,
            "DeadlineInDaysCnt":True,
            "RemindAheadOfDate":True,
            "DocCounts":True,
            "MinutesAgo":True,
            "UploadedDocCnt":True,
            "ApprovedByAuditorCnt":True,
            "SealCnt":True,
            "DaysCnt":True,
            "WorkLogParticipantsHint":True,
            "ConflictRecordsCnt":True,
            "RemainingAnnualLeaveDays":True,
            "RemindBeforeMinutes":True,
            "RemindBeforeHours":True,
            "RemindBeforeDays":True,
            "RemindBeforeWeeks":True,
            "PreviewTemplate":True,
            "SelectableLogCnt":True,
            "OptionalContractInfoCnt":True,
            "OptionalFeeCnt":True,
            "SelectedCnt":True,
            "LawyerCnt":True,
            "ContactsCnt":True,
            "ScheduleTaskCnt":True,
            "ScheduleCnt":True,
            "ScheduleLogCnt":True,
            "ScheduleCourtCnt":True,
            "ScheduleMeetingCnt":True,
            "ScheduleLeaveCnt":True,
            "SecondsAgo":True,
            "YouStillHaveOtherCnt":True,
            "PasswordComplexity_MinLength_Hint":True,
            "PasswordComplexity_MaxLength_Hint":True
        }
    return  switcher.get(key, False)

def initValueByKey(key, value):
    filterValue = value.replace("&","&amp;").replace("'","\\'")
    #忘记密码？ {0}.
    if key == "PasswordChangeDontRememberMessage":
        filterValue = filterValue.replace("{0}.","").replace(" ","")
    if "{0}" in filterValue:
        if isNoColor(key):
            filterValue = filterValue.replace("{0}","%s")
        else:
            index = filterValue.index("{0}")
            strLen = len("{0}")
            length = len(filterValue)
            lastStr = filterValue[index + strLen: length]
            filterValue = "<Data><![CDATA[" + filterValue[0:index]
            filterValue += "<font color=\"#5D73FA\">%s</font>"
            filterValue += lastStr
            filterValue += "]]></Data>"
    return filterValue

def parseXML(fileName):
    content = ""
    tree = ET.parse(docDirectory+"localization/"+fileName)
    root = tree.getroot()
    for text in root.findall('./texts/text'):
        key = text.get('name')
        value = text.get('value')
        if value and not "<br>" in value and key and key != "new" :
            key  = key.replace("(","").replace(")","").replace(".","_").replace(",","").replace(" ","")
            value = initValueByKey(key,value) 
            content += "    <string name=\"" + key + "\">"
            content += value
            content += "</string>\n"
    return content

def writeFile(fileName,folderName):
    #文件路径
    destFilePath = docDirectory+folderName
    #创建文件夹
    if not os.path.exists(destFilePath):
        os.makedirs(destFilePath)
    #编写xml内容
    xmlBuilder = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
    xmlBuilder += "<resources xmlns:tools=\"http://schemas.android.com/tools\" tools:ignore=\"MissingTranslation\">\n\n"
    xmlBuilder += parseXML(fileName)
    xmlBuilder += "\n</resources>"
    textFile = open(destFilePath+"/strings.xml","w")
    textFile.write(xmlBuilder)
    textFile.close()
    return

for name in xmlArrs:
    writeFile(name,folderNameSwitcher(name))
