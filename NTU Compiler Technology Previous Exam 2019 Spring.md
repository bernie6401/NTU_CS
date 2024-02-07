# NTU Compiler Technology Previous Exam 2019 Spring
###### tags: `NTU_CT` `NTU` `Compiler Techonology of Programming Language` `Final Exam`

1. Please explain three different compiler optimization techniques :
(a) 1st compiler optimization technique: (5points/5)
(b) 2nd compiler optimization technique: (5points/10)
(c) 3rd compiler optimization techniques: (5points/15)

2. Many computer systems provide an interactive debugger (for example, `gdb` or db x) to assist users in diagnosing and correcting runtime errors. Although a debugger is run long after a compiler has done its job, the two tools still must cooperate. What information (beyond the translation of a program) must a compiler supply to support effective runtime debugging? (5 points/20)


3. Sometimes it is necessary to modify the syntax of a programming language. This is done by changing the `CFG` that the language uses. Consider the `CFG` of the AC language in the class shown in the right . Please show how to change AC’s `CFG` to implement the if-then-else statement structure with unbounded structural induction? (10points/30)
![](https://imgur.com/hhDGOmm.png)

4. Please write regular expressions that define the strings recognized by the FA in the following. (5points/35)
![](https://imgur.com/kbYNf94.png)

5. Please write a `DFA` recognizing the tokens defined by the following regular expression (5points/40)
![](https://imgur.com/QVZGdkQ.png)

6. In Chapter 4, a bout the top down parsing technology, consider a non terminal A and a string $\alpha$ of terminals and non terminals.
(6a) Please explain First($\alpha$) (2points/42)
(6b) What is the use of First($\alpha$) (3points/45)
(6c) Please explain Follow(A) (2points/47)
(6d) Please explain the use of Follow(A) (3points/50)

7. Consider the grammar in the right Please explain why it cannot be parsed by LL(1) parser while can be by LL(2). (5 points 55)
![](https://imgur.com/lIdGVTC.png)

8. Please draw the `CFSM` of LR parsing for the grammar in the right. (10 points/65)
![](https://imgur.com/cxsfYYj.png)

9. The grammar in the right generates nested lists of numbers. Th e semantic actions are intended to count the number of elements just inside each parenthesized list. For each list found by Rule 2, Marker 44 prints out the number of elements found just inside the list. For example, the input ( ( 1 2 3 ) ( 1 2 3 4 5 6 )) should print 3, 6, and 2. The grammar uses a global variable count to determine the number o f elements in a list. P lease answer the following.
(a) What is wrong with that approach? (5points/70)
(b) Change the semantic actions so that the appropriate values are synthesized by the rules to allow counting without a global variable. (5points/75)
![](https://imgur.com/Q203Cbc.png)

10. Consider the program fragment in the right. The typedef establishes Pair as a typename, defined as a pointer to a record of two integers. The declaration for pairs uses the type name, but adds one more level of indirection to an array of 23 Pairs. P lease d raw a diagram of the symbol table entries, attribute descriptors, and type descriptors that would result from processing the declarations . (10 points /85)
![](https://imgur.com/HuseBl6.png)

11. Assume we add a new option to C++ arrays that are heap allocated, the flex option. A flex array is automatically expanded in size if an index beyond the array’s current upper limit is accessed. Thus we might see: 

    $ar = new flex int[10]; ar[20] = 10;$ 

    The assignment to position 20 in ar forces an expansion of ar’s heap allocation. Explain what changes would be needed in array accessing to implement flex arrays. Especially, please explain w hat should happen if an array position beyond an array’s current upper limit is read rather than written? (5points/90)

12. Local variables are normally allocated within a frame, providing for automatic allocation and deallocation when a frame is pushed and popped.
(a) Under what circumstance must a local variable be dynamically allocated? (4points/89)
(b) Are there any advantages to allocating a local variable statically (i.e., giving it a single fixed address)? 3points/92)
(c) Under what circumstances is static allocation for a local permissible? (3 points /95)