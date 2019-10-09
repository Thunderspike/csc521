# csc521
Compiler for the Quirk computer language, written in Python and partly replicated in Clojure

This project was composed as part of the CSC521 course - Design & Organization of Programing Languages - at American University (Spring 2017). 

In Python, this project makes use of three main functions, the lexer, the parser and the interpreter.
In Clojure, this project is only composed of the interpreter, as Clojure has easy access to parsing functionality (through its Instaparse dependency)



Below is the formal syntax for the 'Quirk' programming language:

--------------------------------------------------------------------------------------------------------------------------------------

Program := Statement Program | Statement                                                          
Statement := FunctionDeclaration | Assignment | Print                                             
FunctionDeclaration :=  FUNCTION Name LPAREN FunctionParams LBRACE FunctionBody RBRACE            
FunctionParams := NameList RPAREN | RPAREN                                                        
FunctionBody := Program Return | Return                                                           
Return := RETURN ParameterList                                                                    
Assignment := SingleAssignment | MultipleAssignment                  
SingleAssignment := VAR Name ASSIGN Expression                                                    
MultipleAssignment := VAR NameList ASSIGN FunctionCall                                                                              
Print:= PRINT Expression  
NameList := Name COMMA NameList | Name  
ParameterList:= Parameter COMMA ParameterList | Parameter                                                                       
Parameter := Expression | Name                                                                                                         
Expression := Term ADD Expressio  n | Term SUB Expression | Term                                      
Term := Factor MULT Term | Factor DIV Term | Factor                                                       
Factor := SubExpression EXP Factor | SubExpression | FunctionCall | Value EXP Factor | Value                      
FunctionCall :=  Name LPAREN FunctionCallParams COLON Num | Name LPAREN FunctionCallParams                          
FunctionCallParams :=  ParameterList RPAREN | RPAREN                                                        
SubExpression := LPAREN Expression RPAREN                                                               
Value := Name | Num                                                         
Name := IDENT | SUB IDENT | ADD IDENT                                                       
Num := NUMBER | SUB NUMBER | ADD NUMBER                                                                                 
VAR := #"var"*                                                                                                                          
FUNCTION := #"function"                                                                                                          
RETURN := #"return"                                                                                                                    
PRINT := #"print"                                                                                                           
ASSIGN := #"\="                                                                                                               
ADD := #"\+"                                                                                                                      
SUB := #"\-"                                                                                                            
MULT := #"\* "                                                                                                                      
DIV := #"\/"                                                                                                                      
EXP := #"\^"                                                                                                                  
LPAREN := #"\("                                                                                                                   
RPAREN := #"\)"                                                                                                                     
LBRACE := #"\{"                                                                                                                   
RBRACE := #"\}"                                                                                                       
COMMA := #"\,"                                                                                                              
COLON := #"\:"                                                                                                                  
NUMBER:= #"((\d+(\.\d*)?)|(\.\d+))"                                                                                           
IDENT := #"[a-zA-Z]+[a-zA-Z0-9_]*"    

--------------------------------------------------------------------------------------------------------------------------------------
