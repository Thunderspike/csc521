'''
                            Welcome to the interpreter.py

This program takes input from the parser.py in a form of a string, turns it into
the tree object through json.load and unpacks the structure of the tree.

It functions by traversing through the tree with the lookup_in_scope_stack func,
and passing number and ident terminals back to python for execution. This
program will output a print statement if the tree recieved has a Print0 node.
'''

import sys
import pprint
import json

pp = pprint.PrettyPrinter(indent=1, depth=100)

#start utilities
def lookup_in_scope_stack(name, scope):
    '''Returns values (including declared functions!) from the scope.
    name - A string value holding the name of a bound variable or function.
    scope - The scope that holds names to value binding for variables and
        functions.
    returns - the value associated with the name in scope.
    '''

    if str(name) in scope:
        return scope[name]
    else:
        if "__parent__" in scope:
            return lookup_in_scope_stack(name, scope["__parent__"])

def get_name_from_ident(tok):
    '''Returns the string lexeme associated with an IDENT token, tok.
    '''
    colon_index = tok.find(":")
    return str(tok[colon_index+2:])
    '''
    all colon_index above are +2 because I made all IDENTs have a space
    before declaration
    '''

def get_number_from_ident(tok):
    '''Returns the float lexeme associated with an NUMBER token, tok.
    '''
    colon_index = tok.find(":")
    return float(tok[colon_index+2:])
    '''
    all colon_index above are +2 because I made all NUMBERs have a space
    before declaration
    '''

def func_by_name(*args):
    '''Calls a function whos name is given as a parameter. It requires the parse
        tree associated with that point in the grammar traversal and the current
        scope.
    *args is interpreted as
        name = args[0] -- the name of the function to call
        pt = args[1] -- the subtree of the parse tree associated with the name
        scope = args[2] -- the scope the subtree should use
    return - Pass through the return value of the called function.
    '''
    name = args[0]
    pt = args[1]
    scope = args[2]
    return globals()[name](pt, scope) #this is how you call another function
#end utilities

# <Program> -> <Statement> <Program> | <Statement>
def Program0(pt, scope):
    #Program0 calling the next thing in the pt, and than calling program0 again
    func_by_name(pt[1][0], pt[1], scope)
    func_by_name(pt[2][0], pt[2], scope)

def Program1(pt, scope):
    #calling the next token <Statement> with name, partial parse tree, and scope
    func_by_name(pt[1][0], pt[1], scope)

# <Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
def Statement0(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)

