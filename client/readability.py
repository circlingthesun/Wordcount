'''Calculate various readibility indices for a set of files.

Gunning Fog Index

    From http://en.wikipedia.org/wiki/Gunning_Fog_Index

    1. Take a full passage that is around 100 words (do not omit any
       sentences).

    2. Find the average sentence length (divide the number of words by
       the number of sentences).

    3. Count words with three or more syllables (complex words), not
       including proper nouns (for example, Djibouti), compound words,
       or common suffixes such as -es, -ed, or -ing as a syllable, or
       familiar jargon.

    4. Add the average sentence length and the percentage of complex
       words (ex., +13.37%, not simply + .1337)

    5. Multiply the result by 0.4

    The complete formula is as follows:

        ((words/sentence) + 100 * (complex words/words)) * 0.4

    The formula can be easily modified to produce a Gunning-Fog index
    result with any length sample. Simply multiply the standard result by
    100/(words in sample). The resultant formula wil be:

    ((words/sentence) + 100 * (complex words/words)) * 0.4 * 100 / (words in sample)

    While the index is a good indication of reading difficulty, it still
    has flaws. Not all multisyllabic words are difficult. For example, the
    word spontaneous is generally not considered to be a difficult word,
    even though it has four syllables.


Automated Readibility Index

    From http://en.wikipedia.org/wiki/Automated_Readability_Index

    To calculate the Automated Readability Index:

    1. Divide the number of characters by the number of words, and
       multiply by 4.71. This is #1.

    2. Divide the number of words by the number of sentences, and
       multiply by 0.5. This is #2.

    3. Add #1 and #2 together, and subtract 21.43.

    (4.71 * characters/word) + (0.5 * words/sentence) - 21.43

Coleman-Liau Index

    From http://en.wikipedia.org/wiki/Coleman-Liau_Index

    1. Divide the number of characters by the number of words, and
       multiply by 5.89. This is #1.

    2. Divide (0.3 times the number of sentences) by 100 times the
       number of words. This is #2.

    3. Subtract #2 from #1 together, and subtract 15.8

    (5.89 * characters/word) - (0.3 * sentences)/(100 * words) -15.8

Flesch-Kincaid Reading Ease

    From http://en.wikipedia.org/wiki/Flesch-Kincaid_Readability_Test


    One of the tests is known as the "Flesch-Kincaid Reading Ease"
    test. It scores passages on a scale of 0-100. Higher scores
    indicate material that is easier to read; lower numbers mark
    harder-to-read passages. The formula for the Flesch Reading Ease
    Score (FRES) test is:

    FRES = 206.835 - 1.015*ASL - 84.6*ASW

    where
        
        ASW = average number of syllables per word
            = (total syllables)/(total words)

        ASL = average sentence length
            = (total words)/(total sentences)

    As a rule of thumb, scores of 90-100 are considered easily
    understandable by an average 5th grader. 8th and 9th grade
    students could easily understand passages with a score of 60-70,
    and passage with results of 0-30 are best understood by college
    graduates. Reader's Digest magazine has a readability index of
    about 65, Time magazine scores about 52, and the Harvard Law
    Review has a general readability score in the low 30s.

    This test has become a U.S. governmental standard. Many government
    agencies require documents or forms to meet specific readability
    levels. Most states require insurance forms to score 40-50 on the
    test. The U.S. Department of Defense uses the Reading Ease test as
    the standard test of readability for its documents and forms. The
    test is so ubiquitous that it is bundled with the popular word
    processing programs KWord and Microsoft Word.

Flesch-Kincaid Grade Level
    
    From http://en.wikipedia.org/wiki/Flesch-Kincaid_Readability_Test

    An obvious use for readability tests is in the field of education.
    The "Flesch-Kincaid Grade Level Formula" translates the 0-100
    score to a U.S. grade level, making it easier for teachers,
    parents, librarians, and others to judge the readability level of
    various books and texts. The grade level is calculated with the
    following formula:

    0.39*ASL + 11.8*ASW

    where
        
        ASW = average number of syllables per word
            = (total syllables)/(total words)

        ASL = average sentence length
            = (total words)/(total sentences)

    The result is a number that corresponds with a grade level. For
    example, a score of 6.1 would indicate that the text is
    understandable by an average student in 6th grade.

SMOG Index
    
    From http://en.wikipedia.org/wiki/SMOG_Index

    McLaughlin, G. (1969), "SMOG grading: A new readability formula",
        Journal of Reading, 12 (8) 639-646

    The SMOG Index is a readability test designed to gauge the
    understandability of a text. Like the Flesch-Kincaid Grade Level,
    Gunning-Fog Index, Automated Readability Index, and Coleman-Liau
    Index, its output is an approximate representation of the U.S.
    grade level needed to comprehend the text.

    To calculate the SMOG Index:

    1. Count the number of complex words (words containing 3 or more
       syllables).

    2. Multiply the number of complex words by a factor of (30/number
       of sentences).

    3. Take the square root of the resultant number.

    4. Add 3 to the resultant number.

FORCAST Readability Formula

    From http://agcomwww.tamu.edu/market/training/power/readabil.html

    FORCAST is a new readability formula designed especially for
    technical materials. It is not meant for traditional high school
    reading matter or for newspapers or magazines or books of fiction.
    It is simpler and faster to use than other readability formulas
    and, according to its authors, is more accurate for technical
    writing. It can be used to analyze a single passage, a group of
    passages, or a random series of selections from a large body of
    technical material.

    1. Count the number of one-syllable words in a 150-word passage.

    2. Divide that number by 10.

    3. Subtract the answer from 20.

    "The FORCAST Readability Formula." Pennsylvania State University
    Nutrition Center, Bridge to Excellence Conference, 1992. 

Copyright (C) 2005 Don Peterson

This program is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free
Software Foundation, Inc., 59 Temple Place, Suite 330,
Boston, MA 02111-1307  USA
'''

