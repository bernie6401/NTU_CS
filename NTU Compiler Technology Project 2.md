# NTU Compiler Technology Project 2
###### tags: `NTU_CT` `NTU` `Compiler Techonology of Programming Language` `Scanner`
:::spoiler
[TOC]
:::
## Objective

This is compiler project 2 that aim to construct the scanner by handmade with some sample code. The output is symbol table that the frequency of each identifier and the result is sorted.

## Run and Test

```bash
$ make /*use make in src folder*/
$ ./scanner ../test/sample1.ac
```

## Output of each sample
* For sample1.ac
    ```bash
    /* 1: this is just a sample */
    /* 2: this is a 3-line
        comment
        */
    /* 3: this is /* the end ***/
    Frequency of identifiers:
    a			3 
    b			2 
    c			3 
    d			4 
    e			1 
    f			2 
    func		2 
    g			2 
    main		3 
    read		1 
    write		1 
    ```
    
* For sample2.ac

    ```
    Frequency of identifiers:
    loopvar		6 
    main		1 
    n			3 
    read		1 
    sum			5 
    write		3
    ```

* For sample3.ac

  ```
  Frequency of identifiers:
  fact		3 
  main		1 
  n			9 
  read		1 
  result		4 
  write		3
  ```

* For sample4.ac

    ```
    /* 1: this is * just a / sample */
    /* 2: this is a 3-line
    	comment
    	*/
    /* 3: this is /* the end ***/
    Frequency of identifiers:
    a1			1 
    abc			4 
    b1			1 
    def			3 
    main		1 
    main_1		1 
    n			3 
    read		1 
    write		2 
    z_123_x_45	1
    ```

## Reference

* [simple intro of lex](http://falldog7.blogspot.com/2007/09/lex.html)
* [line comment & block comment implementation](https://www.zhihu.com/question/30108800)
* [regular expression cheat sheet](https://ithelp.ithome.com.tw/articles/10222163)
* [solve: warning, rule cannot be matched](https://www.ptt.cc/bbs/RegExp/M.1320578122.A.658.html)
* [simple lex example](https://www.geeksforgeeks.org/lex-code-to-count-total-number-of-tokens/)
* [previous homework by other people](https://github.com/liuxt/Compiler/tree/master/hw2)

* [strcmp in c](https://www.programiz.com/c-programming/library-function/string.h/strcmp)