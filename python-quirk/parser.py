'''
                            Welcome to the parser.py

This programs takes a list of token inputs from the Lexer.py and creates a tree
structure by placing all non-terminal object nodes inside of a list of a
non-terminal parent nodes in the manner shown below.

    ['Term2', [Factor4, [Value1, ['Number0', 'NUMBER: 4']]]]

This is done by calling each function in a recursively descending manner, until
a terminal token is reached. The program is validated by the use of terminal
tokens, such as 'NUMBER: 4',in a way that once reached, the tokens validate and
cement the tree path which calls them; and falsify the tree path which called
them if they're not the specified token causing the tree to retrackt and take
another oute from each parent node.
'''

import sys
import pprint
import json

pp = pprint.PrettyPrinter(indent=1, depth=10000)

# begin utilities


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
# end utilities


def Program(token_index):
    '''
    <Program> ->
    <Statement> <Program>
    | <Program>
    '''
    # <Statement> <Program>
    (success, returned_index, returned_subtree) = Statement(token_index)
    if success:
        subtree = ["Program0",  returned_subtree]
        (success, returned_index, returned_subtree) = Program(returned_index)
        if success:
            subtree.append(returned_subtree)
            return [True, returned_index, subtree]

    # <Program>
    (success, returned_index, returned_subtree) = Statement(token_index)
    if success:
        return [True, returned_index, ["Program1", returned_subtree]]
    return [False, token_index, []]


def Statement(token_index):
    '''<Statement> ->
        <FunctionDeclaration>
        | <Assignment>
        | <Print>
    '''
    # <FunctionDeclaration>
    (success, returned_index, returned_subtree) = FunctionDeclaration(token_index)
    if success:
        return [True, returned_index, ["Statement0", returned_subtree]]
    # <Assignment>
    (success, returned_index, returned_subtree) = Assignment(token_index)
    if success:
        return [True, returned_index, ["Statement1", returned_subtree]]
    # <Print>
    (success, returned_index, returned_subtree) = Print(token_index)
    if success:
        return [True, returned_index, ["Statement2", returned_subtree]]
    return [False, token_index, []]


def FunctionDeclaration(token_index):
    '''
    <FunctionDeclaration> ->
        FUNCTION <Name> LPAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
    '''
    # FUNCTION <Name> LPAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
    if "FUNCTION" == tokens[token_index]:
        subtree = ["FunctionDeclaration0", tokens[token_index]]
        (success, returned_index, returned_subtree) = Name(token_index + 1)
        if success:
            subtree.append(returned_subtree)
            if "LPAREN" == tokens[returned_index]:
                subtree.append(tokens[returned_index])
                (success, returned_index, returned_subtree) = FunctionParams(
                    returned_index + 1)
                if success:
                    subtree.append(returned_subtree)
                    if "LBRACE" == tokens[returned_index]:
                        subtree.append(tokens[returned_index])
                        (success, returned_index, returned_subtree) = FunctionBody(
                            returned_index + 1)
                        if success:
                            subtree.append(returned_subtree)
                            if "RBRACE" == tokens[returned_index]:
                                subtree.append(tokens[returned_index])
                                return [True, returned_index + 1, subtree]
    return [False, token_index, []]


def FunctionParams(token_index):
    '''
    <FunctionParams> ->
        <NameList> RPAREN
        | RPAREN
    '''
    # <NameList> RPAREN
    (success, returned_index, returned_subtree) = NameList(token_index)
    if success:
        subtree = ["FunctionParams0", returned_subtree]
        if "RPAREN" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            return [True, returned_index + 1, subtree]
    # RPAREN
    if "RPAREN" == tokens[token_index]:
        subtree = ["FunctionParams1", tokens[token_index]]
        return [True, token_index + 1, subtree]
    return [False, token_index, []]


def FunctionBody(token_index):
    '''<FunctionBody> ->
        <Program> <Return>
        | <Return>
    '''
    # <Program> <Return>
    (success, returned_index, returned_subtree) = Program(token_index)
    if success:
        subtree = ["FunctionBody0",  returned_subtree]
        (success, returned_index, returned_subtree) = Return(returned_index)
        if success:
            subtree.append(returned_subtree)
            return [True, returned_index, subtree]

    # <Return>
    (success, returned_index, returned_subtree) = Return(token_index)
    if success:
        return [True, returned_index, ["FunctionBody1", returned_subtree]]
    return [False, token_index, []]


