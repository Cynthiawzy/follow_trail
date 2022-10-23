
MOVEMENT_SYMBOLS = '><v^'
EMPTY_SYMBOL = '.'
TREASURE_SYMBOL = '+'
BREADCRUMB_SYMBOL = 'X'
MOVEMENT_SYMBOLS_3D = '*|'


def change_map_with_index(maps, index, symbol):

    changed_map = maps[:index] + symbol + maps[index + 1:]
    return changed_map


def last_row_indeces(width, height, start_depth):

    bottom_index = (width * height) - 1
    list_last_row_indeces = ''

    for i in range(width):
        list_last_row_indeces += (str(bottom_index - i + (start_depth * height * width)) + ' ')

    return list_last_row_indeces


def first_row_indeces(width, start_depth, height):

    first_index = width - 1
    list_first_row_indeces = ''
    for i in range(width):
        list_first_row_indeces += (str(first_index - i + (start_depth * width * height)) + ' ')

    return list_first_row_indeces


def movement_0(index, width):

    if (index + 1) % width != 0:
        index += 1
    else:
        index = (index + 1) - width
    return index


def movement_1(index, width):

    if index % width != 0:
        index = index - 1
    else:
        index = index + width - 1
    return index


def movement_2(index, height, start_depth, depth, width):

    if start_depth == depth - 1:
        for n in range(height * depth - 1):
            index -= width
    else:
        index += width
    return index


def movement_2_depth(start_depth, depth):

    if start_depth == depth - 1:
        start_depth = 0
    else:
        start_depth += 1
    return start_depth


def movement_3(index, height, width, start_depth, depth):

    if start_depth == 0:
        for n in range(height * depth - 1):
            index += width
    else:
        index -= width
    return index


def movement_3_depth(start_depth, depth):

    if start_depth == 0:
        start_depth = depth - 1
    else:
        start_depth -= 1
    return start_depth


def follow_trail(maps, start_row, start_column, start_depth, width, height, depth, num_tiles):
    ''' (str, int, int, int, int, int, int, int) -> str
    Given multiple inputs, we will begin following the given map at the start point that is determined by the start inputs.
    The function will stop once we encounter a tile that we have already visited or
    when we have reached the entered number of tiles, whichever one comes first.
    The total number of treasure collected will be displayed as well as the number of tiles visited
    and the map marked with breadcrumbs will be returned.
    If the given number of tiles is -1, then we will follow the map until we encounter the same tile twice.
    If any of the indices are out of bound from the map, the original map will be returned unmarked.
    '''

    index = start_row * width + start_column
    tiles = 0
    treasure_count = 0
    right = 0
    right_comparison = 0
    left = 0
    left_comparison = 0
    down = 0
    down_comparison = 0
    up = 0
    up_comparison = 0
    hole = 0
    hole_comparison = 0
    ladder = 0
    ladder_comparison = 0
    num_tiles_var = 0

    for i in range(start_depth):
        index += width * height

    if start_row >= height or start_column >= width or start_depth >= depth:
        return maps

    if num_tiles == -1:
        num_tiles_var = 1

    while tiles < num_tiles or num_tiles_var == 1:
        if maps[index] == BREADCRUMB_SYMBOL:
            break

        if maps[index] == MOVEMENT_SYMBOLS[0]:
            tiles += 1
            maps = change_map_with_index(maps, index, BREADCRUMB_SYMBOL)
            index = movement_0(index, width)
            if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                right += 1

        elif maps[index] == MOVEMENT_SYMBOLS[1]:
            tiles += 1
            maps = change_map_with_index(maps, index, BREADCRUMB_SYMBOL)
            index = movement_1(index, width)
            if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                left += 1

        elif maps[index] == MOVEMENT_SYMBOLS[2]:
            tiles += 1
            maps = change_map_with_index(maps, index, BREADCRUMB_SYMBOL)

            if str(index) in last_row_indeces(width, height, start_depth):
                index = movement_2(index, height, start_depth, depth, width)
                start_depth = movement_2_depth(start_depth, depth)
            else:
                index += width
            if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                down += 1

        elif maps[index] == MOVEMENT_SYMBOLS[3]:
            tiles += 1
            maps = change_map_with_index(maps, index, BREADCRUMB_SYMBOL)

            if str(index) in first_row_indeces(width, start_depth, height):
                index = movement_3(index, height, width, start_depth, depth)
                start_depth = movement_3_depth(start_depth, depth)
            else:
                index -= width
            if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                up += 1

        elif maps[index] == MOVEMENT_SYMBOLS_3D[0]:
            maps = change_map_with_index(maps, index, BREADCRUMB_SYMBOL)
            tiles += 1
            if start_depth == depth - 1:
                index -= width * height * start_depth
                start_depth = 0
            else:
                index += height * width
                start_depth += 1
            if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                hole += 1

        elif maps[index] == MOVEMENT_SYMBOLS_3D[1]:
            maps = change_map_with_index(maps, index, BREADCRUMB_SYMBOL)
            tiles += 1
            if start_depth == 0:
                start_depth = depth - 1
                index += width * height * start_depth
            else:
                index -= height * width
                start_depth -= 1
            if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                ladder += 1

        elif maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
            tiles += 1
            if maps[index] == TREASURE_SYMBOL:
                treasure_count += 1
            if right > right_comparison:
                index = movement_0(index, width)
                if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                    right += 1
                    right_comparison += 1
                else:
                    right_comparison += 1

            elif left > left_comparison:
                index = movement_1(index, width)
                if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                    left += 1
                    left_comparison += 1
                else:
                    left_comparison += 1

            elif down > down_comparison:
                if str(index) in last_row_indeces(width, height, start_depth):
                    index = movement_2(index, height, start_depth, depth, width)
                    start_depth = movement_2_depth(start_depth, depth)
                else:
                    index += width
                if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                    down += 1
                    down_comparison += 1
                else:
                    down_comparison += 1

            elif up > up_comparison:
                if str(index) in first_row_indeces(width, start_depth, height):
                    index = movement_3(index, height, width, start_depth, depth)
                    start_depth = movement_3_depth(start_depth, depth)
                else:
                    index -= width
                if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                    up += 1
                    up_comparison += 1
                else:
                    up_comparison += 1

            elif hole > hole_comparison:
                if start_depth == depth - 1:
                    index -= width * height * start_depth
                    start_depth = 0
                else:
                    index += height * width
                    start_depth += 1
                if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                    hole += 1
                    hole_comparison += 1
                else:
                    hole_comparison += 1

            elif ladder > ladder_comparison:
                if start_depth == 0:
                    start_depth = depth - 1
                    index += width * height * start_depth
                else:
                    index -= height * width
                    start_depth -= 1
                if maps[index] == EMPTY_SYMBOL or maps[index] == TREASURE_SYMBOL:
                    ladder += 1
                    ladder_comparison += 1
                else:
                    ladder_comparison += 1

    print('Treasures collected:', str(treasure_count))
    print('Symbols visited:', str(tiles))
    return maps



#follow_trail('>+v..*..<...v.<*.|vvv+v+>..', 0, 0, 0, 3, 3, 3, 50)
    #Treasures collected: 1
    #Symbols visited: 11
    #'X+X..X..<...X.XX.|vvv+v+X..'