from __future__ import division
from math import sqrt
import sys, re

# Load our dictionary of number of syllables if available (otherwise, 
# the number of syllables in each word will be found by the function
# guess_syllables.
try:
    import words
except:
    pass

# If true, print out more details
dbg = 0

#-------------------------------------------------------------------------
# The following function is from the pyflesch.py script written by
# Seb Bacon, March 29, 2005,  You can find it at 
# http://freshmeat.net/projects/pyflesch/.

def guess_syllables(word):
    "Guess the number of syllables in a word"
    # Our basic way of guessing is to count the number of vowels
    # in a word.  We then subtract 1 for each dipthong we find,
    # and add 1 for anti-dipthongs (OK, that's probably not the
    # technical term).
    syl = 0
    subtract_syl = ['cial', 'tia', 'cius', 'cious', 'giu', 'ion', 'iou',
                    'sia$', '.ely$', 'ea.', 'oa.', 'enced$']
    add_syl = [ 'ia', 'riet', 'dien', 'iu', 'io', 'ii', '[aeiouym]bl$',
                '[aeiou]{3}', '^mc', 'ism$', '([^aeiouy])\1l$',
                '[^l]lien', '^coa[dglx].',  '[^gq]ua[^auieo]', 'dnt$']
    word = word.lower()
    word = word.replace("'", "") # fold contractions
    word = word.replace('"', "") # remove quotes from around word
    word = re.sub("e$", "", word)
    spl = re.split("[^aeiouy]+", word)
    try:
        spl.remove("")
        spl.remove('') # why do this twice?  
    except ValueError:
        pass
    for rx in subtract_syl:
        if re.match(rx, word):
            syl -= 1
    for rx in add_syl:
        if re.match(rx, word):
            syl += 1
    if len(word) == 1: # 'x'
        syl += 1
    syl += len(spl)
    if syl == 0: 
        syl = 1
    return syl

#-------------------------------------------------------------------------

common_abbreviations = (
    "mr", "mrs", "ms", "dr", "no", "mssr", "st", "ave"
)

def GunningFogIndex(words, sentences, complex_words):
    ASL = words/sentences
    PCW = 100*complex_words/words
    return 0.4*(ASL + PCW)

def AutomatedReadibilityIndex(characters, words, sentences):
    return 4.71*characters/words + 0.5*words/sentences - 21.43

def ColemanLiauIndex(characters, words, sentences):
    return 5.89*characters/words - 0.3*sentences/(100*words) - 15.8


def FleschKincaidReadingEase(words, syllables, sentences):
    ASW = syllables/words
    ASL = words/sentences
    return 206.835 - 1.015*ASL - 84.6*ASW

def FleschKincaidGradeLevel(words, syllables, sentences):
    ASL = words/sentences
    ASW = syllables/words
    return 0.39*ASL + 11.8*ASW - 15.59

def SMOGIndex(complex_words, sentences):
    return sqrt(30*complex_words/sentences) + 3

