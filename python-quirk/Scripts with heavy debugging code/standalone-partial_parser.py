import sys
import pprint

pp = pprint.PrettyPrinter(indent=1, depth=10)

'''
tokens = ["VAR", "IDENT:X", "ASSIGN", "NUMBER:4"]
tokens = ["SUB", "IDENT:X", "ADD", "NUMBER:4"]
tokens = ["SUB", "IDENT:X", "EXP", "NUMBER:4", "EOF"]
tokens = ["SUB", "IDENT:X", "EXP", "NUMBER:4", "EXP", "IDENT:X", "EOF"]

tokens = ["NUMBER:9", "DIV", "IDENT:X", "EXP",
          "NUMBER:4", "EXP", "IDENT:X", "EOF"]
tokens = ["NUMBER:9", "ADD", "IDENT:X", "SUB", "NUMBER:4", "EOF"]
tokens = ["NUMBER:9", "ADD", "LPAREN", "IDENT:X",
          "SUB", "NUMBER:4", "RPAREN", "EOF"]
tokens = ["LPAREN", "IDENT:X", "SUB", "NUMBER:4", "RPAREN", "EOF"]
tokens = ["IDENT:FOO", "LPAREN", "RPAREN", "EOF"]
tokens = ["IDENT:FOO", "LPAREN", "RPAREN", "COLON", "NUMBER:0", "EOF"]
tokens = ["SUB", "IDENT:X", "EOF"]
tokens = ["NUMBER:4", "ADD", "NUMBER:4", "EOF"]
'''
tokens = ["SUB", "NUMBER:4", "NUMBER:6", "EOF"]


#begin utilities
def is_ident(tok):
    '''Determines if the token is of type IDENT.
    tok - a token
    returns True if IDENT is in the token or False if not.
    '''
    return -1 < tok.find("IDENT")

def is_number(tok):
    '''Determines if the token is of type NUMBER.
    tok - a token
    returns True if NUMBER is in the token or False if not.
    '''
    return -1 < tok.find("NUMBER")
#end utilities

'''
def Program(token_index):

    <Program> ->
    <Expression> <Program>
    | <Expression>

    # <Statement> <Program>
    print("the index of location in list = {}".format(token_index))
    print("\n# <Program0> -> <Expression> <Program>")
    (success, returned_index, returned_subtree) = Expression(token_index)
    if success:
        print("sucess at Program0", success)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Returned Subtree", returned_subtree)
        print("returned index {} and word at returned index ".format(returned_index))
        subtree = ["Program0",  returned_subtree]
        print("Subtree at Program0 = ", subtree)
        print("token returned to be scanned", tokens[returned_index])
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Token Index", token_index)
        (success, returned_index, returned_subtree) = Program(token_index + 1)
        if success:
            subtree.append(returned_subtree)
            return [True, returned_index, subtree]
    # <Program>
    (success, returned_index, returned_subtree) = Expression(token_index)
    if success:
        return [True, returned_index, ["Expression1", returned_subtree]]
    return [False, token_index,
'''

