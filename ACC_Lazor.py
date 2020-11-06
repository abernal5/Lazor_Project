# -*- coding: utf-8 -*-
"""
EN.640.635 Software Carpentry
Lazor Project

@author: Alonso, Cam C., Cam G.
"""

import random as rand
import copy


class Reflect:
    '''
    This class serves to represent the reflect blocks in the lazor
    game. These blocks reflect the lazor orthogonally.

    **Parameters**

        flag: *int*
            Marks wether a block is fixed or not. flag == 1 means the block
            is fixed. flag == 0 means it is not.
        side: *str*
            Marks on which side of the "total" block this block
            edge piece is at. This can be either "right" or "left".
            This is used in writting reflect collision mechanics.
    '''

    def __init__(self, flag, side):
        '''
        Initializes the block.
        '''
        self.fixed = flag
        self.side = side

    def __call__(self, lazor_call_A):
        '''
        Allows the user to blindly call this block and have the attached
        lazor go through a refleciton mechanic. This lazor is then returned
        with the updated direction.
        '''
        if lazor_call_A[2] == -1:
            # Lazor is going down and left
            if lazor_call_A[3] == 1:
                # Lazor hits the side of a block
                if self.side == "right":
                    lazor_call_A[2] = 1
                # Lazor hits the top of a block
                else:
                    lazor_call_A[3] = -1
            # Lazor is going up and left
            else:
                # Lazor hits the side of a block
                if self.side == "right":
                    lazor_call_A[2] = 1
                # Lazor hits the bottom of a block
                else:
                    lazor_call_A[3] = 1
        else:
            # Lazor is going down and right
            if lazor_call_A[3] == 1:
                # Lazor hits the side of a block
                if self.side == "left":
                    lazor_call_A[2] = -1
                # Lazor hits the top of a block
                else:
                    lazor_call_A[3] = -1
            # Lazor is going up and right
            else:
                # Lazor hits the side of a block
                if self.side == "left":
                    lazor_call_A[2] = -1
                # Lazor hits the bottom of a block
                else:
                    lazor_call_A[3] = 1
        return(lazor_call_A)

    def __str__(self):
        '''
        Makes the block write itself as 'A'
        '''
        return "A"

    def __repr__(self):
        '''
        Allows you to use print() to write str(block)
        '''
        return str(self)


class Opaque:
    def __init__(self, flag):
        '''
        Initializes the block.
        '''
        self.fixed = flag

    def __call__(self, lazor_call_B):
        '''
        Allows the user to blindly call this block and have the attached
        lazor be absorbed. Returns a lazor with no direction.
        '''
        lazor_call_B[2] = 0
        lazor_call_B[3] = 0
        return lazor_call_B

    def __str__(self):
        '''
        Makes the block write itself as 'B'
        '''
        return "B"

    def __repr__(self):
        '''
        Allows you to use print() to write str(block)
        '''
        return str(self)


class Refract:
    def __init__(self, flag, side):
        '''
        Initializes the block.
        '''
        self.fixed = flag
        self.side = side

    def __call__(self, lazor_call_C):
        '''
        Allows the user to blindly call this block and have the attached
        lazor go through a refleciton mechanic and to pass through the block.
        Both lazors then returned with the updated directions. Also, updates
        the lazor_grid so that no weird double interactions happen for a single
        block
        '''
        A = Reflect(0, self.side)
        lazor_reflected = A(lazor_call_C.copy())
        bypass = lazor_call_C[0], lazor_call_C[1]
        lazor_call_C[0] = lazor_call_C[0] + lazor_call_C[2]
        lazor_call_C[1] = lazor_call_C[1] + lazor_call_C[3]
        lazor_straight = lazor_call_C
        refract_lazors = (lazor_reflected, lazor_straight)
        return refract_lazors, bypass

    def __str__(self):
        '''
        Makes the block write itself as 'C'
        '''
        return "C"

    def __repr__(self):
        '''
        Allows you to use print() to write str(block)
        '''
        return str(self)


