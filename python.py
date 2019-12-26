import sys
import os
from PyQt5.QtWidgets import *

from Board import *

import logging
import threading
import time
import datetime

from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
import gedcom.tags

def Get_Element_UID(element):
    uidValue = ""
    for child in element.get_child_elements():
        if child.get_tag() == "_UID":
            uidValue = child.get_value()
    return uidValue

def Get_Element_Note(element):
    noteValue = ""
    for child in element.get_child_elements():
        if child.get_tag() == "NOTE":
            noteValue = child.get_value()
    
    if noteValue.find("findagrave") == -1 :
        return ""
    return noteValue

def Get_Element_FullName(element):
    (first, last) = element.get_name()

    fxname = ""

    for child in element.get_child_elements():
        if child.get_tag() == gedcom.tags.GEDCOM_TAG_NAME:
            # place the name in the value of the NAME tag.
            found_fx_name = False
            for childOfChild in child.get_child_elements():
                if childOfChild.get_tag() == "NSFX":
                    fxname = childOfChild.get_value()
                    found_fx_name = True

            if found_fx_name:
                return first + " " + last + " " + fxname

    return first + " " + last

def Get_Element_LastName(element):
    (first, last) = element.get_name()
    return last

def Get_Element_Gender(element):
    return element.get_gender()

def Get_Element_HTML(directoryPath, element):
    filePath = directoryPath + "\\" + str(Get_Element_UID(element)) + ".htm"
    return filePath

def Get_Element_CSS(directoryPath):
    filePath = directoryPath + "\\" + "app.css"
    return filePath

def Get_Element_Href(element):
    return str(Get_Element_UID(element)) + ".htm"

def Get_Element_DeathDate(element):
    (DeathDay, DeathPlace, DeathSources) = element.get_death_data()
    return DeathDay

def Get_Element_DeathPlace(element):
    (DeathDay, DeathPlace, DeathSources) = element.get_death_data()
    return DeathPlace

def Get_Element_DeathSources(element):
    (DeathDay, DeathPlace, DeathSources) = element.get_death_data()
    return DeathSources

def Get_Element_BurialDate(element):
    (BurialDate, BurialPlace, BurialSources) = element.get_burial_data()
    return BurialDate

def Get_Element_BurialPlace(element):
    (BurialDate, BurialPlace, BurialSources) = element.get_burial_data()
    return BurialPlace

def Get_Element_BurialSources(element):
    (BurialDate, BurialPlace, BurialSources) = element.get_burial_data()
    return BurialSources

def Get_Element_Birthday(element):   
    birthdataSources = list()
    (birthdayValue, birthplaceValue, birthdataSources) = element.get_birth_data()
    return birthdayValue

def Get_Element_Birthplace(element):   
    birthdataSources = list()
    (birthdayValue, birthplaceValue, birthdataSources) = element.get_birth_data()
    return birthplaceValue