def Expression(token_index):
    '''<Expression> ->
        <Term> ADD <Expression>
        | <Term> SUB <Expression>
        | <Term>
    '''
    # <Term> ADD <Expression>
    print("the index of toekn in list = {}".format(token_index))
    print("\n\n\n\n\n\n\n\n\n# <Expression0> -> <Term> ADD <Expression>")
    (success, returned_index, returned_subtree) = Term(token_index)
    if success:
        print("sucess at expression0", success)
        subtree = ["Expression0", returned_subtree]
        print("Subtree at Expression0 = ", subtree)
        print("token returned to be scanned", tokens[returned_index])
        print("is the returns Index token an ADD string? '{}' If not move sideways".format("ADD" == tokens[returned_index]))
        if "ADD" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Expression(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Term> SUB <Expression>
    print("\n\n\n\n\n\n\n\n# <Expression1> -> <Term> SUB <Expression>")
    (success, returned_index, returned_subtree) = Term(token_index)
    print("is this it?", Term(token_index))
    if success:
        print("Sucess at Expression1", success)
        subtree = ["Expression1", returned_subtree]
        if "SUB" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            print("Subtree at Expression1 = ", subtree)
            print("token returned to be scanned", tokens[returned_index])
            print(returned_index+1)
            (success, returned_index, returned_subtree) = Expression(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Term>
    print("\n\n\n\n\n\n\n\n\n# <Expression2> -> <Term>")
    (success, returned_index, returned_subtree) = Term(token_index)
    print("Term(token_index)", Term(token_index))
    if success:
        print("Sucess at Expresssion2", success)
        print("Subtree at Expression2 = ", subtree)
        print("token returned to be scanned", tokens[returned_index])
        return [True, returned_index, ["Expression2", returned_subtree]]
    return [False, token_index, []]


def Term(token_index):
    '''<Term> ->
        <Factor> MULT <Term>
        | <Factor> DIV <Term>
        | <Factor>
    '''
    # <Factor> MULT <Term>
    print("\n# <Term0> -> <Factor> MULT <Term>")
    (success, returned_index, returned_subtree) = Factor(token_index)
    if success:
        subtree = ["Term0", returned_subtree]
        if "MULT" == tokens[returned_index]:
            print('\'{}\' is the token in question'.format(tokens[token_index]))
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Term(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Factor> DIV <Term>
    print("\n# <Term1> -> <Factor> DIV <Term>")
    (success, returned_index, returned_subtree) = Factor(token_index)
    if success:
        subtree = ["Term1", returned_subtree]
        if "DIV" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Term(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Factor>
    print("\n# <Term2> -> <Factor>")
    (success, returned_index, returned_subtree) = Factor(token_index)
    if success:
        return [True, returned_index, ["Term2", returned_subtree]]
    return [False, token_index, []]


def Factor(token_index):
    '''
    <Factor> ->
        <SubExpression>
        | <SubExpression> EXP <Factor>
        | <FunctionCall>
        | <Value> EXP <Factor>
        | <Value>
    '''
    # <SubExpression> EXP <Factor>
    print("\n# <Factor0> -> <SubExpression> EXP <Factor>")
    (success, returned_index, returned_subtree) = SubExpression(token_index)
    if success:
        subtree = ["Factor0", returned_subtree]
        if "EXP" == tokens[returned_index]:
            print('\'{}\' is the token in question'.format(tokens[token_index]))
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Factor(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <SubExpression>
    print("\n# <Factor1> -> <SubExpression>")
    (success, returned_index, returned_subtree) = SubExpression(token_index)
    if success:
        subtree = ["Factor1", returned_subtree]
        return [True, returned_index, subtree]
    # <FunctionCall>
    print("\n# <Factor2> -> <FunctionCall>")
    (success, returned_index, returned_subtree) = FunctionCall(token_index)
    if success:
        return [True, returned_index, ["Factor2", returned_subtree]]
    # <Value> EXP <Factor>
    print("\n# <Factor3> -> <Value> EXP <Factor>")
    (success, returned_index, returned_subtree) = Value(token_index)
    if success:
        subtree = ["Factor3", returned_subtree]
        if "EXP" == tokens[returned_index]:
            print('\'{}\' is the token in question'.format(tokens[token_index]))
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Factor(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Value>
    print("\n# <Factor4> -> <Value>")
    (success, returned_index, returned_subtree) = Value(token_index)
    if success:
        return [True, returned_index, ["Factor4", returned_subtree]]
    return [False, token_index, []]


def FunctionCall(token_index):
    '''
    <FunctionCall> ->
        <Name> LPAREN <FunctionCallParams> COLON <Number>
        | <Name> LPAREN <FunctionCallParams>
    '''
    # <Name> LPAREN <FunctionCallParams> COLON <Number>
    print("\n# <FunctionCall0> -> <Name> LPAREN <FunctionCallParams> COLON <Number>")
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:
        subtree = ["FunctionCall0", returned_subtree]
        if "LPAREN" == tokens[returned_index]:
            print('\'{}\' is the token in question'.format(tokens[token_index]))
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = FunctionCallParams(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                print('\'{}\' is the token in question'.format(tokens[token_index]))
                if "COLON" == tokens[returned_index]:
                    subtree.append(tokens[returned_index])
                    (success, returned_index, returned_subtree) = Number(
                        returned_index + 1)
                    if success:
                        subtree.append(returned_subtree)
                        return [True, returned_index, subtree]

    # <Name> LPAREN <FunctionCallParams>
    print("\n# <FunctionCall1> -> <Name> LPAREN <FunctionCallParams>")
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:
        subtree = ["FunctionCall1", returned_subtree]
        if "LPAREN" == tokens[returned_index]:
            print('\'{}\' is the token in question'.format(tokens[token_index]))
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = FunctionCallParams(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    return [False, token_index, []]


def FunctionCallParams(token_index):
    '''
    <FunctionCallParams> ->
        <ParameterList> RPAREN
        | RPAREN
    '''
    #<ParameterList> RPAREN
    # todo after ParameterList is finished
    # RPAREN
    print("\n# <FunctionCallParams1> -> RPAREN")
    if "RPAREN" == tokens[token_index]:
        print('\'{}\' is the token in question'.format(tokens[token_index]))
        subtree = ["FunctionCallParams1", tokens[token_index]]
        return [True, token_index + 1, subtree]
    return [False, token_index, []]


def SubExpression(token_index):
    '''<SubExpression> ->
        LPAREN <Expression> RPAREN
    '''
    print("\n# <SubExpression0> -> LPAREN <Expression> RPAREN")
    print("Is your token a terminal LPAREN? '{}' If not, move back to the node that called this one.".format("LPAREN" == tokens[token_index]))
    if "LPAREN" == tokens[token_index]:
        print('\'{}\' is the token in question'.format(tokens[token_index]))
        subtree = ["SubExpression0", tokens[token_index]]
        (success, returned_index, returned_subtree) = Expression(token_index + 1)
        if success:
            subtree.append(returned_subtree)
            if "RPAREN" == tokens[returned_index]:
                subtree.append(tokens[returned_index])
                return [True, returned_index + 1, subtree]
    return [False, token_index, []]


def Value(token_index):
    '''
    <Value> ->
        <Name>
        | <Number>
    '''
    # try in order!
    # <Name>
    print("\n# <Value0> -> <Name>")
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:
        return [True, returned_index, ["Value0", returned_subtree]]
    # <Number>
    print("\n# <Value1> -> <Number>")
    (success, returned_index, returned_subtree) = Number(token_index)
    if success:
        return [True, returned_index, ["Value1", returned_subtree]]
    return [False, token_index, []]


def Name(token_index):
    '''<Name> ->
        IDENT
        | SUB IDENT
        | ADD IDENT
    '''
    print("\n# <Name0> -> IDENT")
    subtree = []
    print("Empty the subtree")
    print("is your terminal an IDENT? '{}' If not, move to Name1".format(is_ident(tokens[token_index])))
    if is_ident(tokens[token_index]):
        print('\'{}\' is the token in question'.format(tokens[token_index]))
        subtree = ["Name0", tokens[token_index]]
        return [True, token_index + 1, subtree]
    print("\n# <Name1> -> SUB IDENT")
    print("Does your Terminal have SUB infront of it? '{}' If not, move to Name2.".format("SUB" == tokens[token_index]))
    if "SUB" == tokens[token_index]:
        print("Is the next token an IDENT? {} If not, move to Name2.".format(is_ident(tokens[token_index + 1])))
        if is_ident(tokens[token_index + 1]):
            print('\'{}\' is the token in question'.format(tokens[token_index]))
            subtree = ["Name1", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
            print("returning: ",[True, token_index + 2, subtree])
    print("\n# <Name2> -> ADD IDENT")
    print("Does your terminal have ADD infront of it? '{}' If not move up the tree.".format("ADD" == tokens[token_index]))
    if "ADD" == tokens[token_index]:
        print("Is the next token an IDENT? {} If not move up the tree.".format(is_ident(tokens[token_index + 1])))
        if is_ident(tokens[token_index + 1]):
            print('\'{}\' is the token in question'.format(tokens[token_index]))
            subtree = ["Name2", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
    return [False, token_index, subtree]


def Number(token_index):
    '''<Number> ->
        NUMBER
        | SUB NUMBER
        | ADD NUMBER
    '''
    subtree = []
    print('\n# <Number0> -> NUMBER')
    print("Is your terminal a NUMBER? '{}' If not, move to Number1".format(is_number(tokens[token_index])))
    if is_number(tokens[token_index]):
        print('\'{}\' is the token in question'.format(tokens[token_index]))
        subtree = ["Number0", tokens[token_index]]
        return [True, token_index + 1, subtree]
    print('\n# <Number1> -> SUB NUMBER')
    print("Does your terminal have SUB infront of it? '{}' If not, move to Number2".format("SUB" == tokens[token_index]))
    if "SUB" == tokens[token_index]:
        print("Is the next token in line, after the SUB, a number? '{}' If not move to Number2".format(is_number(tokens[token_index + 1])))
        if is_number(tokens[token_index + 1]):
            print('\'{}\' is the token in question'.format(tokens[token_index]))
            subtree = ["Number1", tokens[token_index], tokens[token_index + 1]]
            print('Sending to the caller of the sucess chain:', [True, token_index + 2, subtree])
            return [True, token_index + 2, subtree]
            print("SubtreeReturned", subtree)
    print('\n# <Number2> -> ADD NUMBER')
    print(print("Does your terminal have ADD infront of it? '{}' If not, move up the tree".format("ADD" == tokens[token_index])))
    if "ADD" == tokens[token_index]:
        print("Is the next token in line, after the ADD, a number? '{}' If not move up the tree".format(is_number(tokens[token_index + 1])))
        if is_number(tokens[token_index + 1]):
            print('\'{}\' is the token in question'.format(tokens[token_index]))
            subtree = ["Number2", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
    return [False, token_index, subtree]
if __name__ == '__main__':
    print("starting __main__")
    pp.pprint(Expression(0))
