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
        return(0, 0)

def class Refract:
    def call(self, lazor):
        lazor1 = lazor
        lazor2 = Reflect(lazor)
        return(lazor1, lazor2)


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

if __name__ == "__main__":
    read_lazor("mad_4")