def Publish_Html5(parser, element, id, directoryPath, bShowGoogleCode, sCSScode):

    noteValue = Get_Element_Note(element)
    uidValue = Get_Element_UID(element)

    filePath = Get_Element_HTML(directoryPath, element)
    logging.info("PublishHtml: %s", filePath)

    cssPath = Get_Element_CSS(directoryPath)

    fullname = Get_Element_FullName(element)
    lastname = Get_Element_LastName(element)

    gender = Get_Element_Gender(element)

    parentsList = parser.get_parents(element)
    
    fatherElement = 0
    motherElement = 0

    if len(parentsList) == 2:
        fatherElement = parentsList[0]
        motherElement = parentsList[1]

    fathername = "unknown"
    mothername = "unknown"
    fatherhtml = ""
    motherhtml = ""

    if fatherElement != 0 and motherElement != 0:
        fathername = Get_Element_FullName(fatherElement)
        mothername = Get_Element_FullName(motherElement)
        fatherhtml = Get_Element_Href(fatherElement)
        motherhtml = Get_Element_Href(motherElement)


    birthdayValue = Get_Element_Birthday(element)
    birthplaceValue = Get_Element_Birthplace(element)

    currentTime = datetime.datetime.now()

    titleValue = fullname + " " + str(element.get_birth_year()) + " genealogy " + str(currentTime.year) + "-" + str(currentTime.month) + "-" + str(currentTime.day)
    nameValue = fullname + " Family " + str(element.get_birth_year())

    deathDate = Get_Element_DeathDate(element)
    deathPlace = Get_Element_DeathPlace(element)

    burialDate = Get_Element_BurialDate(element)
    burialPlace = Get_Element_BurialPlace(element)

    marriagetuple = parser.get_marriages(element)
    familyList = parser.get_families(element)

    metaDescription = "<META name='description' content='" + fullname + " family history.  Genealogy of the " + lastname + " family.'>"

    fp = open(filePath, "w", encoding = "utf-8")
    fp.write(u"""
        <!DOCTYPE html>    
        <html lang="en">
        <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>
    """)
    fp.write(titleValue)
    fp.write(u"""
        </title>
        <META http-equiv='content-type' content='text/html; charset=iso-8859-1'>
    """)
    fp.write(metaDescription)

    fp.write(u"""
        <link rel="stylesheet" type="text/css" href="app.css">
    """)

    if bShowGoogleCode == True:
        fp.write(u"""
        <script type="text/javascript">

        var _gaq = _gaq || [];
        _gaq.push(['_setAccount', 'UA-30751917-1']);

        _gaq.push(['_trackPageview']);

        (function() {
            var ga = document.createElement('script');
        ga.type = 'text/javascript'; ga.async = true;
            ga.src = ('https:' == document.location.protocol
        ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
            var s = document.getElementsByTagName
        ('script')[0]; s.parentNode.insertBefore(ga, s);
        })();

        </script>
        """ )

    fp.write(u"""
        </head>
        <body>
        <div id="wrap">
        <header>
        """)
    fp.write(u"<center><h1><font color = blue>" + nameValue + "</font></center></h1>")
    fp.write(u"""
        </header>
        <section>
        <br>
    """)

    fp.write(u"""
    <div id = 'advertiser_intro_part'>
    <center>
    <center>Our advertisers help pay the expenses of this site.  Please patronize them.</center>
    </div>
    """)
    fp.write(u"<br>")

    if bShowGoogleCode == True:
        fp.write(u"""
        <div id = 'GoogleCode_part'>
        <center><script type="text/javascript"><!--
        google_ad_client = "ca-pub-6129979233663841";
        /* genealogy leader */
        google_ad_slot = "5342539673";
        google_ad_width = 728;	
        google_ad_height = 90;
        //-->
        </script>
        <script type="text/javascript"
        src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
        </script>
        </center><p>
        </div>
        """)
    
    fp.write(u"<div id = 'Info_Part'><center><font size = 4>" + fullname + " was born " + birthdayValue + " in " + birthplaceValue + ".<br></div>")
    fp.write(u"<br>")

#######################################################
#   Parents Part
#######################################################

    if fathername == "unknown" or mothername == "unknown":
        if gender == "M":
            fp.write(u"<div id = 'Parents_Part'><center>His parents are unknown </center>")
        else:
            fp.write(u"<div id = 'Parents_Part'><center>Her parents are unknown </center>")
    else:
        if gender == "M":
            fp.write(u"<div id = 'Parents_Part'><center>He is the son of ")
        else:
            fp.write(u"<div id = 'Parents_Part'><center>She is the daughter of ")
        fp.write(u"<a href = '" + fatherhtml + "'>" + fathername + "</a> and <a href = '" + motherhtml + "'>" + mothername + ".</a></center></div>")
    fp.write(u"<br>")
#######################################################
#   Dead Part
#######################################################    

    DeadSentence = ""
    if deathDate == "":
        if gender == "M":           
            DeadSentence = "His death is unknown"
        else:
            DeadSentence = "Her death is unknown"
    else:
        if gender == "M":
            DeadSentence = "He died in " + deathDate + " in " + deathPlace
        else:
            DeadSentence = "She died in " + deathDate + " in " + deathPlace
        
        if noteValue != "":
            if burialPlace != "":
                DeadSentence = DeadSentence + " and is <a href = '" + noteValue + "' target = 'parent'>buried</a>"                
                DeadSentence = DeadSentence +  " in the " + burialPlace
            else:
                DeadSentence = DeadSentence + " and is buried<a href = '" + noteValue + "' target = 'parent'> here</a>"
        else:
            if burialPlace != "":
                DeadSentence = DeadSentence + " and is buried"
                DeadSentence = DeadSentence + " in the " + burialPlace
            else:
                DeadSentence = DeadSentence + " and buried is unknown"

    fp.write(u"<div id = 'dead_part'><center>" + DeadSentence + ".</center></div>")
    fp.write(u"<br>")
