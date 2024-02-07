# NTU Compiler Technology Project 1
###### tags: `NTU_CT` `NTU` `Compiler Techonology of Programming Language`

## AcDc Compiler
## Description
* This is a project from NTU (National Taiwan University) course, Compiler Technology of Programming Language.
* First project is aim to 
	* add multiplier and division operation in this compiler
	* let compiler can recognize multi character identifier(variable) name by alphabet string
	* use constant folding to optimize the statement
## How to use?
* You can browse Assignment1.pdf. You must run in Linux OS environment(more conveniently). When you finish the coding, use `$ make` command directly.
* `$ ./AcDc <input sample address> <output file address>`
	* For instance: `$ ./AcDc ../test/sample1.ac ./output`
## Something need to know first
* It can not recognize the bottom line as identifier name.
* It can not print negative value like $1-2=-1$ expression. Actually speaking, it can calculate correctly but it can not print it out.(I'll check it out later.)
	* You can check [constfold testbench](/test/constfold.ac)
	* Solution and Why: In Dc Language, the bottom line represent negative symbol. You can not just use minus as negative symbol, replace it by bottom line instead.
* It can not recognize identifier name with numbers. You can check [longname.ac](/test/longname.ac)
* The other testbenchs can compile from Ac language to Dc language correctly.

## Reference
* [AcDc](https://github.com/jaidTw/AcDc)
* [AcDcCompiler](https://github.com/ZephyrZhuQi/AcDcCompiler)