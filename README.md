Automatic Differentiation
=========================

**This is a differentiation algorithm created by Loan Tricot and Simon Dupouy in Pyhton 3.**

*differentiate.py* differentiates any expression.  
*simplify.py* does *very* basic simplifications. It is used to simplify a bit the differentiated expressions.

differentiation
---------------
This algorithm views an expression as a tree. Each leaf-node is a number or a variable (x), and all the
other nodes are values resulting of the basic operation (+-/\*) made on each of their two sub-nodes.
For example:
![treeExample]()

simplification
--------------
The algorithm takes a tree defined by its first node. It then recursively browses the tree by exploring
separately the left and the right sub-tree each time.
The algorithm for the moment makes the following simplifications:
- x + 0 = x
- a + b = a+b *(calculation)*
- x \* 0 = 0
- x \* 1 = x
- a \* b = ab *(calculation)*
- 0 / x = 0
- x / 1 = x
- x / x = 1

This program will be extended to develop and further simplify expressions, as well as work with power
notations (x^a).  
We will also try to implement it using regular expressions (RegExp).
