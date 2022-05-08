#### How to run Q1a
Unzip the folder Q1a
The test files must be in the same folder with python file('q1a.py'). 'q1a.py' is located inside Q1a folder.
The output will be saved in 'Q1a/Solutions/<algorithm>' folder, and the folder will be created if not already exists.

To run the program, run command:
python3 q1a.py <filename.txt> <hc/rr/rw>
For example,
python3 q1a.py Maze1.txt hc
python3 q1a.py Maze2.txt rr
python3 q1a.py Maze3.txt rw

It takes some time to complete some mazes. Please be patient though it is a bit slow.
In random walk senario, if it ends up 'Not possible', random/best movement is printed all history. Therefore, the result file may be too long.

For analysing maze 3 and maze 4 with p values [0.2, 0.4, 0.6, 0.8] and 15 iterations (step count), separate solution files called 'Maze3_solution_iter15.txt' and 'Maze4_solution_iter15.txt' are included. 

#### How to run Q1b
Unzip the folder Q1b.
Run the python file('q1b.py'). 'q1b.py' is located inside Q1b folder.
The output will be saved in 'Q1b/Solutions' folder, and the folder will be created if not already exists. The number of backtracking would be printed in console.

To run the program, run command:
python3 q1b.py <filename.txt> 
For example, 
python3 q1b.py Maze1.txt
