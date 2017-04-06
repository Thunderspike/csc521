'''
                            Welcome to the lexer.py

This program's function is to create a stream of tokens marked by keywords
for the parser to process.

It does so by taking the input of a text file from the user and running it
through 3 functions.

The first function splits all the tokens by white space.
The second function splits all the tokens by all of the qurik special tokens
which aren't letters.
The third function takes all the tokens and either replaces them with their
assigned keywords, or appends a keyword if the token is a number or a name.
'''

import sys
import re
lexemes = []


def SplitSourceByWhitespace(source):
    # splits all entered lexems by whitespace
    allSplits = []
    for line in source:
        thisSplit = line.split()
        allSplits += thisSplit
    return allSplits


def SplitByUnvariedLexemes(source):
    # splits all lexemes by special tokens as shown in the regex below
    i = 0
    allSplits = []
    while i < len(source):
        line = source[i]
        Split = re.split(
            r'([=]|[+]|[-]|[*]|[\/]|[\^]|[\)]|[\(]|[\}]|[\{]|[,]|[:])', line)
        allSplits += Split
        i += 1
    return(allSplits)


def SplitByIdents(source):
    # splits all lexemes by keywords, IDENT words and NUMBERs
    source = list(filter(None, source))
    i = 0
    allSplits = []
    while i < len(source):
        line = str(source[i])
        matchIdent = re.search(r"\b([a-zA-Z]+[a-zA-Z0-9_]*)\b", line)
        matchNum = re.search(r"\b((\d+(\.\d*)?)|(\.\d+))\b", line)
        # print("token:", line)
        if (line == 'var'):
            sword = re.sub(r'\bvar\b', r'\bVAR\b', source[i])
            '''all tegex r'[\x08]+[.]* take out the \b tokens from the
            splitting process.
            '''
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == 'function'):
            sword = re.sub(r'\bfunction\b', r'\bFUNCTION\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == 'return'):
            sword = re.sub(r'\breturn\b', r'\bRETURN\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == 'print'):
            sword = re.sub(r'\bprint\b', r'\bPRINT\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == '='):
            sword = re.sub(r'[=]', r'\bASSIGN\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == '+'):
            sword = re.sub(r'[+]', r'\bADD\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == '-'):
            sword = re.sub(r'[-]', r'\bSUB\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == '*'):
            sword = re.sub(r'[*]', r'\bMULT\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == '/'):
            sword = re.sub(r'[\/]', r'\bDIV\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == '^'):
            sword = re.sub(r'[\^]', r'\bEXP\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == '('):
            sword = re.sub(r'[\(]', r'\bLPAREN\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == ')'):
            sword = re.sub(r'[\)]', r'\bRPAREN\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == '{'):
            sword = re.sub(r'[\{]', r'\bLBRACE\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == '}'):
            sword = re.sub(r'[\}]', r'\bRBRACE\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == ','):
            sword = re.sub(r'[,]', r'\bCOMMA\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif(line == ':'):
            sword = re.sub(r'[:]', r'\bCOLON\b', source[i])
            resword = re.split(r'[\x08]+[.]*', sword)
            allSplits += resword
        elif (matchIdent is not None):
            allSplits += ["IDENT:" + matchIdent.group(0)]
        elif (matchNum is not None):
            allSplits += ["NUMBER:" + matchNum.group(0)]
        else:
            print('Error with \'{}\'!'.format(line))
            print('Your variable name cannot start with a number, ')
            print('or contain anyspecial characters')
            sys.exit()
        allSplits = list(filter(None, allSplits))
        print(allSplits[i])
        i += 1


if __name__ == '__main__':
    # assigns the quirk file string to s
    s = sys.stdin.read()
    '''Calls SpplitSourceByWhitespace, SplitByUnvariedLexemes,
    and SplitsByIdents in that order, with input s.
    '''
    SplitByIdents(SplitByUnvariedLexemes(SplitSourceByWhitespace([s])))
    print("EOF")
