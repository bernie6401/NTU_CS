# NTU Compiler Technology Project 3
###### tags: `NTU_CT` `NTU` `Compiler Techonology of Programming Language` `YACC` `Lex`

[TOC]

## Objective
* The main task for this project is to revise `src/parser.y` and generate `parser` file properly to compile test code in `test` folder.
* And then use `Graphviz` command to visualize the structure of these test code


## How to run?
* Just use `make` to compile all files in `/src`. Though you'll get a lots of warning shown as below, you can ignore them and obtain the target file `parser`.
    ```bash=
    bison -v -d parser.y
    parser.y: warning: 1 shift/reduce conflict [-Wconflicts-sr]
    flex lexer.l
    gcc -g -c alloc.c
    gcc -g -c parser.tab.c
    parser.tab.c: In function ‘yyparse’:
    parser.tab.c:2565:7: warning: implicit declaration of function ‘yyerror’; did you mean ‘yyerrok’? [-Wimplicit-function-declaration]
           yyerror (YY_("syntax error"));
           ^~~~~~~
           yyerrok
    parser.y: At top level:
    parser.y:825:3: warning: data definition has no type or storage class
       yydebug = 1;
       ^~~~~~~
    parser.y:825:3: warning: type defaults to ‘int’ in declaration of ‘yydebug’ [-Wimplicit-int]
    parser.y:827:1: warning: return type defaults to ‘int’ [-Wimplicit-int]
     main (argc, argv)
     ^~~~
    parser.y: In function ‘main’:
    parser.y:834:5: warning: implicit declaration of function ‘printGV’; did you mean ‘printf’? [-Wimplicit-function-declaration]
         printGV(prog, NULL);
         ^~~~~~~
         printf
    gcc -g -c functions.c
    gcc -g -o parser parser.tab.o alloc.o functions.o -lfl
    ```
* Use parser to compile all files in `/test` folder and you will get `AST_Graph.gv` in **`/test`** folder.
    **`/src`**
    ```bash=
    ./parser ../test/control.c
    dot -Tpng -o ../test/control.png ../test/AST_Graph.gv
    ./parser ../test/decl.c
    dot -Tpng -o ../test/decl.png ../test/AST_Graph.gv
    ./parser ../test/expr.c
    dot -Tpng -o ../test/expr.png ../test/AST_Graph.gv
    ./parser ../test/func.c
    dot -Tpng -o ../test/func.png ../test/AST_Graph.gv
    ```
* Note that in `parser.y`, I set `yydebug = 1` so that we can see the debug message from parser
    ```cpp=821
    #ifdef YYDEBUG
        yydebug = 1;
    #endif
    ```
## For TA
* I changed a little bit `functions.c` that will generate `AST_Graph.gv` at `test/` folder.
```cpp=150
void printGV(AST_NODE *root, char* fileName)
{
    if (fileName == NULL) {
        fileName = "../test/AST_Graph.gv";
    }
    ...
}
```
## Analysis
* You can see the relationship between structure map and test code by yourself.
* **control.c**
    ```cpp=
    int main()
    {
        int i;
        int p;
        int k, j;
        for (i=0; i<9; i=i+1) {
                /* empty */
        }
        for (i=0, p=4+4; i<9; i=i+1, p=i) {
            write("test");
        }
        for (;;) {
            /*empty*/
        }
        while (1) {
        }
        while (2) {
            write("haha");
            write("wow");
        }
        if (k == j) {
            write("first");
        }
        if (k == j) {
            write("first");
        } else if (j == k) {
            write("second");
        } else {
            write("third");
        }
    }
    ```
    ![graphviz of control.c](https://imgur.com/4zTAsML.png)
* **decl.c**
    ```cpp=
    typedef float GFLOAT;
    int main() {
        typedef int INT, INT2, INT3;
        typedef float FLOAT;
        typedef void VOID;
        typedef void VOID2, VOID3;
        INT f[3][3*3-(4+2)/2];
        FLOAT f2;
    }
    ```
    ![graphviz of decl.c](https://imgur.com/6KWV4IT.png)
* **expr.c**
    ```cpp=
    int fn1() {
        return 1;
    }
    float fn3() {
        return 1.0;
    }
    int fn4(int a, int b) {
        return 1;
    }
    int expr(int a, int b, int c, int d,
            float fa, float fb, float fc) {
        int i, j, k, l;
        float fi = 1.0, fj = 2.0, fk = 3.0, fl = 4.0;

        fi = 1.2*fi + -fj * (fl - fk * fn3());
        fi = -fn3() -(-(-(4)));
        fi = !fn3() -(!(!(4)));
        i = !fn1();
        i = 1 < 2;
        i = 1 > 2;
        i = 1 >= 2;
        i = 1 <= 2;
        i = 1 != 2;
        i = 1 == 2;
        i = fn4(1+3*4*fn4(2,3), 3);
        return 1;
    }
    int main() {
    }
    ```
    ![graphviz of expr.c](https://imgur.com/7a6OyJA.png)
* **func.c**
    ```cpp=
    int fn1() {
        int ABC = 5;
        return ABC+5;
    }
    void fn2() {
    }
    void fn3(int a, int b[3][4]) {
    }
    int main() {
        int b[4][4];
        fn1();
        fn2();
        fn3(2, b);
    }
    ```
    ![graphviz of func.c](https://imgur.com/BvW5b2U.png)

## Reference
[Github example](https://github.com/liuxt/Compiler/blob/master/hw3)
[Simple intro of yacc & lex](https://bluelove1968.pixnet.net/blog/post/222285652?utm_source=PIXNET&utm_medium=Blog_CollectionEXP_login)
[Simple intro of Graphviz](https://www.netadmin.com.tw/netadmin/zh-tw/technology/122966CB664D4A17ABAAD11FC2AA887C?page=3)
[A GUIDE TO LEX & YACC from TA](https://arcb.csc.ncsu.edu/~mueller/codeopt/codeopt00/y_man.pdf)
大推：[以lex/yacc實作算式計算機](https://good-ed.blogspot.com/2010/04/lexyacc.html)