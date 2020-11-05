# -*- coding: utf-8 -*-
"""
EN.640.635 Software Carpentry
Lazor Project


def class Reflect:
    def call(self, lazor):
        if lazor[0] == -1:
            if lazor[1] == 1:
                new_lazor = (1, 1)
            else:
                new_lazor = (1, -1)
        if lazor[1] == 1:
            if lazor[0] == 1:
                new_lazor = (1, -1)
            else:
                new_lazor = (-1,-1)
        return(new_lazor)

def class Opaque:
    def call(self, lazor):
        lazor = (0, 0)
        return(lazor)

def class Refract:
    def call(self, lazor):
        lazor1 = lazor
        lazor2 = Reflect(lazor)
        return(lazor1, lazor2)

def generate_grid(input_name):
    '''
    Generate a maze using the Depth First Search method.

    *Parameters*

        input_name: BFF file to be read in

    *Returns*

        block_grid: list of lists
        lazor_grid: list of lists
        lazor: list of tuples
        blocks: list of tuples
    '''
    # Read in BFF file and create appropiate variables
    g_len, g_wid, fix, blocks, lazor, vp = read_lazor(input_name)

    # Create block grid
    block_grid = [
        [0 for i in range(g_wid * 2)]
        for j in range(g_len * 2)
    ]

    # Create lazor grid
    lazor_grid = [
        [0 for i in range(g_wid * 2 + 1)]
        for j in range(g_len * 2 + 1)
    ]

    # Create fixed blocks
    for block in fix:
        block_grid = add_block(block_grid, block, flag=1)

    # Create lazor grid
    for victory in vp:
        x, y = victory[0], victory[1]
        lazor_grid[x][y] = 1

    # Save starting grid for later use
    return block_grid, lazor_grid, lazor, blocks


def read_lazor(level_name):
    '''
    Reads in the lazor level name from a bff file.

    **Parameters**

        level_name: *str*
            The name of the lazor level

    **Returns**

        g_len: *int*
            Length of the lazor grid
        g_wid: *int*
            Width of the lazor grid
        fix: *str, int, int*
            A list of tuples holding the fixed blocks on the grid
            including their type and position
        opt: *str, int*
            A list of tuples holding the optional blocks that
            can be placed including type and number of them
        lazor: *list*
            A list of integers detailing the lazor starting
            position and how it moves
        vp: *list*
            A list of tuples detailing the coordinates of the
            victory points
    '''

    filename = level_name + ".bff"
    lazor_file = open(filename)

    lazor_list = lazor_file.readlines()

    #Initialize list of lazors
    lazor = []

    #Initialize list of VP's
    vp = []

    #Initialize list of optional blocks
    opt = []

    #Initialize list of fixed grid blocks
    fix = []

    start = lazor_list.index("GRID START\n")
    end = lazor_list.index("GRID STOP\n")

    #Iterate through list to find where the grid is defined
    for line in range(len(lazor_list)):
        # if "GRID START" in lazor_list[line]:
        #     start = line
        # if "GRID STOP" in lazor_list[line]:
        #     end = line

        #Add lazors to list
        if lazor_list[line][0] == "L":
            laz = lazor_list[line]
            laz = laz.replace(" ", "")
            l_x = int(laz[1])
            l_y = int(laz[2])

            #Calculate x movement of lazor
            if laz[3] == "-":
                l_vx = int(laz[4])*(-1)
            else:
                l_vx = int(laz[3])
            
            #Calculate y movement of lazor
            if laz[4] == "-":
                l_vy = int(laz[5])*(-1)
            elif laz[3] == "-" and laz[5] == "-":
                l_vy = int(laz[6])*(-1)
            else:
                l_vy = int(laz[4])
            lazor.append((l_x,l_y,l_vx,l_vy))
                    
        #Add VP's to list
        if lazor_list[line][0] == "P":
            point = lazor_list[line]
            point = point.replace(" ", "")
            vp_x = int(point[1])
            vp_y = int(point[2])
            vp.append((vp_x,vp_y))

        #Add optional blocks to list
        if ((lazor_list[line][0] == "A"
            or lazor_list[line][0] == "B"
            or lazor_list[line][0] == "C")
            and line>end):
            opt_blocks = lazor_list[line]
            opt_blocks = opt_blocks.replace(" ", "")
            opt_type = opt_blocks[0]
            opt_num = int(opt_blocks[1])
            opt.append((opt_type, opt_num))

    #Calculate the length of the grid
    g_wid = end - start - 1
    
    #Determine the width of the grid
    g_len = len(lazor_list[start+1]) - lazor_list[start+1].count(" ") - 1

    #Iterate through grid to find any fixed blocks
    for row in range(start+1, end):
        grid_row = lazor_list[row]
        grid_row = grid_row.replace(" ", "")
        #Iterate through the row
        for block in range(len(grid_row)):
            if (grid_row[block] == "x"
                or grid_row[block] == "A"
                or grid_row[block] == "B"
                or grid_row[block] == "C"):
                fix_block = grid_row[block]
                fix_x = block
                fix_y = row - (start+1)
                fix.append((fix_block, fix_x, fix_y))

    lazor_file.close()

    print("Length: ", g_len)
    print("Width: ", g_wid)
    print("Fixed blocks: ", fix)
    print("Optional blocks: ", opt)
    print("Lazors: ", lazor)
    print("Victory points: ", vp)

    return(g_len, g_wid, fix, opt, lazor, vp)

def add_block(grid, block, flag=0):
    '''
    This adds the block types to the grid.
    
    **Parameters**
    
    grid: *list of lists*
        The list defining the grid
    block: *list of tuples*
        A list defining block characteristics
    flag: *int*
        Holds a value of 0 or 1 if block is fixed or not fixed
        
    **Returns**
    
    grid: *list of lists*
        The list defining the grid with blocks added
    '''
    
    x = block[1]
    y = block[2]
    
    #Fixed block in the grid
    if block[0] == 'x':
        grid[x*2][y*2] = 1
        grid[x*2 + 1][y*2] = 1
        grid[x*2][y*2 + 1] = 1
        grid[x*2 + 1][y*2 + 1] = 1

    #Reflect type block in the grid
    elif block[0] == 'A':
        grid[x*2][y*2] = Reflect(flag)
        grid[x*2 + 1][y*2] = Reflect(flag)
        grid[x*2][y*2 + 1] = Reflect(flag)
        grid[x*2 + 1][y*2 + 1] = Reflect(flag)
   
    #Opaque type block in the grid
    elif block[0] == 'B':
        grid[x*2][y*2] = Opaque(flag)
        grid[x*2 + 1][y*2] = Opaque(flag)
        grid[x*2][y*2 + 1] = Opaque(flag)
        grid[x*2 + 1][y*2 + 1] = Opaque(flag)
    
    #Refract type block in the grid
    elif block[0] == 'C':
        grid[x*2][y*2] = Refract(flag)
        grid[x*2 + 1][y*2] = Refract(flag)
        grid[x*2][y*2 + 1] = Refract(flag)
        grid[x*2 + 1][y*2 + 1] = Refract(flag)
    
    #Exits the system if invalid block type is found
    else:
        raise SystemExit("Invalid block type in bff file")
    return grid


if __name__ == "__main__":
    read_lazor("mad_4")
