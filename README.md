#Personalized data
The code might not run while using the command "python" due to the presence of the "copy()" function. If it does not run, python3 NQueens.py ALG N CFile RFile would work.

#Important Information
All the code was run from a personal linux computer using the python version 3.6.
While trying to run on a similar VCL image, it was found that "python Search.py <ALG> <FILE>" had problems in execution and "python3 Search.py <ALG> <FILE>" ran correctly (specifying the python version explicitly while running on some systems)

#Description
The code to develop a forward checking and Consistance maintaining algorithm for solving the N-Queen Puzzle. This is written and compiled in Python3. It is available in the file NQueens.py. Three two algoritms have been used to determine the permutations. Namely Forward checking algorithms and Maintaining Arc Consistancy algorithm

#Implementation
For this problem I have develop a python package that is called as follows:
NQueens.py ALG N CFile RFile
where: ALG is one of FOR or MAC representing Backtracking search with forward checking or Maintaining
Arc Consistency respectively. N represents the number of rows and columns in the chessboard as well as the
number of queens to be assigned. CFile is an output filename for your constraint problem. And RFile is an
output file for my results.

#Results
Similar results were obtained for both the algorithms however, the runtime of the MAC algorithm was considerably higher.

#Issues
For larger constraint spaces, the algorithm takes a longer time to check if a queen can be placed in the next position and it also takes a little more time to update the domain and constraints in each step.
