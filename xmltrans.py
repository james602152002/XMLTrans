#! /usr/bin/env python3
import os
import re
import xml.etree.ElementTree as ET

xmlArrs = {"Saury.xml",
           "Saury(en).xml",
           "Saury-ja-JP.xml",
           "Saury-ko-KR.xml",
           "Saury(zh)-zh-CN.xml",
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

def folderNameSwitcher(arg):
    switcher={
            "Saury.xml":"values",
            "Saury(en).xml":"values-en",
            "Saury-ja-JP.xml":"values-ja-rJP",
            "Saury-ko-KR.xml":"values-ko-rKR",
            "Saury(zh)-zh-CN.xml":"values-zh",
            "Saury-zh-CN.xml":"values-zh-rCN",
            "Saury-zh-Hant.xml":"values-zh-rTW",
            "Saury-ar.xml":"values-ar",
            "Saury-de.xml":"values-de",
            "Saury-es.xml":"values-es",
            "Saury-fr.xml":"values-fr",
            "Saury-hi.xml":"values-hi",
            "Saury-ru.xml":"values-ru"
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
            "PasswordComplexity_MaxLength_Hint":True,
            "AccountBankCnt":True,
            "ConflictDetactResults":True,
            "PlzSelect":True,
            "MinValueBusinessCard":True,
            "ValidateMinValue":True,
            "HintTableTotalCount":True,
            "CompareMustGreaterThan":True,
            "CompareMustLowerEqual":True,
            "PlzInputMultipleNumOfValue":True,
            "HintTotalFixedAmountOfCaseExpenses":True,
            "HintTotalAllocRatioOfCase":True,
            "AMustBeB":True,
            "TotalArchivingFeeIsCappedHint":True,
            "AMustEqualB":True,
            "UploadArgs":True,
        }
    return  switcher.get(key, False)

def isPass(key):
    switcher={
        "Pages_Executive_AssetsManagement":False,
        "new":False,
        "UserCannotBeDeleted":False,
        "ChatUserSearch_Hint":False
    }
    return switcher.get(key, True)

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
        value = value.replace("<","&lt;").replace(">","&gt;")
        value = value.replace("\\'","")
        if value and not "<br>" in value and key and isPass(key):
            key  = key.replace("_","ASCIIUNDERLINE").replace("appASCIIUNDERLINEname","app_name").replace("toastASCIIUNDERLINEinternetASCIIUNDERLINErequestASCIIUNDERLINEtimeASCIIUNDERLINEout","toast_internet_request_time_out").replace(".","_").replace('-','_').replace(",","").replace(" ","ASCIISPACE").replace("{0}","").replace("/","").replace("!","").replace(":","ASCIICOLON").replace("'","").replace("&","ASCIIAND").replace("%","ASCIIPERCENT").replace("(","ASCIILBRACE").replace(")","ASCIIRBRACE")
            #key = key.replace("0","zero__").replace("5","five__")
            isNumber = re.match("^(\d+).*", key)
            if isNumber:
                key = "Number__" + key
            value = initValueByKey(key,value)
            content += "    <string name=\"" + key + "\">"
            content += value
            content += "</string>\n"
    return content

def writeFile(fileName,folderName):
    nameRegex = re.sub('\(.*\)',"",fileName)
    #文件路径
    destFilePath = docDirectory+folderName
    #创建文件夹
    if not os.path.exists(destFilePath):
        os.makedirs(destFilePath)
    #编写xml内容
    xmlBuilder = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
    xmlBuilder += "<resources xmlns:tools=\"http://schemas.android.com/tools\" tools:ignore=\"MissingTranslation\">\n\n"
    xmlBuilder += parseXML(nameRegex)
    xmlBuilder += "\n</resources>"
    textFile = open(destFilePath+"/strings.xml","w")
    textFile.write(xmlBuilder)
    textFile.close()
    return

for name in xmlArrs:
    writeFile(name,folderNameSwitcher(name))