def add_block(new_grid, block, flag=0):
    '''
    This will add a block to the existing block grid,
    and return the updated grid.

    **Parameters**

        new_grid: *list, list, [int, object]*
            A list of lists, holding integers or objects that represent blocks:
                0 - Empty Space - A place ready to hold a block
                1 - No Space - A place unable to hold a block
                A - Reflect Block - A reflect block on the grid
                B - Opaque Block - An opaque block on the grid
                C - Refract Block - A refract block on the grid
        block: *tuple*
            Tuple that states the block type and the x and y coordinates on
            the game grid. ex. (A, 0, 2). *Note: These coordinates are counting
            only valid entire block spaces. Half blocks or edges are not
            counted.
        flag: *int*
            An int that indicates wether a block is fixed or not. flag = 1
            means that block is fixed in that location, flag = 0 otherwise.

    **Returns**

        new_grid: *list, list, [int, object]*
    '''
    x = block[1]
    y = block[2]
    if block[0] == 'x':
        new_grid[x*2][y*2] = 1
        new_grid[x*2 + 1][y*2] = 1
        new_grid[x*2][y*2 + 1] = 1
        new_grid[x*2 + 1][y*2 + 1] = 1
    elif block[0] == 'A':
        new_grid[x*2][y*2] = Reflect(flag, side="left")
        new_grid[x*2 + 1][y*2] = Reflect(flag, side="right")
        new_grid[x*2][y*2 + 1] = Reflect(flag, side="left")
        new_grid[x*2 + 1][y*2 + 1] = Reflect(flag, side="right")
    elif block[0] == 'B':
        new_grid[x*2][y*2] = Opaque(flag)
        new_grid[x*2 + 1][y*2] = Opaque(flag)
        new_grid[x*2][y*2 + 1] = Opaque(flag)
        new_grid[x*2 + 1][y*2 + 1] = Opaque(flag)
    elif block[0] == 'C':
        new_grid[x*2][y*2] = Refract(flag, side="left")
        new_grid[x*2 + 1][y*2] = Refract(flag, side="right")
        new_grid[x*2][y*2 + 1] = Refract(flag, side="left")
        new_grid[x*2 + 1][y*2 + 1] = Refract(flag, side="right")
    else:
        raise SystemExit("Invalid block type in bff file")
    return new_grid


def read_lazor(level_name):
    '''
    This reads in the .bff file and creates the assorted values
    required to run the solver. The level_name should not include the .bff
    extension when being passed in.

    **Parameters**

        level_name: *str*
            This is the level name without the .bff extension.

    **Returns**

        g_len: *int*
            The length (columns) of the level.
        g_wid: *int*
            The width (rows) of the level.
        fix: *list[tuple]*
            List of tuples describing fixed blocks and their location.
            Ex. (['A', 2,2], ['x', 0, 0])
        opt: *list[tuple]*
            List of tuples describing how many blocks we have to
            use on the level. Ex. (['A', 5], ['B', 6])
        lazor: *list[tuple]*
            List of tuples that describe the starting positions of lazors
            and their behaviors.
        vp: *list[tuples]*
            List of tuples that describe the victory points that need to be
            traversed in order to complete the level.
            Ex. [(4,5),(2,3)]
    '''
    filename = level_name + ".bff"
    lazor_file = open(filename)
    lazor_list = lazor_file.readlines()
    # Initialize list of lazors
    lazor = []
    # Initialize list of VP's
    vp = []
    # Initialize list of optional blocks
    opt = []
    # Initialize list of fixed grid blocks
    fix = []
    start = lazor_list.index("GRID START\n")
    end = lazor_list.index("GRID STOP\n")
    # Iterate through list to find where the grid is defined
    for line in range(len(lazor_list)):
        # if "GRID START" in lazor_list[line]:
        #     start = line
        # if "GRID STOP" in lazor_list[line]:
        #     end = line

        # Add lazors to list
        if lazor_list[line][0] == "L":
            laz = lazor_list[line]
            laz = laz.replace(" ", "")
            l_x = int(laz[1])
            l_y = int(laz[2])

            # Calculate x movement of lazor
            if laz[3] == "-":
                l_vx = int(laz[4])*(-1)
            else:
                l_vx = int(laz[3])
            # Calculate y movement of lazor
            if laz[4] == "-":
                l_vy = int(laz[5])*(-1)
            elif laz[3] == "-" and laz[5] == "-":
                l_vy = int(laz[6])*(-1)
            else:
                l_vy = int(laz[4])
            lazor.append((l_x, l_y, l_vx, l_vy))

        # Add VP's to list
        if lazor_list[line][0] == "P":
            point = lazor_list[line]
            point = point.replace(" ", "")
            vp_x = int(point[1])
            vp_y = int(point[2])
            vp.append((vp_x, vp_y))

        # Add optional blocks to list
        if ((lazor_list[line][0] == "A"
            or lazor_list[line][0] == "B"
            or lazor_list[line][0] == "C")
                and line > end):
            opt_blocks = lazor_list[line]
            opt_blocks = opt_blocks.replace(" ", "")
            opt_type = opt_blocks[0]
            opt_num = int(opt_blocks[1])
            opt.append((opt_type, opt_num))

    # Calculate the length of the grid
    g_wid = end - start - 1
    # Determine the width of the grid
    g_len = len(lazor_list[start+1]) - lazor_list[start+1].count(" ") - 1

    # Iterate through grid to find any fixed blocks
    for row in range(start+1, end):
        grid_row = lazor_list[row]
        grid_row = grid_row.replace(" ", "")
        # Iterate through the row
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

    return(g_len, g_wid, fix, opt, lazor, vp)