def Return(token_index):
    '''<Return> ->
        RETURN <ParameterList>
    '''
    # RETURN <ParameterList>
    if "RETURN" == tokens[token_index]:
        subtree = ["Return0", tokens[token_index]]
        (success, returned_index, returned_subtree) = ParameterList(token_index + 1)
        if success:
            subtree.append(returned_subtree)
            return [True, returned_index, subtree]
    return [False, token_index, []]


def Assignment(token_index):
    '''<Assignment> ->
        <SingleAssignment>
        | <MultipleAssignment>
    '''
    # <SingleAssignment>
    (success, returned_index, returned_subtree) = SingleAssignment(token_index)
    if success:
        return [True, returned_index, ["Assignment0", returned_subtree]]
    # <MultipleAssignment>
    (success, returned_index, returned_subtree) = MultipleAssignment(token_index)
    if success:
        return [True, returned_index, ["Assignment1", returned_subtree]]
    return [False, token_index, []]


def SingleAssignment(token_index):
    '''<SingleAssignment> ->
        VAR <Name> ASSIGN <Expression>
    '''
    # VAR <Name> ASSIGN <Expression>
    if "VAR" == tokens[token_index]:
        subtree = ["SingleAssignment0", tokens[token_index]]
        (success, returned_index, returned_subtree) = Name(token_index + 1)
        if success:
            subtree.append(returned_subtree)
            if "ASSIGN" == tokens[returned_index]:
                subtree.append(tokens[returned_index])
                (success, returned_index, returned_subtree) = Expression(
                    returned_index + 1)
                if success:
                    subtree.append(returned_subtree)
                    return [True, returned_index, subtree]
    return [False, token_index, []]


def MultipleAssignment(token_index):
    '''<MultipleAssignment> ->
        VAR <NameList> ASSIGN <FunctionCall>
    '''
    # VAR <NameList> ASSIGN <FunctionCall>
    if "VAR" == tokens[token_index]:
        subtree = ["MultipleAssignment0", tokens[token_index]]
        (success, returned_index, returned_subtree) = NameList(token_index + 1)
        if success:
            subtree.append(returned_subtree)
            if "ASSIGN" == tokens[returned_index]:
                subtree.append(tokens[returned_index])
                (success, returned_index, returned_subtree) = FunctionCall(
                    returned_index + 1)
                if success:
                    subtree.append(returned_subtree)
                    return [True, returned_index, subtree]
    return [False, token_index, []]


def Print(token_index):
    '''<Print> ->
        PRINT <Expression>
    '''
    # COMMA <Expression>
    if "PRINT" == tokens[token_index]:
        subtree = ["Print0", tokens[token_index]]
        (success, returned_index, returned_subtree) = Expression(token_index + 1)
        if success:
            subtree.append(returned_subtree)
            return [True, returned_index, subtree]
    return [False, token_index, []]