def FORCASTReadabilityFormula(words, one_syllable_words):
    N = words/150
    return 20 - (one_syllable_words/N)/10

def EndOfSentence(word):
    '''Return 1 if the word is the end of a sentence.
    '''
    if len(word) == 0:
        raise "Empty word"
    last_char = word[-1]
    end_of_sentence_chars = ".!?"
    non_word_chars = ",;:-" + end_of_sentence_chars
    if last_char in end_of_sentence_chars:
        word = word[:-1]
        while len(word) and word[-1] in non_word_chars:
            word = word[:-1]
        word = word.lower()
        if word in common_abbreviations:
            return 0
        else:
            return 1
    else:
        return 0

def StripNonletters(word):
    while len(word) and word[-1] not in "abcdefghijklmnopqrstuvwxyz":
        word = word[:-1]
    return word

def CountSyllables(word):
    num = 0
    try:
        if words.word_syllables.has_key(word):
            num = words.word_syllables[word]
        else:
            num = guess_syllables(word)
    except:
        num = guess_syllables(word)
    return num

def CountStats(text):
    '''For a set string of text, return a tuple of the following items:
        number of characters
        number of words
        number of sentences
        number of syllables
        number of complex words (i.e., with >= 3 syllables)
    '''
    characters         = 0
    words              = 0
    complex_words      = 0
    one_syllable_words = 0
    syllables          = 0
    sentences          = 0
    for word in text.split():
        word = word.lower()  # Ignore proper nouns
        if EndOfSentence(word):
            sentences += 1
        words += 1
        word = StripNonletters(word)
        characters += len(word)
        number_of_syllables = CountSyllables(word)
        syllables += number_of_syllables
        if number_of_syllables >= 3:
            complex_words += 1
        if number_of_syllables == 1:
            one_syllable_words += 1
    return (characters, words, complex_words, one_syllable_words, 
            syllables, sentences)

def Usage():
    print "Usage:  %s file1 [file2...]\n" % sys.argv[0]
    print "Prints readability statistics for text files."
    if dbg:
        print '''    C    = number of characters in words
    W    = number of words
    CW   = number of complex words (3 or more syllables)
    SY   = number of syllables
    SENT = number of sentences'''
    print '''
FKRE = Flesch-Kincaid Reading Ease
    0-100, higher numbers mean easier to read

The following numbers are the approximate reading level in US grade level:
    FOG  = Gunning Fog Index
    ARI  = Automated Readibility Index
    CL   = Coleman-Liau Index
    FKGL = Flesch-Kincaid Grade Level
    SMOG = SMOG Index
    FORC = FORCAST Readability Formula

See the comments in the program code for formulas and references.'''
    sys.exit(0)

def PrintHeader():
    if dbg:
        print "     C      W    CW     OS    SY  SENT   FOG   ARI",
        print "   CL  FKRE  FKGL  SMOG  FORC"
    else:
        print "  FOG   ARI   CL   FKRE  FKGL  SMOG  FORC"

def PrintResults(stats, file):
    characters, words, complex_words, one_syllable_words, \
        syllables, sentences = stats
    fog  = GunningFogIndex(words, sentences, complex_words)
    ari  = AutomatedReadibilityIndex(characters, words, sentences)
    cl   = ColemanLiauIndex(characters, words, sentences)
    fkre = FleschKincaidReadingEase(words, syllables, sentences)
    fkgl = FleschKincaidGradeLevel(words, syllables, sentences)
    smog = SMOGIndex(complex_words, sentences)
    forc = FORCASTReadabilityFormula(words, one_syllable_words)
    if dbg:
        print "%6d %6d %5d %6d %5d %5d" % stats,
    fmt = "%5.1f " * 7
    print fmt % (fog, ari, cl, fkre, fkgl, smog, forc),
    print file

def main():
    if len(sys.argv) < 2:
        Usage()
    else:
        PrintHeader()
        for file in sys.argv[1:]:
            stats = CountStats(open(file).read())
            PrintResults(stats, file)

if __name__ == "__main__":
    main()


'''
Government officials urged parents to not let their children
trick or treat after dark because of power outages and
fallen power lines that still affect much of the area a week
after the storm struck. And even in areas with lights,
debris is piled high in front yards, making walking after
dark dangerous.

chars           249
words            53
complex words     3
syllables        79
sentences         2

GF = 28.544
ARI = 13.948
CL = 11.872
FKRE = 53.801
FKGL = 27.924
SMOG = 12.487
'''
