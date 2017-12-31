#!/usr/bin/python2
# -*- coding: utf-8 -*-

import wx
import wx.html
import os
import subprocess
import pygame
import parsersAndCalculators
import thread
import platform
import pickle
import webbrowser
import os.path

class wxHTML(wx.html.HtmlWindow):

    def OnLinkClicked(self, link):
        webbrowser.open(link.GetHref())


class MyFrame(wx.Frame):

    def __init__(self, *args, **kwds):
        self.font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.font.SetPointSize(14)
        self.Parser = parsersAndCalculators.Parsers()
        self.CurrentPrayerName = ''
        self.CurrentPrayerList = ''
        self.ListOfPrayerLists = self.Parser.getListOfListsNames()
        self.ListOfPrayerNames = \
            self.Parser.getListOfPrayerNames('BasicCatholicPrayers.xml')
        self.LatinOrEnglish = 'latin'
        self.HTMLContents = \
            '''

            <h2>Information about Latin Catholic Prayers</h2>

            <p>The program is easy to use.   Select the prayer group you want
            to work on.  Then select the prayer you should like to memorize.
            Clicking the quiz will result in a quiz starting.   Click the word
            you think is the best and you will score a success or a failure.  A
            score shows in the top window.  You can also view the grammar for 
            any particular word by clicking on it then clicking grammar.  If
            you want the grammar for the whole prayer select nothing then press
            grammar.  If you want to hear the prayer then click the play the
            player button. </p>
            
            '''

        kwds['style'] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.lblPrayerListSelect = wx.StaticText(self, -1,
                'Select Prayer List')
        self.cmbPrayerListSelect = wx.ComboBox(self, -1,
                choices=self.ListOfPrayerLists, style=wx.CB_DROPDOWN
                 | wx.CB_READONLY)
        self.lblPrayerToTest = wx.StaticText(self, -1, 'Prayer to Test')
        self.cmbPrayerToTest = wx.ComboBox(self, -1,
                choices=self.ListOfPrayerNames, style=wx.CB_DROPDOWN
                 | wx.CB_READONLY)
        self.lblDisplayPrayer = wx.StaticText(self, -1, 'Display Prayer'
                )
        self.txtDisplayPrayer = wx.TextCtrl(self, -1, '',
                style=wx.TE_MULTILINE)
        self.txtDisplayInfo = wx.TextCtrl(self, -1, '',
                style=wx.TE_MULTILINE)
        self.__set_buttons()
        self.__set_properties()
        self.__do_layout()
        self.__set_styles()
        self.__set_events()
       
    def __set_buttons(self):
        self.lblWordChoice = wx.StaticText(self, -1, 'Word Choice')
        self.lsbWordChoice = wx.ListBox(self, -1, choices=[])
        self.html = wxHTML(self)
        self.btnReadLatin = wx.Button(self, -1, 'Play Latin Audio File')
        self.btnShowPrayer = wx.Button(self, -1, 'Show Prayer')
        self.btnStartQuiz = wx.Button(self, -1, 'Start Quiz')
        self.btnCancelQuiz = wx.Button(self, -1, 'Cancel Quiz')
        self.btnClearScreens = wx.Button(self, -1, 'Clear Screens')
        self.btnShowGrammar = wx.Button(self, -1, 'Show Grammar')
        self.btnChangeFont = wx.Button(self, -1, 'Change Font')
        self.btnShowSource = wx.Button(self, -1, 'Show Source')
        self.btnAbout = wx.Button(self, -1, 'About')
        self.rdbMode = wx.RadioBox(
            self,
            -1,
            'Mode of Operation',
            choices=['Latin', 'English'],
            majorDimension=0.00,
            style=wx.RA_SPECIFY_ROWS,
            )

    def __set_events(self):
        self.Bind(wx.EVT_COMBOBOX, self.cmbPrayerListSelectClick,
                  self.cmbPrayerListSelect)
        self.Bind(wx.EVT_COMBOBOX, self.cmbPrayerToTestClick,
                  self.cmbPrayerToTest)
        self.Bind(wx.EVT_LISTBOX, self.lsbWordChoiceClick,
                  self.lsbWordChoice)
        self.Bind(wx.EVT_BUTTON, self.btnReadLatinClick,
                  self.btnReadLatin)
        self.Bind(wx.EVT_BUTTON, self.btnShowPrayerClick,
                  self.btnShowPrayer)
        self.Bind(wx.EVT_BUTTON, self.btnStartQuizClick,
                  self.btnStartQuiz)
        self.Bind(wx.EVT_BUTTON, self.btnCancelQuizClick,
                  self.btnCancelQuiz)
        self.Bind(wx.EVT_BUTTON, self.btnClearScreensClick,
                  self.btnClearScreens)
        self.Bind(wx.EVT_BUTTON, self.btnShowGrammarClick,
                  self.btnShowGrammar)
        self.Bind(wx.EVT_BUTTON, self.btnChangeFontClick,
                  self.btnChangeFont)
        self.Bind(wx.EVT_BUTTON, self.btnShowSourceClick,
                  self.btnShowSource)
        self.Bind(wx.EVT_BUTTON, self.btnAboutClick, self.btnAbout)
        self.Bind(wx.EVT_RADIOBOX, self.rdbModeSelect, self.rdbMode)
        self.Bind(wx.EVT_CLOSE, self.onApplicationClose)


    def __set_properties(self):

        self.SetTitle('Catholic Prayers in Latin')
        self.SetSize((1172, 893))
        self.rdbMode.SetSelection(0.00)
        self.cmbPrayerToTest.Selection = 0.00
        self.cmbPrayerListSelect.Selection = 0.00
        self.html.SetPage(self.HTMLContents)

        self.CurrentPrayerList = \
            self.Parser.getListOfListsFileNames()[self.cmbPrayerListSelect.Selection]
        self.CurrentPrayerName = \
            self.Parser.getListOfPrayerTags(self.CurrentPrayerList)[self.cmbPrayerToTest.Selection]
        
        currentDirectory = os.path.abspath(__file__)
        currentDirectory = os.path.dirname(currentDirectory)
        
        newDirectory = os.path.join(currentDirectory, 'settings.dump')

        programSettings = pickle.load(open(newDirectory))

        self.cmbPrayerListSelect.Selection = programSettings[0]
        self.cmbPrayerListSelectClick(0)
        self.cmbPrayerToTest.Selection = programSettings[1]
        self.txtDisplayPrayer.SetValue(programSettings[2])
        self.txtDisplayInfo.SetValue(programSettings[3])
        self.lsbWordChoice.Items = programSettings[4]
        self.CurrentPrayerName = \
            self.Parser.getListOfPrayerTags(self.CurrentPrayerList)[self.cmbPrayerToTest.Selection]

        self.font.SetPointSize(programSettings[7])
        self.font.SetFaceName(programSettings[8])
        self.font.SetFamily(programSettings[9])
        self.font.SetWeight(programSettings[10])
        self.font.SetStyle(programSettings[11])
        self.__set_styles()

    def __set_styles(self):

        listOfElementsToChange = [self.txtDisplayPrayer,
                                  self.txtDisplayInfo,
                                  self.lsbWordChoice]

        for element in listOfElementsToChange:
            element.SetFont(self.font)

    def __do_layout(self):

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizerDisplays = wx.BoxSizer(wx.HORIZONTAL)
        sizerMain.Add(self.lblPrayerListSelect, 0.00, wx.ALL
                       | wx.EXPAND, 5)
        sizerMain.Add(self.cmbPrayerListSelect, 0.00, wx.ALL
                       | wx.EXPAND, 5)
        sizerMain.Add(self.lblPrayerToTest, 0.00, wx.ALL | wx.EXPAND, 5)
        sizerMain.Add(self.cmbPrayerToTest, 0.00, wx.ALL | wx.EXPAND, 5)
        sizerMain.Add(self.lblDisplayPrayer, 0.00, wx.ALL | wx.EXPAND,
                      5)
        sizerDisplays.Add(self.txtDisplayPrayer, 1, wx.ALL | wx.EXPAND,
                          5)
        sizerDisplays.Add(self.txtDisplayInfo, 1, wx.ALL | wx.EXPAND, 5)
        sizerMain.Add(sizerDisplays, 1, wx.EXPAND, 5)
        sizerMain.Add(self.lblWordChoice, 0.00, wx.ALL | wx.EXPAND, 5)
        sizer_5.Add(self.lsbWordChoice, 1, wx.ALL | wx.EXPAND, 5)
        sizer_5.Add(self.html, 1, wx.ALL | wx.EXPAND, 5)
        sizer_4.Add(self.btnReadLatin, 0.00, wx.EXPAND, 0.00)
        sizer_4.Add(self.btnShowPrayer, 0.00, wx.EXPAND, 0.00)
        sizer_4.Add(self.btnStartQuiz, 0.00, wx.EXPAND, 0.00)
        sizer_4.Add(self.btnCancelQuiz, 0.00, wx.EXPAND, 0.00)
        sizer_4.Add(self.btnClearScreens, 0.00, wx.EXPAND, 0.00)
        sizer_4.Add(self.btnShowGrammar, 0.00, wx.EXPAND, 0.00)
        sizer_4.Add(self.btnChangeFont, 0.00, wx.EXPAND, 0.00)
        sizer_4.Add(self.btnShowSource, 0.00, wx.EXPAND, 0.00)
        sizer_4.Add(self.btnAbout, 0.00, wx.EXPAND, 0.00)
        sizer_4.Add(self.rdbMode, 0.00, wx.ALL | wx.EXPAND
                     | wx.ALIGN_CENTER_HORIZONTAL
                     | wx.ALIGN_CENTER_VERTICAL, 5)
        sizerMain.Add(sizer_5, 1, wx.EXPAND, 0.00)
        sizer_3.Add(sizer_4, 0.00, wx.EXPAND, 0.00)
        sizerMain.Add(sizer_3, 0.00, wx.EXPAND, 0.00)

        self.SetSizer(sizerMain)
        self.Layout()
        self.Centre()

    def cmbPrayerListSelectClick(self, event):  # wxGlade: MyFrame.<event_handler>
        self.cmbPrayerToTest.Clear()
        fileNameList = self.Parser.getListOfListsFileNames()
        self.ListOfPrayerNames = \
            self.Parser.getListOfPrayerNames(fileNameList[self.cmbPrayerListSelect.Selection])
        self.CurrentPrayerList = \
            fileNameList[self.cmbPrayerListSelect.Selection]
        reversedList = self.ListOfPrayerNames[:]
        reversedList.reverse()
        for item in reversedList:
            self.cmbPrayerToTest.Insert(item, 0)
        self.cmbPrayerToTest.SetSelection(0)
        if event != 0:
            event.Skip()

    def cmbPrayerToTestClick(self, event):  # wxGlade: MyFrame.<event_handler>

        self.CurrentPrayerName = \
            self.Parser.getListOfPrayerTags(self.CurrentPrayerList)[self.cmbPrayerToTest.Selection]
        event.Skip()

    def lsbWordChoiceClick(self, event):  # wxGlade: MyFrame.<event_handler>

        currentCleanedPrayer = \
            self.Parser.scrubListOfPunctuation(self.txtDisplayPrayer.GetValue().split(' '
                ))
        fullDirtyPrayer = []
        listOfWords = []
        if self.LatinOrEnglish == 'latin':
            fullDirtyPrayer = \
                self.Parser.getWholeLatinPrayer(self.CurrentPrayerList,
                    self.CurrentPrayerName).split(' ')
        if self.LatinOrEnglish == 'english':
            fullDirtyPrayer = \
                self.Parser.getWholeEnglishPrayer(self.CurrentPrayerList,
                    self.CurrentPrayerName).split(' ')
        fullCleanedPrayer = \
            self.Parser.scrubListOfPunctuation(fullDirtyPrayer)
        lastChoice = len(currentCleanedPrayer)
        currentChoice = \
            self.lsbWordChoice.GetString(self.lsbWordChoice.Selection)

        if currentChoice.strip()\
             == fullCleanedPrayer[lastChoice].strip():
            self.txtDisplayInfo.AppendText('\n' + currentChoice + ' is correct!!')
            self.txtDisplayPrayer.AppendText(fullDirtyPrayer[lastChoice] + ' ')
            self.txtDisplayPrayer.PageUp()
            numberOfLines = self.txtDisplayPrayer.SetInsertionPointEnd
            selectionNumber = self.cmbPrayerToTest.Selection
            listOfPrayerTags = \
                self.Parser.getListOfPrayerTags(self.CurrentPrayerList)
            chosenPrayerList = \
                self.Parser.getListOfListsFileNames()[self.cmbPrayerListSelect.Selection]
            if self.LatinOrEnglish == 'latin':
                listOfWords = \
                    self.Parser.getLatinWords(listOfPrayerTags[selectionNumber],
                        chosenPrayerList)
            if self.LatinOrEnglish == 'english':
                listOfWords = \
                    self.Parser.getEnglishWords(listOfPrayerTags[selectionNumber],
                        chosenPrayerList)
            wordsSoFar = self.txtDisplayPrayer.GetValue().split(' ')
            self.lsbWordChoice.Clear()

            try:
                randomizedPrayerList = \
                    self.Parser.getSelectionChoicesForQuiz(listOfWords,
                        wordsSoFar)
                self.lsbWordChoice.InsertItems(randomizedPrayerList,
                        0)
            except:
                self.txtDisplayInfo.SetValue(self.txtDisplayInfo.GetValue()
                         + '\nQuiz Complete!!')
                totalListOfResults = \
                    self.txtDisplayInfo.GetValue().split('\n')
                totalResults = 0.00
                totalCorrect = 0.00
                percentageCorrect = 0.00
                for eachResult in totalListOfResults:
                    totalResults += 1
                    if eachResult.find('is correct') != -1:
                        totalCorrect += 1
                totalResults -= 3
                percentageCorrect = (totalCorrect / totalResults) * 100
                reportedValue = str(percentageCorrect) + '%'
                self.txtDisplayInfo.AppendText('\n' + reportedValue + ' Correct')
        else:

            if currentChoice != '':
                self.txtDisplayInfo.AppendText( '\n' + currentChoice + ' is incorrect!!')

    def rdbModeSelect(self, event):  # wxGlade: MyFrame.<event_handler>
        if self.rdbMode.GetSelection() == 1:
            self.LatinOrEnglish = 'english'
        if self.rdbMode.GetSelection() == 0:
            self.LatinOrEnglish = 'latin'
        event.Skip()

    def btnReadLatinClick(self, event):  # wxGlade: MyFrame.<event_handler>

        currentDirectory = self.getCurrentFileLocation()

        currentDirectory = os.path.join(currentDirectory, 'SoundFiles')
        selectionNumber = self.cmbPrayerToTest.Selection
        listOfPrayerTags = \
            self.Parser.getListOfPrayerTags(self.CurrentPrayerList)
        fileName = os.path.join(currentDirectory,
                                listOfPrayerTags[selectionNumber]
                                 + '.ogg')
        try:

            thread.start_new_thread(self.playTheSoundFile, (fileName,
                                    1))
        except:
            wx.MessageBox(fileName + ' was not found', 'info')
            print errorcode
        event.Skip()

    def btnStartQuizClick(self, event):  # wxGlade: MyFrame.<event_handler>
        self.CurrentPrayerName = \
            self.Parser.getListOfPrayerTags(self.CurrentPrayerList)[self.cmbPrayerToTest.Selection]
        self.lsbWordChoice.Clear()
        self.txtDisplayInfo.Clear()
        self.txtDisplayPrayer.Clear()
        self.txtDisplayInfo.SetValue(self.CurrentPrayerName + '\n')
        selectionNumber = self.cmbPrayerToTest.Selection
        listOfPrayerTags = \
            self.Parser.getListOfPrayerTags(self.CurrentPrayerList)
        chosenPrayerList = \
            self.Parser.getListOfListsFileNames()[self.cmbPrayerListSelect.Selection]
        listOfWords = []
        if self.LatinOrEnglish == 'latin':
            listOfWords = \
                self.Parser.getLatinWords(listOfPrayerTags[selectionNumber],
                    chosenPrayerList)
        if self.LatinOrEnglish == 'english':
            listOfWords = \
                self.Parser.getEnglishWords(listOfPrayerTags[selectionNumber],
                    chosenPrayerList)
        wordsSoFar = self.txtDisplayPrayer.GetValue().split(' ')
        wordsSoFar.append(' ')

        randomizedPrayerList = \
            self.Parser.getSelectionChoicesForQuiz(listOfWords,
                wordsSoFar)
        self.lsbWordChoice.InsertItems(randomizedPrayerList, 0)

        event.Skip()

    def btnShowPrayerClick(self, event):  # wxGlade: MyFrame.<event_handler>
        listOfPrayerTags = \
            self.Parser.getListOfPrayerTags(self.CurrentPrayerList)
        chosenPrayer = listOfPrayerTags[self.cmbPrayerToTest.Selection]
        chosenPrayerList = \
            self.Parser.getListOfListsFileNames()[self.cmbPrayerListSelect.Selection]
        wholePrayer = ''
        if self.LatinOrEnglish == 'latin':
            wholePrayer = \
                self.Parser.getWholeLatinPrayer(chosenPrayerList,
                    chosenPrayer).strip('\n').strip()
        if self.LatinOrEnglish == 'english':
            wholePrayer = \
                self.Parser.getWholeEnglishPrayer(chosenPrayerList,
                    chosenPrayer).strip('\n').strip()

        self.txtDisplayPrayer.SetValue(self.txtDisplayPrayer.GetValue().strip('\n'
                ).strip() + '''

''' + wholePrayer)
        event.Skip()

    def btnCancelQuizClick(self, event):  # wxGlade: MyFrame.<event_handler>
        self.txtDisplayInfo.SetValue('')
        self.txtDisplayPrayer.SetValue('')
        self.lsbWordChoice.Clear()
        event.Skip()

    def btnClearScreensClick(self, event):  # wxGlade: MyFrame.<event_handler>
        self.txtDisplayPrayer.SetValue('')
        self.txtDisplayInfo.SetValue('')
        event.Skip()

    def btnShowGrammarClick(self, event):  # wxGlade: MyFrame.<event_handler>

        contentsOfSelection = self.txtDisplayPrayer.GetStringSelection()
        if contentsOfSelection != '':
            searchTerms = \
                self.Parser.scrubListOfPunctuation(contentsOfSelection.split(' '
                    ))
        else:
            searchTerms = \
                self.Parser.scrubListOfPunctuation(self.txtDisplayPrayer.GetValue().split(' '
                    ))
        operatingSystem = platform.system().lower()
        runCommandForGrammar = ''

        for searchTerm in searchTerms:
            if searchTerm != '':

                currentDirectory = self.getCurrentFileLocation()

                newDirectory = os.path.join(currentDirectory,
                        'LatinEngines')
                if operatingSystem.find('linux') != -1:
                    newDirectory = os.path.join(newDirectory, 'Linux')
                    runCommandForGrammar = './words'
                if operatingSystem.find('windows') != -1\
                     or operatingSystem.find('microsoft') != -1:
                    newDirectory = os.path.join(newDirectory, 'Windows')
                    runCommandForGrammar = 'words.exe'
                if operatingSystem.find('darwin') != -1:
                    newDirectory.path.join(newDirectory, 'Linux')
                    runCommandForGrammar = './words'
                os.chdir(newDirectory)

                try:
                    myOutput = subprocess.Popen([runCommandForGrammar,
                            self.Parser.unicodeToAscii(searchTerm)],
                            stdout=subprocess.PIPE).communicate()[0]
                except:
                    myOutput = 'An error has occured try again.'
                os.chdir(currentDirectory)
                self.txtDisplayInfo.SetValue((self.txtDisplayInfo.GetValue()
                         + '''

''' + myOutput).strip('\n'))

        event.Skip()

    def btnChangeFontClick(self, event):

        initialFontData = wx.FontData()
        initialFontData.SetInitialFont(self.font)

        dialog = wx.FontDialog(None, initialFontData)

        if dialog.ShowModal() == wx.ID_OK:
            data = dialog.GetFontData()
            font = data.GetChosenFont()
            self.font = font
            self.__set_styles()
            dialog.Destroy()
        event.Skip()

    def playTheSoundFile(self, fileName, *args):

        pygame.init()
        pygame.mixer.init()

        fileExists = os.path.isfile(fileName)
        if fileExists:

         pygame.mixer.music.load(fileName)
         pygame.mixer.music.play(0)

         clock = pygame.time.Clock()
         clock.tick(10)
         while pygame.mixer.music.get_busy():
             pygame.event.poll()
             clock.tick(10)
        else:
         print (fileName + " is not found")
        
        pygame.close()
        pygame.mixer.close()


    def onApplicationClose(self, event):
        cmbPrayerListSelectContents = self.cmbPrayerListSelect.Selection
        cmbPrayerToTestContents = self.cmbPrayerToTest.Selection
        txtDisplayPrayerContents = self.txtDisplayPrayer.GetValue()
        txtDisplayInfoContents = self.txtDisplayInfo.GetValue()
        lsbWordChoiceContents = self.lsbWordChoice.Items
        windowSize = frame_1.GetSize()
        windowPosition = frame_1.GetPosition()
        fontPointSize = self.font.GetPointSize()
        fontFaceName = self.font.GetFaceName()
        fontFamily = self.font.GetFamily()
        fontWeight = self.font.GetWeight()
        fontStyle = self.font.GetStyle()



        fullListOfAttributes = [
            cmbPrayerListSelectContents,
            cmbPrayerToTestContents,
            txtDisplayPrayerContents,
            txtDisplayInfoContents,
            lsbWordChoiceContents,
            windowSize,
            windowPosition,
            fontPointSize,
            fontFaceName,
            fontFamily,
            fontWeight,
            fontStyle,
            ]
        
        currentDirectory = os.path.abspath(__file__)
        currentDirectory = os.path.dirname(currentDirectory)
        newDirectory = os.path.join(currentDirectory, 'settings.dump')
        pickleFilePath = os.path.join(currentDirectory, 'settings.dump')

        print pickleFilePath + " - when written" 
        pickle.dump(fullListOfAttributes, open(pickleFilePath, 'w'))

        self.Destroy()

    def btnShowSourceClick(self, event):
        originalContent = self.html.GetOpenedPage()
        self.html.SetPage(originalContent + 'Show Source')
        event.Skip()

    def btnAboutClick(self, event):  # wxGlade: MyFrame.<event_handler>

        fileDirectory = self.getCurrentFileLocation()
        fileDirectory = os.path.join(fileDirectory, 'AboutDocs')

        descriptionFile = os.path.join(fileDirectory, 'Description')
        licenseFile = os.path.join(fileDirectory, 'license')

        descriptionFileObject = open(descriptionFile, 'r')
        licenseFileObject = open(licenseFile, 'r')
        description = descriptionFileObject.read()

        license = licenseFileObject.read()

        currentDirectory = self.getCurrentFileLocation()
        iconFilePath = os.path.join(currentDirectory,
                                    'LatinCatholicPrayers.png')

        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon(iconFilePath, wx.BITMAP_TYPE_PNG))
        info.SetName('Catholic Latin Prayers')
        info.SetVersion('1.36')
        info.SetDescription(description)
        info.SetCopyright('(C) 2016 Christopher Patrick Fair')
        #info.SetWebSite('http://latinlovingcatholic.blogspot.com/')
        info.SetLicence(license)
        info.AddDeveloper('Christopher P. Fair')

        wx.AboutBox(info)

        event.Skip()

    def getCurrentFileLocation(self):
        fileDirectory = os.path.abspath(__file__)
        fileDirectory = os.path.dirname(fileDirectory)
        if fileDirectory.find('NetBeansProjects') == False:
            if fileDirectory.find('LatinCatholicPrayers') == True:
                fileDirectory = os.path.join(fileDirectory,
                        'LatinCatholicPrayers')

        return fileDirectory


if __name__ == '__main__':
    app = wx.PySimpleApp(0.00)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, 'wxPython custom icon')
    currentIconFile = frame_1.getCurrentFileLocation()
    currentIconFile = os.path.join(currentIconFile,
                                   'LatinCatholicPrayers.png')
    frameIcon = wx.Icon(currentIconFile, wx.BITMAP_TYPE_PNG)
    frame_1.SetIcon(frameIcon)
    app.SetTopWindow(frame_1)
    currentDirectory = os.path.abspath(__file__)
    currentDirectory = os.path.dirname(currentDirectory)
    newDirectory = os.path.join(currentDirectory, 'settings.dump')
    print newDirectory + " - When read"
    try:
        programSettings = pickle.load(open(newDirectory))
        frame_1.SetSize(programSettings[5])
        frame_1.SetPosition(programSettings[6])
    except:
        print 'There is no file yet for settings.'

    frame_1.Show()
    app.MainLoop()
