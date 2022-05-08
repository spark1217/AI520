#### How to run Q1
Unzip the folder Q1
The test files must be in the same folder with python file('q1.py'). 'spark43_q1.py' is located inside Q1 folder.
The output will be saved in 'Q1/Solutions' folder, and the folder will be created if not already exists.

To run the program, run command:
python3 q1.py '<filename.txt>'
For example,
python3 q1.py case1.txt

The output can be checked in console too.


#### How to run Q2
Unzip the folder Q2.
Run the python file('spark43_q2.py'). 'q2.py' is located inside Q2 folder.
It will read Maze examples stored in Mazes/DFS or Mazes/Astar folder for each algorithm.
The output will be saved in 'Q2/Solutions/<algorithm>' folder, and the folder will be created if not already exists.

To run the program, run command:
python3 spark43_q2.py '<Maze filename>'.txt <bfs/dfs/astar>
For example, 
python3 q2.py Maze1.txt bfs
python3 q2.py Maze1.txt dfs
python3 q2.py Maze2.txt astar

The heuristic function used in scenario 2 is h(n) = sqrt((end_y - y)^2 + (end_x - x)^2).
This is consistent and admissible as h(n) value is always less than or equal to actual cost.

The expected output will show up in console too.
<output format in console in scenario 0.1>
Path expanding steps, the number of path expanding
<output format in console in scenario 0.2>
[[order of keys found], number of moves, [path]]