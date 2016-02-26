#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'christopher'
__date__ = '$Nov 7, 2010 3:53:36 PM$'

from xml.etree import ElementTree
import os
import random
import sys


class Parsers:

    def getLatinWords(self, nameOfPrayer, nameOfPrayerList):

        wholeLatinPrayer = self.getWholeLatinPrayer(nameOfPrayerList,
                nameOfPrayer)
        splitLatinPrayer = wholeLatinPrayer.split(' ')
        cleanedSplitLatinPrayer = \
            self.scrubListOfPunctuation(splitLatinPrayer)
        return cleanedSplitLatinPrayer

    def getEnglishWords(self, nameOfPrayer, nameOfPrayerList):

        wholeEnglishPrayer = \
            self.getWholeEnglishPrayer(nameOfPrayerList, nameOfPrayer)
        splitEnglishPrayer = wholeEnglishPrayer.split(' ')
        cleanedSplitEnglishPrayer = \
            self.scrubListOfPunctuation(splitEnglishPrayer)
        return cleanedSplitEnglishPrayer

    def scrubListOfPunctuation(self, listToScrub):

        scrubbedList = []
        listOfPunctuation = [
            '.',
            ',',
            '!',
            ';',
            ':',
            '(',
            ')',
            '?',
            ' ',
            '\n',
            ]
        for word in listToScrub:

            for punctuationMark in listOfPunctuation:

                word = word.strip(punctuationMark)

            if word != '':
                scrubbedList.append(word.lower())
        return scrubbedList

    def unicodeToAscii(self, unicode):
        """This takes a UNICODE string and replaces Latin-1 characters with
            something equivalent in 7-bit ASCII. It returns a plain ASCII string.
            This function makes a best effort to convert Latin-1 characters into
            ASCII equivalents. It does not just strip out the Latin-1 characters.
            All characters in the standard 7-bit ASCII range are preserved.
            In the 8th bit range all the Latin-1 accented letters are converted
            to unaccented equivalents. Most symbol characters are converted to
            something meaningful. Anything not converted is deleted.
        """

        xlate = {
            0xc0: 'A',
            0xc1: 'A',
            0xc2: 'A',
            0xc3: 'A',
            0xc4: 'A',
            0xc5: 'A',
            0xc6: 'Ae',
            0xc7: 'C',
            0xc8: 'E',
            0xc9: 'E',
            0xca: 'E',
            0xcb: 'E',
            0xcc: 'I',
            0xcd: 'I',
            0xce: 'I',
            0xcf: 'I',
            0xd0: 'Th',
            0xd1: 'N',
            0xd2: 'O',
            0xd3: 'O',
            0xd4: 'O',
            0xd5: 'O',
            0xd6: 'O',
            0xd8: 'O',
            0xd9: 'U',
            0xda: 'U',
            0xdb: 'U',
            0xdc: 'U',
            0xdd: 'Y',
            0xde: 'th',
            0xdf: 'ss',
            0xe0: 'a',
            0xe1: 'a',
            0xe2: 'a',
            0xe3: 'a',
            0xe4: 'a',
            0xe5: 'a',
            0xe6: 'ae',
            0xe7: 'c',
            0xe8: 'e',
            0xe9: 'e',
            0xea: 'e',
            0xeb: 'e',
            0xec: 'i',
            0xed: 'i',
            0xee: 'i',
            0xef: 'i',
            0xf0: 'th',
            0xf1: 'n',
            0xf2: 'o',
            0xf3: 'o',
            0xf4: 'o',
            0xf5: 'o',
            0xf6: 'o',
            0xf8: 'o',
            0xf9: 'u',
            0xfa: 'u',
            0xfb: 'u',
            0xfc: 'u',
            0xfd: 'y',
            0xfe: 'th',
            0xff: 'y',
            0xa1: '!',
            0xa2: '{cent}',
            0xa3: '{pound}',
            0xa4: '{currency}',
            0xa5: '{yen}',
            0xa6: '|',
            0xa7: '{section}',
            0xa8: '{umlaut}',
            0xa9: '{C}',
            0xaa: '{^a}',
            0xab: '<<',
            0xac: '{not}',
            0xad: '-',
            0xae: '{R}',
            0xaf: '_',
            0xb0: '{degrees}',
            0xb1: '{+/-}',
            0xb2: '{^2}',
            0xb3: '{^3}',
            0xb4: "'",
            0xb5: '{micro}',
            0xb6: '{paragraph}',
            0xb7: '*',
            0xb8: '{cedilla}',
            0xb9: '{^1}',
            0xba: '{^o}',
            0xbb: '>>',
            0xbc: '{1/4}',
            0xbd: '{1/2}',
            0xbe: '{3/4}',
            0xbf: '?',
            0xd7: '*',
            0xf7: '/',
            }

        r = ''
        for i in unicode:
            if xlate.has_key(ord(i)):
                r += xlate[ord(i)]
            elif ord(i) >= 0x80:
                pass
            else:
                r += str(i)
        return r

    def getWholeLatinPrayer(self, nameOfPrayerList, nameOfPrayer):

        tree = \
            ElementTree.parse(self.getNameOfResource(nameOfPrayerList))
        rootelement = tree.getroot()
        latinPrayer = ''
        for subelement in rootelement:
            if subelement.tag == nameOfPrayer:
                for lowerelement in subelement:
                    if lowerelement.tag == 'LatinPrayer':
                        latinPrayer = lowerelement.text
                    if lowerelement.tag == 'LatinPrayerWithAccents':
                        latinPrayer = lowerelement.text
        return latinPrayer

    def getWholeEnglishPrayer(self, nameOfPrayerList, nameOfPrayer):

        tree = \
            ElementTree.parse(self.getNameOfResource(nameOfPrayerList))
        rootelement = tree.getroot()
        latinPrayer = ''
        for subelement in rootelement:
            if subelement.tag == nameOfPrayer:
                for lowerelement in subelement:
                    if lowerelement.tag == 'EnglishPrayer':
                        latinPrayer = lowerelement.text
                        break
        return latinPrayer

    def getListOfPrayerTags(self, nameOfPrayerList):

        tree = \
            ElementTree.parse(self.getNameOfResource(nameOfPrayerList))
        rootelement = tree.getroot()
        listOfPrayers = []
        for subelement in rootelement:
            listOfPrayers.append(subelement.tag)
        return listOfPrayers

    def getListOfPrayerNames(self, nameOfPrayerList):

        tree = \
            ElementTree.parse(self.getNameOfResource(nameOfPrayerList))
        rootelement = tree.getroot()
        listOfPrayers = []
        for subelement in rootelement:
            for lowerelement in subelement:
                if lowerelement.tag == 'EnglishPrayerName':
                    listOfPrayers.append(lowerelement.text)
        return listOfPrayers

    def getListOfListsNames(self):

        xml_file = os.path.abspath(__file__)
        xml_file = os.path.dirname(xml_file)
        if xml_file.find('library.zip') != -1:
            xml_file = os.path.split(xml_file)[0]
        xml_file = os.path.join(xml_file, 'XMLDocs')
        xml_file = os.path.join(xml_file, 'ListOfPrayerLists.xml')
        tree = ElementTree.parse(xml_file)
        rootelement = tree.getroot()
        listOfLists = []
        for subelement in rootelement:
            for lowerelement in subelement:
                if lowerelement.tag == 'PrettyFormat':
                    listOfLists.append(lowerelement.text)
        return listOfLists

    def getListOfListsFileNames(self):

        xml_file = os.path.abspath(__file__)
        xml_file = os.path.dirname(xml_file)
        if xml_file.find('library.zip') != -1:
            xml_file = os.path.split(xml_file)[0]
        xml_file = os.path.join(xml_file, 'XMLDocs')
        xml_file = os.path.join(xml_file, 'ListOfPrayerLists.xml')
        tree = ElementTree.parse(xml_file)
        rootelement = tree.getroot()
        listOfLists = []
        for subelement in rootelement:
            for lowerelement in subelement:
                if lowerelement.tag == 'ListFileName':
                    listOfLists.append(lowerelement.text)
        return listOfLists

    def getNameOfResource(self, nameOfPrayerList):

        xml_file = os.path.abspath(__file__)
        xml_file = os.path.dirname(xml_file)
        if xml_file.find('library.zip') != -1:
            xml_file = os.path.split(xml_file)[0]
        xml_file = os.path.join(xml_file, 'XMLDocs')
        xml_file = os.path.join(xml_file, nameOfPrayerList)
        return xml_file

    def getSelectionChoicesForQuiz(self, allChoices, prayerSoFar):
        """ This function obtains a 3 member randomised list and combines it
        with the next known Latin word choice.  It then returns that to the
        calling function for use in the quiz"""

        mustChoice = len(self.scrubListOfPunctuation(prayerSoFar))
        mustChoiceString = ''
        mustChoiceString = allChoices[mustChoice]

        randomSampling = random.sample(self.unique(allChoices), 3)
        while mustChoiceString in randomSampling:
            randomSampling = random.sample(self.unique(allChoices), 3)

        randomSampling.append(mustChoiceString)
        randomSamplingFinal = random.sample(randomSampling, 4)
        return randomSamplingFinal

    def unique(self, s):
        """Return a list of the elements in s, but without duplicates.

        For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
        unique(\"abcabc\") some permutation of [\"a\", \"b\", \"c\"], and
        unique(([1, 2], [2, 3], [1, 2])) some permutation of
        [[2, 3], [1, 2]].

        For best speed, all sequence elements should be hashable.  Then
        unique() will usually work in linear time.

        If not possible, the sequence elements should enjoy a total
        ordering, and if list(s).sort() doesn't raise TypeError it's
        assumed that they do enjoy a total ordering.  Then unique() will
        usually work in O(N*log2(N)) time.

        If that's not possible either, the sequence elements must support
        equality-testing.  Then unique() will usually work in quadratic
        time.
        """

        n = len(s)
        if n == 0:
            return []

        u = {}
        try:
            for x in s:
                u[x] = 1
        except TypeError:
            del u  # move on to the next method
        else:
            return u.keys()

        try:
            t = list(s)
            t.sort()
        except TypeError:
            del t  # move on to the next method
        else:
            assert n > 0
            last = t[0]
            lasti = i = 1
            while i < n:
                if t[i] != last:
                    t[lasti] = last = t[i]
                    lasti += 1
                i += 1
            return t[:lasti]

        u = []
        for x in s:
            if x not in u:
                u.append(x)
        return u