#######################################################
#   Marriage & Child Part
#######################################################

    fp.write(u"<div id = 'family_part'>")
    bMarriageFlag = False
    for family in familyList:
        date = ''
        place = ''
        husbandElement = 0
        wifeElement = 0
        
        element_dictionary = parser.get_element_dictionary()

        children = []
        
        for family_data in family.get_child_elements():

            if family_data.get_tag() == gedcom.tags.GEDCOM_TAG_HUSBAND:
                husbandElement = element_dictionary[family_data.get_value()]
            if family_data.get_tag() == gedcom.tags.GEDCOM_TAG_WIFE:
                wifeElement = element_dictionary[family_data.get_value()]

            if family_data.get_tag() == gedcom.tags.GEDCOM_TAG_CHILD:
                if family_data.get_value() in element_dictionary:
                    children.append(element_dictionary[family_data.get_value()])

            if family_data.get_tag() == gedcom.tags.GEDCOM_TAG_MARRIAGE:
                for marriage_data in family_data.get_child_elements():
                    if marriage_data.get_tag() == gedcom.tags.GEDCOM_TAG_DATE:
                        date = marriage_data.get_value()
                    if marriage_data.get_tag() == gedcom.tags.GEDCOM_TAG_PLACE:
                        place = marriage_data.get_value()

        if husbandElement == 0 or wifeElement == 0:
            continue
        
        bMarriageFlag = True

        marriageSentence = ""

        if gender == "M":
            marriageSentence = "He married <a href = '" + Get_Element_Href(wifeElement) + "'>" + Get_Element_FullName(wifeElement) + "</a>"
            if date != '':
                marriageSentence = marriageSentence + " on " + date
            if place != '':
                marriageSentence = marriageSentence + " in " + place
            if date == '' and place != '':
                marriageSentence = marriageSentence + " (date is unknown)."
            if place == '' and date != '':
                marriageSentence = marriageSentence + " (place is unknown)."
            if place == '' and date == '':
                marriageSentence = marriageSentence + " (date and place are unknown)."
        else:
            marriageSentence = "She married <a href = '" + Get_Element_Href(husbandElement) + "'>" + Get_Element_FullName(husbandElement) + "</a>"
            if date != '':
                marriageSentence = marriageSentence + " on " + date
            if place != '':
                marriageSentence = marriageSentence + " in " + place
            if date == '' and place != '':
                marriageSentence = marriageSentence + " (date is unknown)."
            if place == '' and date != '':
                marriageSentence = marriageSentence + " (place is unknown)."
            if place == '' and date == '':
                marriageSentence = marriageSentence + " (unknown)."

        fp.write(u"<div id = 'marriage_part'>")
        fp.write(u"<center>" + marriageSentence + "</center>")
        fp.write(u"</div>")
        fp.write(u"<br>")
        
        fp.write(u"<div id = 'children_part'>")
        childsSentence = ""

        if len(children) == 0:
            childsSentence = "<center>No Children between " + Get_Element_FullName(husbandElement) + " and " + Get_Element_FullName(wifeElement) + "</center>"
        else:
            childsSentence = "<center>Children of " + Get_Element_FullName(husbandElement) + " and " + Get_Element_FullName(wifeElement) + " are:</center>"
            childsSentence += "<center><table id = 'child_table'><tr><td>"
            for child in children:
                childsSentence += "<li>"
                child_birthday = Get_Element_Birthday(child)
                if child_birthday == "":
                    child_birthday = " - no date of birth or death"                
                if Get_Element_Gender(child) == "M":                   
                    childsSentence += "A son, <a href = '" + Get_Element_Href(child) + "'>" + Get_Element_FullName(child) + "</a> was born " + child_birthday + "."
                else:
                    childsSentence += "A daughter, <a href = '" + Get_Element_Href(child) + "'>" + Get_Element_FullName(child) + "</a> was born " + child_birthday + "."
            childsSentence += "</td></tr></table></center>"

        fp.write(u"<center>" + childsSentence + "</center>")
        fp.write(u"</div><br>")

    if bMarriageFlag == False:
        fp.write(u"<div id = 'marriage_part'><center> No Marriage </center></div>")
    
    fp.write(u"<div id = 'Previous_part'><center><a href='home.htm'> Home, </a> <a href='index.htm'> Prologue, </a> <a href='credits.htm'> Credits </a></center></div>")
    fp.write(u"<div id = 'Digree_part'><center>Back to <a href='" + lastname + "pedigree.htm'>" + lastname + " Pedigree</a></center><p></div>")
    fp.write(u"</div>")

    if ( bShowGoogleCode == True ):
        fp.write(
            """
            <center>Search this web site for more information.</center>
            <center>
            <style type="text/css">
            @import url(http://www.google.com/cse/api/branding.css);
            </style>
            <div class="cse-branding-side" 
            style="background-color:#FFFFFF;color:#000000">
            <div class="cse-branding-form">
                <form action="http://www.google.com" 
            id="cse-search-box" target="_blank">
                <div>
                    <input type="hidden" name="cx" value="partner-pub-6129979233663841:6165808411" />
                    <input type="hidden" name="ie" value="UTF-8" />
                    <input type="text" name="q" size="80" />
                    <input type="submit" name="sa" value="Search" />
                </div>
                </form>
            </div>
            <div class="cse-branding-logo">
                <img src="http://www.google.com/images/poweredby_transparent/poweredby_FFFFFF.gif" alt="Google" />
            </div>
            <div class="cse-branding-text">
                Custom Search
            </div>
            </div>
            """
        )
    fp.write(
        """
        </section>
        """)
    fp.write(u"<footer> <center>&copy;Copyright 2012-2019 ellisgenealogy.com</center> </footer>")
    fp.write(u"""
        </div>
        </body>
        </html>
        """
    )
    fp.close()
    return filePath