def NameList(token_index):
    '''<NameList> ->
        <Name> COMMA <NameList>
        | <Name>
    '''
    # <Name> COMMA <NameList>
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:
        subtree = ["NameList0", returned_subtree]
        if "COMMA" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = NameList(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Name>
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:
        return [True, returned_index, ["NameList1", returned_subtree]]
    return [False, token_index, []]


def ParameterList(token_index):
    '''<ParameterList> ->
        <Parameter> COMMA <ParameterList>
        | <Parameter>
    '''
    # <Parameter> COMMA <ParameterList>
    (success, returned_index, returned_subtree) = Parameter(token_index)
    if success:
        subtree = ["ParameterList0", returned_subtree]
        if "COMMA" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = ParameterList(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Parameter>
    (success, returned_index, returned_subtree) = Parameter(token_index)
    if success:
        return [True, returned_index, ["ParameterList1", returned_subtree]]
    return [False, token_index, []]


def Parameter(token_index):
    '''<Parameter> ->
        <Expression>
        | <Name>
    '''
    # <Expression>
    (success, returned_index, returned_subtree) = Expression(token_index)
    if success:
        return [True, returned_index, ["Parameter0", returned_subtree]]
    # <Name>
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:
        return [True, returned_index, ["Parameter1", returned_subtree]]
    return [False, token_index, []]


def Expression(token_index):
    '''<Expression> ->
        <Term> ADD <Expression>
        | <Term> SUB <Expression>
        | <Term>
    '''
    # <Term> ADD <Expression>
    (success, returned_index, returned_subtree) = Term(token_index)
    if success:
        subtree = ["Expression0", returned_subtree]
        if "ADD" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Expression(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Term> SUB <Expression>
    (success, returned_index, returned_subtree) = Term(token_index)
    if success:
        subtree = ["Expression1", returned_subtree]
        if "SUB" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Expression(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Term>
    (success, returned_index, returned_subtree) = Term(token_index)
    if success:
        return [True, returned_index, ["Expression2", returned_subtree]]
    return [False, token_index, []]


def Term(token_index):
    '''<Term> ->
        <Factor> MULT <Term>
        | <Factor> DIV <Term>
        | <Factor>
    '''
    # <Factor> MULT <Term>
    (success, returned_index, returned_subtree) = Factor(token_index)
    if success:
        subtree = ["Term0", returned_subtree]
        if "MULT" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Term(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Factor> DIV <Term>
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
    (success, returned_index, returned_subtree) = SubExpression(token_index)
    if success:
        subtree = ["Factor0", returned_subtree]
        if "EXP" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Factor(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <SubExpression>
    (success, returned_index, returned_subtree) = SubExpression(token_index)
    if success:
        subtree = ["Factor1", returned_subtree]
        return [True, returned_index, subtree]
    # <FunctionCall>
    (success, returned_index, returned_subtree) = FunctionCall(token_index)
    if success:
        return [True, returned_index, ["Factor2", returned_subtree]]
    # <Value> EXP <Factor>
    (success, returned_index, returned_subtree) = Value(token_index)
    if success:
        subtree = ["Factor3", returned_subtree]
        if "EXP" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = Factor(returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                return [True, returned_index, subtree]
    # <Value>
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
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:

        subtree = ["FunctionCall0", returned_subtree]
        if "LPAREN" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            (success, returned_index, returned_subtree) = FunctionCallParams(
                returned_index + 1)
            if success:
                subtree.append(returned_subtree)
                if "COLON" == tokens[returned_index]:
                    subtree.append(tokens[returned_index])
                    (success, returned_index, returned_subtree) = Number(
                        returned_index + 1)
                    if success:
                        subtree.append(returned_subtree)
                        return [True, returned_index, subtree]

    # <Name> LPAREN <FunctionCallParams>
        (success, returned_index, returned_subtree) = Name(token_index)
        if success:
            subtree = ["FunctionCall1", returned_subtree]
            if "LPAREN" == tokens[returned_index]:
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
    # <ParameterList> RPAREN
    (success, returned_index, returned_subtree) = ParameterList(token_index)
    if success:
        subtree = ["FunctionCallParams0", returned_subtree]
        if "RPAREN" == tokens[returned_index]:
            subtree.append(tokens[returned_index])
            return [True, returned_index + 1, subtree]
    # RPAREN
    if "RPAREN" == tokens[token_index]:
        subtree = ["FunctionCallParams1", tokens[token_index]]
        return [True, token_index + 1, subtree]
    return [False, token_index, []]


def SubExpression(token_index):
    '''<SubExpression> ->
        LPAREN <Expression> RPAREN
    '''
    if "LPAREN" == tokens[token_index]:
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
    # <name>
    (success, returned_index, returned_subtree) = Name(token_index)
    if success:
        return [True, returned_index, ["Value0", returned_subtree]]

    # <number>
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
    subtree = []
    if is_ident(tokens[token_index]):
        subtree = ["Name0", tokens[token_index]]
        return [True, token_index + 1, subtree]
    if "SUB" == tokens[token_index]:
        if is_ident(tokens[token_index + 1]):
            subtree = ["Name1", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
    if "ADD" == tokens[token_index]:
        if is_ident(tokens[token_index + 1]):
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
    if is_number(tokens[token_index]):
        subtree = ["Number0", tokens[token_index]]
        return [True, token_index + 1, subtree]
    if "SUB" == tokens[token_index]:
        if is_number(tokens[token_index + 1]):
            subtree = ["Number1", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
    if "ADD" == tokens[token_index]:
        if is_number(tokens[token_index + 1]):
            subtree = ["Number2", tokens[token_index], tokens[token_index + 1]]
            return [True, token_index + 2, subtree]
    return [False, token_index, subtree]


if __name__ == '__main__':
    # reads input from lexer.py print
    token_input = sys.stdin.read()
    '''
    splits the tokens of that result by whitespace, creating an extra empty
    token in the end, replacing 'EOF'
    '''
    tokens = token_input.split("\n")

    '''
    should be replaced by a statement that checks whether
    Program(0)[0] == 'true'
    '''
    token_result = (Program(0))[2]
    serializedPaseTree = json.dumps(token_result)
    # prints statement for interpreter.py to receive
    print(serializedPaseTree)
