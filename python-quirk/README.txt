Pol Ajazi

CSC 521 - Python Quirk Language Implementation

In order to run the project through BASH, locate the directory of this file in your
terminal and simply type:
		
	'python lexer.py < "filenamehere"| python parser.py | python interpreter.py'
	
	replacing "filenamehere" with your specific file.
	
	An example of actual input would look like this:
	
	'python lexer.py < example1 | python parser.py | python interpreter.py'
	
	as also seen in the output examples 1-5.
	
I have included files example1 through example5 for easy testing of my program.
To discover how each part of the implementation works, read the comments at the top
and through the body of the code in each of the scripts: lexer.py, parser.py and 
interpreter.py.

Finally, I have also includede a folder named 'Scripts with heavy debugging code' which
contains the standalone version of the partial parser similar to the one provided by the
professor, heavily emebded with print statement in order to understand the interpretation.
Also incudluded is a standalone version of the interpreter heavily embeded with print 
statements as well, showing the entirity of the tree unrwarping and the functionality of
the entire final program. 

Notes and comments:

	* The tree in the parse tree will sometimes take longer than it needs to get to the 
	a terminal because some non-terminal nodes also lead to the answer through a longer 
	route. This could be easily fixable by changing the order in which the nodes are 
	processed, however it would lead to longer processing times for currently corrent 
	pathing tokens. 
	
	* The interpreter will have difficulty printing the result of multiple Expressions in 
	a row. For example print 4+2-7+9 would actually result to  4+[2-[7+9]] which will
	result to 10, as oposed to the mathematically correct 8 because the implementation 
	always forces rightmost processing. I am not sure fix a problem like this without
	changing the implementation of the parser as well as the interpreter.
	
	* In the current implementation, FunctionCall0 of the intrpreter will work correctly
	only for the call of the first return index because: 
	foofunc(){return 1, return 2, return 3} will actually return [1, [2, 3]]. This 
	is easily fixable by implementing an unrwaping class.