def Publish_IndexHtml(directoryPath, sCSScode, individualCount, nameList, UrlList, UIDList):

    filePath = directoryPath + "\\list.htm"
    logging.info("Publish_IndexHtml: %s", filePath)

    currentTime = datetime.datetime.now()

    titleValue = "List of Individuals : " + str(currentTime.day)
    metaDescription = "<META name='description' content='List of Individuals'>"

    fp = open(filePath, "w", encoding = "utf-8")
    fp.write(u"""
        <!DOCTYPE html>    
        <html lang="en">
        <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>
    """)
    fp.write(titleValue)
    fp.write(u"""
        </title>
        <META http-equiv='content-type' content='text/html; charset=iso-8859-1'>
    """)
    fp.write(metaDescription)

    fp.write("""
    <link rel="stylesheet" type="text/css" href="app.css">
    """)

    fp.write(u"""
        </head>
        <body>
        <div id="wrap">
        <header>
        """)
    fp.write(u"<center><h1><font color = blue>" + titleValue + "</font></center></h1>")
    fp.write(u"""
        </header>
        <section>
        <br>
    """)

    fp.write(u"""
    <div id = 'Individuals_Count_Part'>
    """)
    fp.write(u"<center><font size = 3>" + str(individualCount) + " individuals</font></center>")
    fp.write(u"</div><br>")
    
    fp.write(u"<div id = 'Individual_List_Part'><table id = 'Individual_List_Table'><tr><th>No</th><th>Full Name</th><th>UID</th><th>link</th></tr>")

    i = 0
    for i in range(individualCount):
        fp.write(u"<tr><td>" + str(i) + "</td><td>" + nameList[i] + "</td><td>" + UIDList[i] + "</td><td><a href = '" + UrlList[i] + "'>" + UrlList[i] + "</a></td><td><tr>")

    fp.write(u"</table></div>")
    fp.write(
        """
        </section>
        """)
    fp.write(u"<footer> <center>&copy;Copyright 2012-2019 ellisgenealogy.com</center> </footer>")
    fp.write(u"""
        </div>
        </body>
        </html>
        """
    )
    fp.close()
    return filePath
