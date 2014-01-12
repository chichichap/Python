from cspbase import *
#from test_boards import *

def enforce_gac(constraint_list):
    '''Input a list of constraint objects, each representing a constraint, then enforce GAC on them, pruning values from the variables in the scope of these constraints. 
       if a DWO is detected, return False. else return True. 
       
       The pruned values will be removed from the variable object cur_domain. 
       enforce_gac modifies the variable objects that are in the scope of the constraints passed to it.'''

#<<<your implementation of enforce_gac below
    GACQueue = list(constraint_list)
    constraint_list2 = []
    
    while GACQueue:
        constraint = GACQueue.pop(0)
        constraint_list2.append(constraint) # list of constraints currently not in GACQueue

        for var in constraint.scope:
            for val in var.cur_domain():
                if constraint.has_support(var, val):
                    continue
                
                # Assignment not found
                var.prune_value(val)
                if not var.cur_domain():  
                    return False #DWO
                else:
                    remove_list = []
                    i = 0
                    for other_constraint in constraint_list2:
                        if var in other_constraint.scope: 
                            GACQueue.append(other_constraint)
                            remove_list.append(i)
                        i = i+1
                            
                    for j in remove_list[::-1]: # remove from top to bottom; otherwise invalid index error
                        constraint_list2.pop(j)

    return True # loop done without DWO 
#>>>your implementation of enforce_gac above

def create_variables( initial_sudoku_board ):
    ''' create a matrix of variables given the board '''
    var_matrix = []
    
    for r in range(0,9):
        row = initial_sudoku_board[r]
        
        var_list = []              
        for c in range(0,9):
            col = row[c]
            name = "R" + str(r) + "C" + str(c) 
            
            if col == 0: var_list.append( Variable(name, [1,2,3,4,5,6,7,8,9]) )
            else:        var_list.append( Variable(name, [col]) )

        var_matrix.append(var_list) 
    return var_matrix

def create_constraints( var_list ):
    ''' create NOT-EQUAL constraints over 2 of the 9 variables in the list '''
    constraint_list = []
    
    for i in range(0,8):
        for j in range(i+1,9):
            constraint = Constraint(var_list[i].name + " " + var_list[j].name, [var_list[i], var_list[j]])
            
            satisfying_tuples = []
            for val1 in var_list[i].cur_domain():
                for val2 in var_list[j].cur_domain():
                    if val1 != val2:
                        satisfying_tuples.append([val1, val2])
            
            constraint.add_satisfying_tuples( satisfying_tuples ) 
            constraint_list.append( constraint )    
        
    return constraint_list

def get_results( var_matrix ):
    ''' get the domains of the variables in the matrix '''
    results = []
    
    for r in range(0,9): 
        row_result = []
        for var in var_matrix[r]:
            row_result.append(var.cur_domain())
        results.append(row_result)    
        
    return results
                            
def sudoku_enforce_gac_model_1(initial_sudoku_board):
    '''The input board is specified as a list of 9 lists. Each of the 9 lists represents a row of the board. 
            if a 0 is in the list, it represents an empty cell. 
       Else if a number between 1--9 is in the list, it represents a pre-set board position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       In model_1 you should create a variable for each cell of the board, with domain equal to {1-9} if the board has a 0 at that position, 
                                                                            and domain equal to {i}   if the board has a fixed number i at that cell. 
       
       Model_1 should create BINARY CONSTRAINTS OF NOT-EQUAL between all relevant variables (all pairs of variables in the same row), then invoke enforce_gac on those constraints. 
       All constraints of Model_1 MUST BE binary constraints (constraints whose scope includes exactly two variables).
       
       This function outputs the GAC consistent domains after enforce_gac has been run. 
       The output is a list with the same layout as the input list: a list of nine lists each representing a row of the board. 
       However, now the numbers in the positions of the input list are to be replaced by LISTS which are the corresponding cell's pruned domain (current domain) AFTER GAC has been performed.
       
       For example, if GAC failed to prune any values the output from the above input would result in, an output would be: 
       (I PADDED OUT ALL OF THE LISTS WITH BLANKS SO THAT THEY LINE UP IN TO COLUMNS. Python would not output this list of list in this format.)
       
       
       [[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8]],
       [[1,2,3,4,5,6,7,8,9],[                7],[1,2,3,4,5,6,7,8,9],[                4],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3]],
       [[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9],[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6]],
       [[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                5],[                7],[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9]],
       [[                6],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]]
       
       Of course, GAC would prune some variable domains so this would not be the output list.
    '''

