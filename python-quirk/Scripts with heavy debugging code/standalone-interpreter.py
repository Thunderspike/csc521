import sys
import pprint
import json

pp = pprint.PrettyPrinter(indent=1, depth=100)

'''Scope example:
var x = 4 #{'x':4}
function foo(z) {
    foo(z/2)
    return z + x
}
foo(14)
Inside of foo(14), the scope looks like this:
{
 'z':7,
 "__parent__": {
    'z':14,
    "__parent__": {
        'x':4
    }
 }
}
'''
tree_with_function_call = ['Program0',
  ['Statement0',
   ['FunctionDeclaration0',
    'FUNCTION',
    ['Name0', 'IDENT: cloud_func'],
    'LPAREN',
    ['FunctionParams0', ['NameList1', ['Name0', 'IDENT: a']], 'RPAREN'],
    'LBRACE',
    ['FunctionBody1',
     ['Return0',
      'RETURN',
      ['ParameterList0',
       ['Parameter0',
        ['Expression2',
         ['Term2', ['Factor4', ['Value0', ['Name0', 'IDENT: a']]]]]],
       'COMMA',
       ['ParameterList0',
        ['Parameter0',
         ['Expression2',
          ['Term2',
           ['Factor3',
            ['Value0', ['Name0', 'IDENT: a']],
            'EXP',
            ['Factor4', ['Value1', ['Number0', 'NUMBER: 2']]]]]]],
        'COMMA',
        ['ParameterList1',
         ['Parameter0',
          ['Expression2',
           ['Term2',
            ['Factor3',
             ['Value0', ['Name0', 'IDENT: a']],
             'EXP',
             ['Factor4', ['Value1', ['Number0', 'NUMBER: 3']]]]]]]]]]]],
    'RBRACE']],
  ['Program1',
   ['Statement2',
    ['Print0',
     'PRINT',
     ['Expression2',
      ['Term2',
       ['Factor2',
        ['FunctionCall0',
         ['Name0', 'IDENT: cloud_func'],
         'LPAREN',
         ['FunctionCallParams0',
          ['ParameterList1',
           ['Parameter0',
            ['Expression2',
             ['Term2', ['Factor4', ['Value1', ['Number0', 'NUMBER: 2']]]]]]],
          'RPAREN'],
         'COLON',
         ['Number0', 'NUMBER: 1']]]]]]]]]

# scope_with_function = {'x':100, 'z':101}

#start utilities
def lookup_in_scope_stack(name, scope):
    '''Returns values (including declared functions!) from the scope.
    name - A string value holding the name of a bound variable or function.
    scope - The scope that holds names to value binding for variables and
        functions.
    returns - the value associated with the name in scope.
    '''
    #turn this on for better debugging
    print("lookup_in_scope_stack() "+ str(name))
    if str(name) in scope:
        if len(scope) < 3:
            print("scope of name", name, " = ")
            pp.pprint(scope[name])
        else:
            print("scope of name", name, " = ", scope[name])
        return scope[name]
    else:
        if "__parent__" in scope:
            print("not found in scope. Looking at __parent__")
            return lookup_in_scope_stack(name, scope["__parent__"])
        else:
            print("ERROR: variable " + name + " was not found in scope stack!")

def get_name_from_ident(tok):
    '''Returns the string lexeme associated with an IDENT token, tok.
    '''
    print("get_name_from_ident() " + tok)
    colon_index = tok.find(":")
    return str(tok[colon_index+2:])
    '''
    all colon_index above are +2 because I made all IDENTs have a space
    before declaration
    '''

def get_number_from_ident(tok):
    '''Returns the float lexeme associated with an NUMBER token, tok.
    '''
    print("get_number_from_ident() " + tok)
    colon_index = tok.find(":")
    print(float(tok[colon_index+2:]))
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
    print("func_by_name() calling --->", name, "\nParse Tree:")
    pp.pprint(pt)
    print("Scope Dict:", scope)
    return globals()[name](pt, scope) #this is how you call another function
#end utilities