def Publish_CSS(directoryPath, sCSScode):

    cssPath = Get_Element_CSS(directoryPath)
    fp = open(cssPath, "w", encoding="utf-8")
    fp.write(sCSScode)
    fp.close()

def thread_function(self):

    logging.info("Thread %s: starting flag = %d", self.m_filePath, self.thread_flag)

    # Path to your `.ged` file
    file_path = self.m_filePath

    # Initialize the parser
    gedcom_parser = Parser()

    # Parse your file
    gedcom_parser.parse_file(file_path)
    elements_list = gedcom_parser.get_element_list()
    element_count = 0

    nameList = []
    urlList = []
    UIDList = []

    # Iterate through all root child elements
    Publish_CSS(self.m_dirPath, self.m_CSSCode)

    for element in elements_list:

        if self.thread_flag == 0:
            break
        # Is the `element` an actual `IndividualElement`? (Allows usage of extra functions such as `surname_match` and `get_name`.)
        if isinstance(element, IndividualElement):          

            # Unpack the name tuple
            (first, last) = element.get_name()

            # Print the first and last name of the found individual
            logging.info("Thread %d %s %s: %s %s", element_count + 1, first, last, element.get_gender(), Get_Element_Note(element))
            try:
                url = Publish_Html5(gedcom_parser, element, element_count, self.m_dirPath, self.m_bShowGoogleCode, self.m_CSSCode)
            except:
                logging.info("Thread Error %d %s %s: %s", element_count + 1, first, last, element.get_gender(), Get_Element_UID(element))
                continue
            nameList.append(Get_Element_FullName(element))
            urlList.append(url)
            UIDList.append(Get_Element_UID(element))
            item = QListWidgetItem(url)
            self.ui.listWidget.addItem(item)
            self.ui.StatusLabel.setText(str(element_count + 1) + " Individuals")
            element_count = element_count + 1

    indexUrl = Publish_IndexHtml(self.m_dirPath, self.m_CSSCode, element_count, nameList, urlList, UIDList)

    item = QListWidgetItem(indexUrl)
    self.ui.listWidget.addItem(item)

    logging.info("Thread Element Count: %d", element_count)
    logging.info("Thread %s: finished", self.m_filePath)  

