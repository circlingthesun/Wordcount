import os
import sys

ignoredList = ["document", "tiny", "scriptsize", "footnotesize", "small", "normalsize", "large", "Large", "LARGE", "huge", "huge", "flushleft", "center", "flushright"]
words = []

#########################################

def begin(command, index):
        i = index
        if ignoredList.count(command):
                try: wordNos.remove(i)
                except ValueError:
                                return
                        
                while words[i].find("\\end{" + str(command) +"}") == -1:
                        i+=1
                try: wordNos.remove(i)
                except ValueError:
                        return
        else:
                while words[i].find("\\end{" + str(command) +"}") == -1:
                        try: wordNos.remove(i)
                        except ValueError:
                                return
                        i+=1
                wordNos.remove(i)
                return
                
#########################################

def backslashFn(index, opnCu, clsCu, opnSq, clsSq):
        try: wordNos.remove(index)
        except ValueError:
                return
        opnCu += words[index].count("{")
        clsCu += words[index].count("}")
        opnSq += words[index].count("[")
        clsSq += words[index].count("]")
        if clsCu == opnCu and clsSq == opnSq:
                return
        else:
                return backslashFn(index+1, opnCu, clsCu, opnSq, clsSq)
                
#########################################

def dollar(index, no, sinDbl):
        #print index, no
        try: wordNos.remove(index)
        except ValueError:
                return
        no += words[index].count("$"*sinDbl)
        if no%2 == 0:
                return
        else:
                return dollar(index+1, no, sinDbl)

#########################################

def latexcount(path):

    # read file
    try:
        f = open(path, 'rb')
    except IOError:
        print("Please provide a valid .tex-file.")
        sys.exit()

    wholewords = f.read()
    f.close()

    # start main script
    lines = wholewords.splitlines()

    # remove comments
    i = 0
    while i < len(lines):
            if len(lines[i]) > 0 and lines[i][0] == "%":
                    del(lines[i])
                    continue
            if lines[i].find("%") != -1:
                    if lines[i][lines[i].find("%")-1] != ("\\"):
                            lines[i] = lines[i][:lines[i].find("%")]
            if len(lines[i]) == 0:
                    lines.pop(i)
                    continue
            i +=1
                            
    global words
    words = []

    for i in range(len(lines)):
            words.append(lines[i].split())    

    words = sum(words, [])

    global wordNos

    wordNos = range(len(words))

    for i in range(len(words)):
    # "dollar sign" equations

            if words[i].count("$")>0 and words[i].count("$")%2 == 0 and words[i].count("$$")%2 == 0:
                    try: wordNos.remove(i)
                    except ValueError:
                            continue                
            elif words[i].count("$")%2 == 1 and words[i].count("$$")%2 == 0 and wordNos.count(i) == 1:
                    wordNos.remove(i)
                    dollar(i+1, words[i].count("$"), 1)
            elif words[i].count("$")%2 == 0 and words[i].count("$$")%2 == 1 and wordNos.count(i) == 1:
                    wordNos.remove(i)
                    dollar(i+1, words[i].count("$$"), 2)
    #begin and end functions
            elif words[i].find("\\begin{") == 0:
                    begin(words[i][7:words[i].find("}")], i)
            elif words[i].find("\\begin{") > 0:
                    begin(words[i][7:words[i].find("}")], i+1)
    #named functions
            elif words[i].find("\\") == 0 and words[i].count("{") == words[i].count("}") and words[i].count("[") == words[i].count("]"):
                    try: wordNos.remove(i)
                    except ValueError:
                            continue
            elif words[i].find("\\") == 0 and words[i].count("{") > words[i].count("}") or words[i].count("[") > words[i].count("]"):
                    try: wordNos.remove(i)
                    except ValueError:
                            continue
                    backslashFn(i+1, words[i].count("{"), words[i].count("}"), words[i].count("["), words[i].count("]"))


    return len(wordNos)

if __name__ == '__main__':
    try:
        print latexcount(sys.argv[1])
    except:    
        exit()   