#<Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
def Statement1(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


def Statement2(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)

# <FunctionDeclaration> -> FUNCTION <Name> PAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
def FunctionDeclaration0(pt, scope):
    #1. Get function name.
    funcDec_Name = func_by_name(pt[2][0], pt[2], scope)[1]
    #2. Get names of parameters.
    funcDec_Params = func_by_name(pt[4][0], pt[4], scope)
    #3. Get reference to function body subtree.
    funcDec_Body = pt[6]
    '''
    4. In scope, bind the function's name to the following list:
        "foo": [['p1', 'p2', 'p3'], [FunctionBodySubtree]]
        where foo is the function names, p1, p2, p2 are the parameters and
        FunctionBodySubtree represents the partial parse tree that holds the
        FunctionBody0 expansion. This would correspond to the following code:
        function foo(p1, p2, p3) { [the function body] }
    '''
    scope[funcDec_Name] = [funcDec_Params, funcDec_Body]

# <FunctionParams> -> <NameList> RPAREN | RPAREN
def FunctionParams0(pt, scope):
    #Returns a list of values to FunctionDeclaration
    return func_by_name(pt[1][0], pt[1], scope)

def FunctionParams1(pt, scope):
    return []

# <FunctionBody> -> <Program> <Return> | <Return>
def FunctionBody0(pt, scope):
    #calls Program
    func_by_name(pt[1][0], pt[1], scope)
    #returns a list of values of the program
    return func_by_name(pt[2][0], pt[2], scope)

def FunctionBody1(pt, scope):
    #returns a list of values of the program
    return func_by_name(pt[1][0], pt[1], scope)

# <Return> -> RETURN <ParameterList>
def Return0(pt, scope):
    #returns a list of params
    return func_by_name(pt[2][0], pt[2], scope)

# <Assignment> -> <SingleAssignment> | <MultipleAssignment>
def Assignment0(pt, scope):
    #calls SingleAssignment through func_by_name
    func_by_name((pt[1][0]), pt[1], scope)

def Assignment1(pt, scope):
    #calls MultipleAssignment through func_by_name
    func_by_name(pt[1][0], pt[1], scope)

# <SingleAssignment> -> VAR <Name> ASSIGN <Expression>
def SingleAssignment0(pt, scope):
    # adds name and expression to the scope by:

    #1. Get name of the variable.
    var_Name = func_by_name(pt[2][0], pt[2], scope)[1]
    #2. Get value of <Expression>
    var_Value = func_by_name(pt[4][0], pt[4], scope)
    #3. Bind name to value in scope.
    scope[var_Name] = var_Value

# <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
def MultipleAssignment0(pt, scope):
    # binds multiple names to expressions by:

    #1. Get list of variable names
    var_Names =  func_by_name(pt[2][0], pt[2], scope)
    #2. Get the values returned from the fuction call
    funcCall_values = func_by_name(pt[4][0], pt[4], scope)
    i = 0
    #3. Bind name to value in scope.
    while i < len(funcCall_values):
        scope[var_Names[i]] = funcCall_values[i]
        i += 1


# <Print> -> PRINT <Expression>
def Print0(pt, scope):
    #prints as a string the expression called by the second token in the pt
    print("\n",str(func_by_name(pt[2][0], pt[2], scope)))

# <NameList> -> <Name> COMMA <NameList> | <Name>
def NameList0(pt, scope):
    #returning a list of names
    param_name = func_by_name(pt[1][0], pt[1], scope)[1]
    return [param_name] + func_by_name(pt[3][0], pt[3], scope)

def NameList1(pt, scope):
    #returning a singular name
    #getting the [1] of the return value for name as it returns a [val, name]
    return [func_by_name(pt[1][0], pt[1], scope)[1]]

# <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
def ParameterList0(pt, scope):
    #returning a list of values
    param = func_by_name(pt[1][0], pt[1], scope)
    return [param] + [func_by_name(pt[3][0], pt[3], scope)]


def ParameterList1(pt, scope):
    #returning a singular parameter
    return func_by_name(pt[1][0], pt[1], scope)

# <Parameter> -> <Expression> | <Name>
def Parameter0(pt, scope):
    #returns the value of the subtree of Expression
    return func_by_name(pt[1][0], pt[1], scope)

def Parameter1(pt, scope):
    #returning the value of the subtree of Name
    return func_by_name(pt[1][0], pt[1], scope)[0]

#<Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
def Expression0(pt, scope):
    #returning the added value of the left <Term> and right <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value + right_value

def Expression1(pt, scope):
    #returning the subtracted value of the left <Term> and right <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return (left_value) - (right_value)

def Expression2(pt, scope):
    #returning the value of the subtere of Term
    return func_by_name(pt[1][0], pt[1], scope)

#<Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
def Term0(pt, scope):
    #returning the product value of the left <Term> and right <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value * right_value

def Term1(pt, scope):
    #returning the product value of the left <Term> dividing right <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value / right_value

def Term2(pt, scope):
    #returning the value of the subtere of Factor
    return func_by_name(pt[1][0], pt[1], scope)

#<Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>
def Factor0(pt, scope):
    #returning value of <SubExpression> to the power of <Factor>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value ** right_value

def Factor1(pt, scope):
    #returning the value of the subtree of SubExpression
    return func_by_name(pt[1][0], pt[1], scope, scope)

def Factor2(pt, scope):
    #returns the values of FunctionCall
    return func_by_name(pt[1][0], pt[1], scope, scope)#[0]

def Factor3(pt, scope):
    #returning value of <Value> to the power of <Factor>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value ** right_value

def Factor4(pt, scope):
    #returning the value of the subtree of Value
    return func_by_name(pt[1][0], pt[1], scope)

#<FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number>
#                   | <Name> LPAREN <FunctionCallParams>
def FunctionCall0(pt, scope):

    #1. Get the function name.
    funcName = get_name_from_ident(pt[1][1])
    #2. Retrieve the stored function information from scope.
    stored_Func_pt = scope[funcName]
    #3. Make a new scope with old scope as __parent__
    new_scope = {"__parent__" : scope}
    #4. Get the list of parameter values.
    get_params_vals = func_by_name(pt[3][0], pt[3], scope)
    #5. Bind parameter names to parameter values in the new function scope.
    if type(get_params_vals) == float: #float if single value
        new_scope[stored_Func_pt[0][0]] = get_params_vals
    else: #List type otherwise
        i = 0
        while i < len(get_params_vals):
            new_scope[stored_Func_pt[0][i]] = get_params_vals[i]
            i += 1
        print("\nThis is your functioncall's scope!")
        pp.pprint(new_scope)
        '''
    #6. Run the FunctionBody subtree that is part of the stored function
        information.
        '''
    function_body_pt = (lookup_in_scope_stack(funcName, scope))[1]
    list_of_vals = func_by_name(function_body_pt[0], function_body_pt, new_scope)
    #7. Get the index return number.
    index_return_number = int(func_by_name(pt[5][0], pt[5], new_scope))
    '''
    #8. Return one value from the list of return values that corresponds to the
       index number.
    '''
    return list_of_vals[index_return_number - 1]

def FunctionCall1(pt, scope):

    # 1. Get the function name.
    funcName = get_name_from_ident(pt[1][1])
    # 2. Retrieve the stored function information from scope.
    stored_Func_pt = scope[funcName]
    # 3. Make a new scope with old scope as __parent__
    new_scope = {"__parent__" : scope}
    # 4. Get the list of parameter values.
    get_params_vals = func_by_name(pt[3][0], pt[3], scope)
    # 5. Bind parameter names to parameter values in the new function scope.
    i = 0
    while i < len(get_params_vals):
        new_scope[stored_Func_pt[0][i]] = get_params_vals[i]
        i += 1
    # 6. Run the FunctionBody subtree that is part of the stored function information.
    function_body_pt = (lookup_in_scope_stack(funcName, scope))[1]
    list_of_vals = func_by_name(function_body_pt[0], function_body_pt, new_scope)
    # 7. Return the list of values generated by the <FunctionBody>
    return func_by_name(function_body_pt[0], function_body_pt, new_scope)


#<FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
def FunctionCallParams0(pt, scope):
    #Returns a list of parameters from ParameterList
    return func_by_name(pt[1][0], pt[1], scope)

def FunctionCallParams1(pt, scope):
    return[]

#<SubExpression> -> LPAREN <Expression> RPAREN
def SubExpression0(pt, scope):
    #returns the value of the Expression subtree
    return func_by_name(pt[2][0], pt[2], scope)

#<Value> -> <Name> | <Number>
def Value0(pt, scope):
    #returns the name value of the Name subtree
    return func_by_name(pt[1][0], pt[1], scope)[0]

def Value1(pt, scope):
    #returns the int value of the Number subtree
    return func_by_name(pt[1][0], pt[1], scope)

#<Name> -> IDENT | SUB IDENT | ADD IDENT
def Name0(pt, scope):
    #retrieves name from the Name subtree list
    name = get_name_from_ident(pt[1])
    #returns [value, name]
    return [lookup_in_scope_stack(name, scope), name]

def Name1(pt, scope):
    #retrieves name from the Name subtree list
    name = get_name_from_ident(pt[2])
    #returns [-value, name]
    return [-lookup_in_scope_stack(name, scope), name]

def Name2(pt, scope):
    #retrieves name from the Name subtree list
    name = get_name_from_ident(pt[2])
    #returns [value, name]
    return [lookup_in_scope_stack(name, scope), name]

#<Number> -> NUMBER | SUB NUMBER | ADD NUMBER
def Number0(pt, scope):
    #retrieves the number value from the Number subtree list
    return get_number_from_ident(pt[1])

def Number1(pt, scope):
    #retrieves the negative number value from the Number subtree list
    return (-(get_number_from_ident(pt[2])))

def Number2(pt, scope):
    #retrieves the number value from the Number subtree list
    return get_number_from_ident(pt[2])

if __name__ == '__main__':
    #saves the .read input in string_from_parser
    string_from_parser = sys.stdin.read()
    #unpacks string_from_parser into the tree structure in tree
    tree = json.loads(string_from_parser)
    #creates scope dictionary
    scope = {}
    #starts the execution of the program
    func_by_name(tree[0], tree, scope)