class MyBoard(QDialog):

    m_flag = 0
    m_dirPath = ""
    m_filePath = ""
    m_thread = ""
    thread_flag = 0
    m_bShowGoogleCode = False
    m_CSSCode = str("""
        body {
        color: #222;
        background: #fafafa;
        font: 13px/1.4 'segoe ui', sans-serif;
        }

        h1,
        h2 {
        margin: 0 0 .25em;
        font: 700 2.4em/1 'myriad pro', sans-serif;
        }

        h2 {
        color: #999;
        margin: 0 0 1em;
        font-size: 1.6em;
        }

        a {
        color: #06c;
        transition: .2s linear;
        -webkit-transition: .2s linear;
        }

        a:hover {
        color: #39f;
        }

        p {
        margin: 1em 0;
        }

        footer {
        color: #999;
        margin: 3em 0 0;
        text-align: center;
        }

        footer a {
        color: #777;
        }

        #wrap {
        width: 75%;
        margin: 1em auto;
        padding: 1.5em;
        background: #fff;
        box-shadow: 0 1em 2em rgba(0, 0, 0, .2);
        }
        #advertiser_intro_part {

        }

        #GoogleCode_part {

        }

        #Info_Part {

        }

        #Parents_Part {

        }

        #dead_part {

        }

        #family_part {

        }

        #marriage_part {
            
        }

        #Individuals_Count_Part {

        }
        #individual_List_Part {

        }
        #individual_List_Table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }
        #individual_List_Table td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        }
        #individual_List_Table tr:nth-child(even) {
        background-color: #dddddd;
        }
    """)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.OpenButton.clicked.connect(self.OpenDialog)
        self.ui.StartButton.clicked.connect(self.StartAction)
        self.ui.StopButton.clicked.connect(self.StopAction)
        self.ui.OutputButton.clicked.connect(self.OutputConfig)
        self.ui.bGoogleCode.clicked.connect(self.ShowGoogleCode)
        self.show()

    def init_variables(self):
        self.m_filePath = ""
        self.m_dirPath = ""
        self.m_flag = 0
        self.m_bShowGooleCode = False
        self.m_CSSCode = str("""
            <style id = "compiled css" type = "text/css">
        body {
        color: #222;
        background: #fafafa;
        font: 13px/1.4 'segoe ui', sans-serif;
        }

        h1,
        h2 {
        margin: 0 0 .25em;
        font: 700 2.4em/1 'myriad pro', sans-serif;
        }

        h2 {
        color: #999;
        margin: 0 0 1em;
        font-size: 1.6em;
        }

        a {
        color: #06c;
        transition: .2s linear;
        -webkit-transition: .2s linear;
        }

        a:hover {
        color: #39f;
        }

        p {
        margin: 1em 0;
        }

        footer {
        color: #999;
        margin: 3em 0 0;
        text-align: center;
        }

        footer a {
        color: #777;
        }

        #wrap {
        width: 75%;
        margin: 1em auto;
        padding: 1.5em;
        background: #fff;
        box-shadow: 0 1em 2em rgba(0, 0, 0, .2);
        }
        #advertiser_intro_part {

        }

        #GoogleCode_part {

        }

        #Info_Part {

        }

        #Parents_Part {

        }

        #dead_part {

        }

        #family_part {

        }

        #marriage_part {
            
        }
    </style>
    """)

    def ShowGoogleCode(self):
        self.m_bShowGoogleCode = not self.m_bShowGoogleCode

    def OpenDialog(self):
        opt_str = QFileDialog.Options()
        self.m_filePath, _= QFileDialog.getOpenFileName(self, "Select a GEDCOM file", "", "GEDCOM files (*.ged);;All files (*);")
        self.m_dirPath = os.path.dirname(os.path.realpath(self.m_filePath))

        if self.m_filePath:
            logging.info("MainBoard : filePath %s", self.m_filePath)
            self.setWindowTitle(self.m_filePath)
            self.ui.FilePath.setText(self.m_filePath)
            self.ui.OutputFolderLabel.setText(self.m_dirPath)
            self.ui.CSS_text.setPlainText(self.m_CSSCode)
            self.m_flag = 1

    def OutputConfig(self):
        ResPath = QFileDialog.getExistingDirectory(self, "Select Directory")
        
        if ResPath:
            self.m_dirPath = ResPath
            self.ui.OutputFolderLabel.setText(self.m_dirPath)

    def StartAction(self):
        if self.m_flag != 1:
            logging.info("MainBoard : Not File Yet. Please Load File")
            self.ui.FilePath.setText("Please Load File")
            return
        
        logging.info("MainBoard : Start Parsing %s", self.m_filePath)
        self.m_flag = 2
        self.m_CSSCode = self.ui.CSS_text.toPlainText()
        self.m_thread = threading.Thread(target=thread_function, args=(self,))
        logging.info("MainBoard : Thread Running")
        self.thread_flag = 1
        self.m_thread.start()

    def StopAction(self):       
        if self.m_flag != 2:
            logging.info("MainBoard : Not File or Not Running")
            self.ui.FilePath.setText("No File or Not running")
            return
        logging.info("MainBoard : Stop Parsing %s", self.m_filePath)
        self.m_flag = 1
        self.thread_flag = 0
        logging.info("MainBoard : Thread Stop")

if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logTime = datetime.datetime.now()

    logfile = "log_" + str(logTime.year) + "_" + str(logTime.month) + "_" + str(logTime.day) + "_" + str(logTime.hour) + "_" + str(logTime.minute) + "_" + str(logTime.second) + ".log"

    logging.basicConfig( filename=logfile, filemode="wt", format=format, level=logging.INFO, datefmt="%H:%M:%S")
    app = QApplication(sys.argv)
    Board = MyBoard()
    Board.show()
    sys.exit(app.exec())
