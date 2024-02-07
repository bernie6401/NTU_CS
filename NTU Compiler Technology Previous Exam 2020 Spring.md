# NTU Compiler Technology Previous Exam 2020 Spring
###### tags: `NTU_CT` `NTU` `Compiler Techonology of Programming Language` `Final Exam`

1. According to the grammar of AC in the right , please write down the recursive descent parsing procedure for nonterminal Expr. (10 points/10)
![](https://imgur.com/fIUehwA.png)

2. Please write down a regular expression that defines the set of strings recognized by the FA in the following and explain your answer (5points/ 15)
![](https://imgur.com/oWs2kC0.png)

3. Please write down a `DFA` recognizing the tokens defined by the following regular expression and explain your answer (5 points/20)
![](https://imgur.com/SDEdOWl.png)

4. Please write down a regular expression that defines C-like comments delimited by /* and */. Individual *’s and /’s may appear in the comment body, but the pair */ may not. (5 points/ 25)

5. Consider the ac grammar in question 1 . 
5a. Please write down the value of First(`Stmts`)! ( 2 points/ 27)
5b. Please write down the value of First(`Stmt`)! ( 2 points/ 29)
5c. Please write down the value of First(`Expr`)! ( 2 points/ 31)
5d. Please write down the value of Follow(`Stmts`)! ( 2 points/ 33)
5e. Please write down the value of Follow(`Expr`)! ( 2 points/ 35)

6. Please explain the technology of recursive descent LL(1) parsers. There is no standard answer to this question. But the points you get depend on our evaluation of the depth of your correct understanding of the technology purely based on to your answer below. (10points/45)

7. Please write down a grammar that cannot be parsed by LL(0) while can be by LR(0) and explain why. (5points/50)

8. Please write down a grammar that cannot be parsed by LR(0) while can be by SLR(1) and explain why . (5points/ 55 )

9. Consider the program fragment in the right. The typedef establishes Pair Name as a typename,defined as a pointer to a record of two integers with its name . The declaration for p p s uses the type name, but adds one more level of indirection to an array of $23x48$ PairNames. Please draw a diagram of the symbol table entries, attribute descriptors, and type descriptors that would result from processing the declarations.(10 points 65 )

10. Please explain the algorithm of Sethi-Ullman/Ershov Numbering for register allocation in compiler technology. (5point s /70)

11. P lease writ e down an abstract syntax tree (`AST`) that needs 4 registers to calculate according to the Sethi-Ullman/Ershov Numbering algorithm. You need explain why 4 registers are needed.(5points/ 75)

12. Please explain GCD test in generating parallel machine code f or multi core machines .(5points/80)

13. Please explain the Virtual Assistant Programming Language (`VAPL`) ThingTalk in the Almond project of Stanford University. What are the new challenges in processing ThingTalk programs compared to traditional programming languages ? (Ref: Genie: A Generator of Natural Language Semantic Parsers for Virtual Assistant Commands ”, `PLDI` 2019) (5 points/ 85)

14. Please explain how compiler technology can help in pruning Convolutional Neural Network (CNN) (Ref: "*Wootz: A Compiler Based Framework for Fast CNN Pruning via Composability*", `PLDI` 2019) (5 points/90)

15. What is the technology of string solver mentioned in the 2019 `PLDI` paper: "*Computing Summaries of String Loops in C for Better Testing and Refactoring*"? (5points/95)

16. P lease explain how machine learning technology can be used to improve the trade off between machine code performance and power consumption of compilers. (Ref: "*Generative and Multi phase Learning for Computer Systems Optimization* ", `ISCA` (5points/100)