# <Program> -> <Statement> <Program> | <Statement>
def Program0(pt, scope):
    print("\nhey, we're here now")
    print("Program0 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    func_by_name(pt[1][0], pt[1], scope)
    print("\nProgram0 sending func_by_name() this arg[0] --->", pt[2][0], "\narg[2] as tree:")
    pp.pprint(pt[2])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    func_by_name(pt[2][0], pt[2], scope)

def Program1(pt, scope):
    print("\nProgram1 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    func_by_name(pt[1][0], pt[1], scope)

# <Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
def Statement0(pt, scope):
    print("\nStatement0 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    func_by_name(pt[1][0], pt[1], scope)

def Statement1(pt, scope):
    print("\nStatement1 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    func_by_name(pt[1][0], pt[1], scope)

def Statement2(pt, scope):
    print("\nStatement2 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    func_by_name(pt[1][0], pt[1], scope)

# <FunctionDeclaration> -> FUNCTION <Name> PAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
def FunctionDeclaration0(pt, scope):
    '''
    1. Get function name.
    2. Get names of parameters.
    3. Get reference to function body subtree.
    4. In scope, bind the function's name to the following list:
        "foo": [['p1', 'p2', 'p3'], [FunctionBodySubtree]]
        where foo is the function names, p1, p2, p2 are the parameters and
        FunctionBodySubtree represents the partial parse tree that holds the
        FunctionBody0 expansion. This would correspond to the following code:
        function foo(p1, p2, p3) { [the function body] }
    #Bonus: check for return value length at declaration time
    '''
    funcDec_Name = func_by_name(pt[2][0], pt[2], scope)[1]
    print("\nFunction Name", funcDec_Name)
    print("\n\n\nFunctionDeclaration0 seeking params from:" )
    pp.pprint(pt[4])
    funcDec_Params = func_by_name(pt[4][0], pt[4], scope)
    funcDec_Body = pt[6]
    print("\nfuncDec_Body >>>>>>>>>>>>>>>>>>\n")
    pp.pprint(pt[6])
    scope[funcDec_Name] = [funcDec_Params, funcDec_Body]
    print(scope)

# <FunctionParams> -> <NameList> RPAREN | RPAREN
# should return a list of values
def FunctionParams0(pt, scope):
    print("\FunctionParams0 returning func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope)

def FunctionParams1(pt, scope):
    print("Closing parantheses")
    return []

# <FunctionBody> -> <Program> <Return> | <Return>
def FunctionBody0(pt, scope):
    print("\nFunctionBody0 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    func_by_name(pt[1][0], pt[1], scope)
    print("\nFunctionBody0 sending func_by_name() this arg[0] --->", pt[2][0], "\narg[2] as tree:")
    pp.pprint(pt[2])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[2][0], pt[2], scope)

def FunctionBody1(pt, scope):
    print("\nFunctionBody0 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope)

# <Return> -> RETURN <ParameterList>
def Return0(pt, scope):
    return func_by_name(pt[2][0], pt[2], scope)


# <Assignment> -> <SingleAssignment> | <MultipleAssignment>
def Assignment0(pt, scope):
    print("\nAssignment0 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    func_by_name((pt[1][0]), pt[1], scope)

def Assignment1(pt, scope):
    print("\nAssignment1 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    func_by_name(pt[1][0], pt[1], scope)

# <SingleAssignment> -> VAR <Name> ASSIGN <Expression>
def SingleAssignment0(pt, scope):

    print("\nRetrieving Var_Name\n")
    #1. Get name of the variable.
    var_Name = func_by_name(pt[2][0], pt[2], scope)[1]
    print("\n\nname of SingleAssignment0 -> {}\n\n".format(var_Name))
    #2. Get value of <Expression>
    print("\nRetrieving Var_Value\n")
    var_Value = func_by_name(pt[4][0], pt[4], scope)
    print("\n\nvalue of SingleAssignment0 -> {}\n\n".format(var_Value))
    #3. Bind name to value in scope.
    scope[var_Name] = var_Value
    print("Your scope now contains:")
    pp.pprint(scope)
    #Bonus: error if the name already exists in scope -- no rebinding
    '''
    print("#####################executing", pt)
    variable_name = func_by_name(pt[2][0], pt[2], scope)[1]
    value = func_by_name(pt[4][0], pt[4], scope)
    scope[variable_name] = value
    print(">>>>>>>>>>>>>>>>>>>>>>\n>>>>>>>", scope)
    #return print("\n\n\n\n\n\nvarNAMEMEMEMEMEMMEME,", varName)
    '''
# <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
def MultipleAssignment0(pt, scope):
    #1. Get list of variable names
    print("\nRetrieving variable names")
    var_Names =  func_by_name(pt[2][0], pt[2], scope)
    pp.pprint(pt[4])
    #2. Get the values returned from the fuction call
    print("\nGetting values returned from function Call")
    funcCall_values = func_by_name(pt[4][0], pt[4], scope)
    print("FuncCall_Values", funcCall_values)
    i = 0
    #Bonus: error if any name already exists in scope -- no rebinding
    while i < len(funcCall_values):
        scope[var_Names[i]] = funcCall_values[i]
        i += 1
    print("\n\n\n\n\n\n\n\n:")
    pp.pprint(scope)
    #Bonus: error if the number of variable names does not match the number of values


# <Print> -> PRINT <Expression>
def Print0(pt, scope):
    print("\nPrint0 printing the result of func_by_name() with arg[0] --->",
    pt[2][0], "\narg[2] as tree:")
    pp.pprint(pt[2])
    '''
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    print(">>>>>>>>>>>>>>>>>>>>>>", func_by_name(pt[2][0], pt[2], scope))
    '''
    print(str(func_by_name(pt[2][0], pt[2], scope)))

# <NameList> -> <Name> COMMA <NameList> | <Name>
def NameList0(pt, scope):
    print("Looking to return value from pt[1]:")
    pp.pprint(pt[1])
    param_name = func_by_name(pt[1][0], pt[1], scope)[1]
    print("[param_name]", [param_name])
    pp.pprint(pt[3])
    return [param_name] + func_by_name(pt[3][0], pt[3], scope)

def NameList1(pt, scope):
    #getting the [1] of the return value for name as it returns a [val, name]
    print("\nNameList1 returning the result of func_by_name() with arg[0] --->",
    pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    return [func_by_name(pt[1][0], pt[1], scope)[1]]

# <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
#should return a a list of values.
def ParameterList0(pt, scope):
    print("\nParameterList0 returning func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    param = func_by_name(pt[1][0], pt[1], scope)
    return [param] + [func_by_name(pt[3][0], pt[3], scope)]


def ParameterList1(pt, scope):
    print("\ParameterList1 returning func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope)

# <Parameter> -> <Expression> | <Name>
def Parameter0(pt, scope):
    print("\nParameter0 returning func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope)

def Parameter1(pt, scope):
    #pull value out of [value,name]
    return func_by_name(pt[1][0], pt[1], scope)[0]

#<Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
def Expression0(pt, scope):
    #<Term> ADD <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    print("\n\nleft_value {0} + right_value {1}".format(left_value, right_value))
    return left_value + right_value

def Expression1(pt, scope):
    #<Term> SUB <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    print("\n\nleft_value {0} - right_value {1}".format(left_value, right_value))
    return (left_value) - (right_value)

def Expression2(pt, scope):
    print("\nExpression2 returning func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope)

#<Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
def Term0(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    print("\n\nleft_value {0} * right_value {1}".format(left_value, right_value))
    return left_value * right_value

def Term1(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    print("\n\nleft_value {0} / right_value {1}".format(left_value, right_value))
    return left_value / right_value

def Term2(pt, scope):
    print("\nTerm2 sending func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope)

#<Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>
def Factor0(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    print("\n\nleft_value {0} ** right_value {1}".format(left_value, right_value))
    return left_value ** right_value

def Factor1(pt, scope):
    print("\nFactor1 returning the first value to func_by_name() from --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope, scope)

def Factor2(pt, scope):
    #returns multiple values -- use the first by default.
    print("\nFactor2 returning the first value to func_by_name() from --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope, scope)#[0]

def Factor3(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    print("\n\nleft_value {0} ** right_value {1}".format(left_value, right_value))
    return left_value ** right_value

def Factor4(pt, scope):
    print("\nFactor4 returning func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope)

#<FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>
def FunctionCall0(pt, scope):
    '''
    This is the most complex part of the interpreter as it involves executing a
    a partial parsetree that is not its direct child.
    1. Get the function name.
    2. Retrieve the stored function information from scope.
    3. Make a new scope with old scope as __parent__
    4. Get the list of parameter values.
    5. Bind parameter names to parameter values in the new function scope.
    6. Run the FunctionBody subtree that is part of the stored function information.
    7. Get the index return number.
    8. Return one value from the list of return values that corresponds to the index number.
    Bonus: Flag an error if the index value is greater than the number of values returned by the function body.
    '''

    print("getting the function name")
    funcName = get_name_from_ident(pt[1][1])
    stored_Func_pt = scope[funcName]
    print("Stored function information -->", stored_Func_pt)
    new_scope = {"__parent__" : scope}
    print("New Scope -->")
    pp.pprint(new_scope)
    get_params_vals = func_by_name(pt[3][0], pt[3], scope)
    print("List of param vals -->", get_params_vals)
    if type(get_params_vals) == float:
        new_scope[stored_Func_pt[0][0]] = get_params_vals
        print("\nThis is your functioncall's scope!")
        pp.pprint(new_scope)
    else:
        i = 0
        while i < len(get_params_vals):
            new_scope[stored_Func_pt[0][i]] = get_params_vals[i]
            i += 1
        print("\nThis is your functioncall's scope!")
        pp.pprint(new_scope)
    # 6
    function_body_pt = (lookup_in_scope_stack(funcName, scope))[1]
    print("\nThis is your functionCall's functionbody:")
    pp.pprint(function_body_pt)
    list_of_vals = func_by_name(function_body_pt[0], function_body_pt, new_scope)

    #7
    index_return_number = int(func_by_name(pt[5][0], pt[5], new_scope))
    #8

    return list_of_vals[index_return_number - 1]

def FunctionCall1(pt, scope):

    # 1. Get the function name.
    print("\n\ngetting the function name")
    funcName = get_name_from_ident(pt[1][1])
    print("FuncName -->", funcName)
    # 2. Retrieve the stored function information from scope.
    stored_Func_pt = scope[funcName]
    print("Stored function information -->", stored_Func_pt)
    # 3. Make a new scope with old scope as __parent__
    new_scope = {"__parent__" : scope}
    print("New Scope -->")
    pp.pprint(new_scope)
    # 4. Get the list of parameter values.
    get_params_vals = func_by_name(pt[3][0], pt[3], scope)
    print("List of param vals -->", get_params_vals)
    # 5. Bind parameter names to parameter values in the new function scope.
    i = 0
    while i < len(get_params_vals):
        new_scope[stored_Func_pt[0][i]] = get_params_vals[i]
        i += 1
    print("\nThis is your functioncall's scope!")
    pp.pprint(new_scope)
    # 6. Run the FunctionBody subtree that is part of the stored function information.
    function_body_pt = (lookup_in_scope_stack(funcName, scope))[1]
    print("\nThis is your functionCall's functionbody:")
    pp.pprint(function_body_pt)
    list_of_vals = func_by_name(function_body_pt[0], function_body_pt, new_scope)
    print("\n\n List of values returned from FunctionCall1:", list_of_vals)
    # 7. Return the list of values generated by the <FunctionBody>
    return func_by_name(function_body_pt[0], function_body_pt, new_scope)
'''
This is the most complex part of the interpreter as it involves executing a
a partial parsetree that is not its direct child.
1. Get the function name. <
2. Retrieve the stored function information from scope. <
3. Make a new scope with old scope as __parent__ <
4. Get the list of parameter values. <
5. Bind parameter names to parameter values in the new function scope. <
6. Run the FunctionBody subtree that is part of the stored function information.
7. Return the list of values generated by the <FunctionBody>
'''

#<FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
def FunctionCallParams0(pt, scope):
    print("\nFunctionCallParams0 returning to func_by_name() from --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope)

def FunctionCallParams1(pt, scope):
    return[]

#<SubExpression> -> LPAREN <Expression> RPAREN
def SubExpression0(pt, scope):
    print("\nSubExpression0 returning to func_by_name() from --->", pt[2][0], "\narg[2] as tree:")
    pp.pprint(pt[2])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[2][0], pt[2], scope)

#<Value> -> <Name> | <Number>
def Value0(pt, scope):
    print("\nValue0 returning func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    print("\n\n Result of running Name", func_by_name(pt[1][0], pt[1], scope))
    return func_by_name(pt[1][0], pt[1], scope)[0] #changed to 1 instead of 0

def Value1(pt, scope):
    print("\nValue1 returning func_by_name() this arg[0] --->", pt[1][0], "\narg[2] as tree:")
    pp.pprint(pt[1])
    print("arg[3] as scope ", scope)
    print("         Calling for func_by_name() with above params\n")
    return func_by_name(pt[1][0], pt[1], scope)

#<Name> -> IDENT | SUB IDENT | ADD IDENT
def Name0(pt, scope):
    name = get_name_from_ident(pt[1])
    print("Name > ", name)
    print("")
    return [lookup_in_scope_stack(name, scope), name]

def Name1(pt, scope):
    name = get_name_from_ident(pt[2])
    return [-lookup_in_scope_stack(name, scope), name]

def Name2(pt, scope):
    name = get_name_from_ident(pt[2])
    return [lookup_in_scope_stack(name, scope), name]

#<Number> -> NUMBER | SUB NUMBER | ADD NUMBER
def Number0(pt, scope):
    return get_number_from_ident(pt[1])

def Number1(pt, scope):
    return (-(get_number_from_ident(pt[2])))

def Number2(pt, scope):
    return get_number_from_ident(pt[2])

if __name__ == '__main__':
    '''
    string_from_parser = sys.stdin.read()
    tree = json.loads(string_from_parser)
    pp.pprint(tree)
    '''
    #choose a parse tree and initial scope
    #tree = tree_with_function_call
    tree = tree_with_function_call
    scope = {}
    #execute the program starting at the top of the tree
    func_by_name(tree[0], tree, scope)
    '''
    #Uncomment to see the final scope after the program has executed.
    print("\nThis is scope?\n")
    pp.pprint(scope)
    print("results: " + str(func_by_name(tree[0], tree, scope)))
    '''