#<<<your implementation of model_1  below
    constraint_list = []

# step 1: create a list of variables
    var_matrix = create_variables( initial_sudoku_board )
         
# step 2A: create row constraints
    for r in range(0,9):    
        var_list = var_matrix[r]         
        constraint_list = constraint_list + create_constraints( var_list )   
        
# step 2B: create column constraints
    for c in range(0,9):
        var_list = tuple(r[c] for r in var_matrix)    
        constraint_list = constraint_list + create_constraints( var_list )   
        
# step 2C: create sub-square constraints
    for r in range(0,3):
        for c in range(0,3):
            var_list = [var_matrix[r*3   ][c*3], var_matrix[r*3   ][c*3 +1], var_matrix[r*3   ][c*3 +2],
                        var_matrix[r*3 +1][c*3], var_matrix[r*3 +1][c*3 +1], var_matrix[r*3 +1][c*3 +2],
                        var_matrix[r*3 +2][c*3], var_matrix[r*3 +2][c*3 +1], var_matrix[r*3 +2][c*3 +2]]
                            
            constraint_list = constraint_list + create_constraints( var_list )
        
# step 3: enforce GAC and return the pruned domains
    enforce_gac(constraint_list)  
    return get_results( var_matrix ) 
#>>>your implementation of model_1 above

def create_constraint(name, var_list):
    ''' create a constraint over 9 variables in the list '''
    constraint = Constraint(name, var_list)
          
    satisfying_tuples = []
    t = []
        
    create_satisfying_tuples(var_list, t, satisfying_tuples)
   
    constraint.add_satisfying_tuples( satisfying_tuples ) 
    return constraint

def create_satisfying_tuples(var_list, t, satisfying_tuples):
    ''' create satisfying tuples based on the current variable domains '''
    i = len(t)
    
    for val in var_list[i].cur_domain():
        if val in t: continue
        
        t.append(val)  
        if i < 8:
            create_satisfying_tuples(var_list, t, satisfying_tuples)
        else:
            satisfying_tuples.append(list(t))          
        t.pop()

##############################

def sudoku_enforce_gac_model_2(initial_sudoku_board):
    '''This function takes the same input format (a list of 9 lists specifying the board, and generates the same format output as sudoku_enforce_gac_model_1.
    
    variables of model_2 are the same as for model_1: a variable for each cell, with domain {1-9} if the board has a 0 at that position, and domain {i} if the board has a fixed number i at that cell.

    model_2 has different constraints. Instead of binary non-equals constraints, model_2 has 27 all-different constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. 
    
    Each of these constraints is over 9-variables (some of these variables will have a single value in their domain). 
    model_2 should create these all-different constraints between the relevant variables, invoke enforce_gac on those constraints, and then output the list of gac consistent variable domains in the same format.
    '''
#<<<your implementation of model_2  below
    constraint_list = []

# step 1: create a list of variables
    var_matrix = create_variables( initial_sudoku_board )   
        
# step 2A: create row constraints
    for r in range(0,9):    
        var_list = var_matrix[r]         
        constraint_list.append( create_constraint("R"+ str(r), var_list) )
              
# step 2B: create column constraints
    for c in range(0,9):
        var_list = tuple(r[c] for r in var_matrix)            
        constraint_list.append( create_constraint("C"+ str(c), var_list) )
        
# step 2C: create sub-square constraints
    for r in range(0,3):
        for c in range(0,3):
            var_list = [var_matrix[r*3   ][c*3], var_matrix[r*3   ][c*3 +1], var_matrix[r*3   ][c*3 +2],
                        var_matrix[r*3 +1][c*3], var_matrix[r*3 +1][c*3 +1], var_matrix[r*3 +1][c*3 +2],
                        var_matrix[r*3 +2][c*3], var_matrix[r*3 +2][c*3 +1], var_matrix[r*3 +2][c*3 +2]]
                            
            constraint_list.append( create_constraint("subR" + str(r) + "C"+ str(c), var_list) )
            
# step 3: enforce GAC and return the pruned domains
    enforce_gac(constraint_list)  
    return get_results( var_matrix ) 
#>>>your implementation of model_2 above

# for testing only
# for b in boards:
#     print "Solution from MODEL 1"
#     sol1 = sudoku_enforce_gac_model_1(b)
#     for row in sol1:
#         print row
#     print "Solution from MODEL 2"
#     sol2 = sudoku_enforce_gac_model_2(b)
#     for row in sol2:
#        print row