def generate_grid(input_name):
    '''
    This generates the block_grid and the lazor_grid from the passed
    values read from the .bff file.

    **Parameters**

    input_name: *str*
        This is the level name without the .bff extension.

    **Returns**

    block_grid: *list[list[ints]]*
        The block grid where blocks can be placed.
    lazor_grid: *list[list[ints]]*
        The lazor grid that the lazor will traverse and where the victory
        points will be placed.
    lazor: *list[tuple]*
            List of tuples that describe the starting positions of lazors
            and their behaviors.
    blocks: *list[tuple]*
            List of tuples describing how many blocks we have to
            use on the level. Ex. (['A', 5], ['B', 6])
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
        lazor_grid[x][y] = 2

    # Save grid, lazor, and optional blocks
    return block_grid, lazor_grid, lazor, blocks


def solution_generator(grid, blocks):
    '''
    This generates solution grids to be tested to see if they are the solution.

    **Parameters**

    grid: *list[list[ints]]*
        The block grid where blocks can be placed.
    blocks: *list[tuple]*
            List of tuples describing how many blocks we have to
            use on the level. Ex. (['A', 5], ['B', 6])

    **Returns**

     grid: *list[list[ints]]*
        The updated block grid with the blocks already placed.
    '''
    count_A = 0
    count_B = 0
    count_C = 0
    for types in blocks:
        if types[0] == 'A':
            count_A = types[1]
        if types[0] == 'B':
            count_B = types[1]
        if types[0] == 'C':
            count_C = types[1]
    total_count = count_A + count_B + count_C
    types = ['A', 'B', 'C']
    x_spots = list(range(0, len(grid) - 1, 2))
    y_spots = list(range(0, len(grid[0]) - 1, 2))
    while total_count > 0:
        x = rand.choice(x_spots)
        y = rand.choice(y_spots)
        if grid[x][y] == 0:
            block_type = rand.choice(types)
            if block_type == 'A' and count_A > 0:
                grid = add_block(grid, ('A', int(x/2), int(y/2)))
                total_count -= 1
                count_A = count_A - 1
            if block_type == 'B' and count_B > 0:
                grid = add_block(grid, ('B', int(x/2), int(y/2)))
                total_count -= 1
                count_B -= 1
            if block_type == 'C' and count_C > 0:
                grid = add_block(grid, ('C', int(x/2), int(y/2)))
                total_count -= 1
                count_C -= 1
            else:
                block_type = rand.choice(types)
    return grid


def solve_grid(input_name):
    '''
    This master program runs everything, from reading in the .bff file, to
    generating the grids, to finding the solutions.

    **Parameters**

    input_name: *str*
        This is the level name without the .bff extension.

    **Returns**

     None
    '''
    fail = 0
    block_grid, lazor_grid, lazor, blocks = generate_grid(input_name)
    reset_blocks = copy.deepcopy(block_grid)
    reset_lazors = copy.deepcopy(lazor_grid)
    reset_lazor = copy.deepcopy(lazor)
    vp_count = 0
    for column in lazor_grid:
        vp_count += column.count(2)
    while fail == 0:
        vp_check = 0
        temp_grid = copy.deepcopy(reset_blocks)
        temp_lazors = copy.deepcopy(reset_lazors)
        temp_lazor = copy.deepcopy(reset_lazor)
        block_grid = solution_generator(temp_grid, blocks)
        lazor_grid = temp_lazors
        lazor = temp_lazor
        lazor_count = len(lazor)
        while lazor_count > 0:
            cur_lazor = list(lazor[-1])
            while 1 == 1:
                x = cur_lazor[0]
                y = cur_lazor[1]
                try:
                    if lazor_grid[x][y] == 2:
                        vp_check += 1
                except IndexError:
                    lazor.pop()
                    break
                try:
                    block_grid[x][y]
                except IndexError:
                    lazor.pop()
                    break
                if cur_lazor[3] > 0:
                    # lazor is going down and left
                    if cur_lazor[2] < 0:
                        if x <= 0:
                            lazor.pop()
                            break
                        block = block_grid[x - 1][y]
                        if block != 0 and block != 1:
                            if isinstance(block, Refract):
                                refract_lazors, bypass = block(cur_lazor)
                                lazor.insert(0, refract_lazors[0])
                                cur_lazor = refract_lazors[1]
                                lazor_grid[bypass[0]][bypass[1]] = 1
                            else:
                                cur_lazor = block(cur_lazor)
                    else:
                        # lazor is going down and right
                        block = block_grid[x][y]
                        if block != 0 and block != 1:
                            if isinstance(block, Refract):
                                refract_lazors, bypass = block(cur_lazor)
                                lazor.insert(0, refract_lazors[0])
                                cur_lazor = refract_lazors[1]
                                lazor_grid[bypass[0]][bypass[1]] = 1
                            else:
                                cur_lazor = block(cur_lazor)
                else:
                    # lazor is going up and left
                    if cur_lazor[2] < 0:
                        if x <= 0 or y <= 0:
                            lazor.pop()
                            break
                        block = block_grid[x - 1][y - 1]
                        if block != 0 and block != 1:
                            if isinstance(block, Refract):
                                refract_lazors, bypass = block(cur_lazor)
                                lazor.insert(0, refract_lazors[0])
                                cur_lazor = refract_lazors[1]
                                lazor_grid[bypass[0]][bypass[1]] = 1
                            else:
                                cur_lazor = block(cur_lazor)
                    else:
                        # lazor is going up and right
                        block = block_grid[x][y - 1]
                        if block != 0 and block != 1:
                            if isinstance(block, Refract):
                                refract_lazors, bypass = block(cur_lazor)
                                lazor.insert(0, refract_lazors[0])
                                cur_lazor = refract_lazors[1]
                                lazor_grid[bypass[0]][bypass[1]] = 1
                            else:
                                cur_lazor = block(cur_lazor)
                lazor_grid[x][y] = 1
                if cur_lazor[2] == 0 and cur_lazor[3] == 0:
                    lazor.pop()
                    break
                cur_lazor[0] = cur_lazor[0] + cur_lazor[2]
                cur_lazor[1] = cur_lazor[1] + cur_lazor[3]
            lazor_count = len(lazor)
            if vp_count == vp_check:
                fail = 1
                print("\nSolution found!\nPlease see your results below\n")
                break
    print(block_grid)


if __name__ == "__main__":
    solve_grid("mad_1")
    solve_grid("mad_4")
    solve_grid("mad_7")
    solve_grid("dark_1")
    solve_grid("tiny_5")
    solve_grid("yarn_5")
    solve_grid("numbered_6")
