import numpy as np
import time
from datetime import timedelta
from functools import reduce

#from tetris_cube_pieces import pieces, cube_size, default_place
from simple_cube_pieces import pieces, cube_size, default_place

# A Piece is an [ID, Shape, Place]

# A Place is a [Posn, Orient]
# A Posn is an np.array([[x], [y], [z]])
# An Orient is an Integer in [0, 23]

def repeat(func, arg, n):
    '''General repeater function allowing for 1 extra parameter'''
    return lambda a: reduce(lambda x, _: func(x, arg), range(n), a)


def simple_rot(posn, axis):
    '''Rotates given posn around given axis'''
    ax = np.matrix('1 0 0; 0 0 -1; 0 1 0')
    ay = np.matrix('0 0 1; 0 1 0; -1 0 0')
    az = np.matrix('0 -1 0; 1 0 0; 0 0 1')
    return {
        'x': np.array(np.dot(ax, posn)),
        'y': np.array(np.dot(ay, posn)),
        'z': np.array(np.dot(az, posn))
    }[axis]

# Generate list of possible rotation functions
rot_list = []

for x_count in range(4):
    for y_count in range(4):
        def xy_rot(posn, x_count=x_count, y_count=y_count):
            '''Composes x_count x rotations with y_count y rotations'''
            x_rot = repeat(simple_rot, 'x', x_count)(posn)
            return repeat(simple_rot, 'y', y_count)(x_rot)
        rot_list.append(xy_rot)

for z_count in [1, 3]:
    for y_count in range(4):
        '''Composes z_count z rotations with y_count y rotations'''
        def zy_rot(posn, z_count=z_count, y_count=y_count):
            z_rot = repeat(simple_rot, 'z', z_count)(posn)
            return repeat(simple_rot, 'y', y_count)(z_rot)
        rot_list.append(zy_rot)

def transform(piece):
    '''Transforms piece according to its place'''
    shape = piece[1]
    place = piece[2]
    def translate(pt):
        return pt + place[0]
    def rotate(pt):
        return rot_list[place[1]](pt)
    return [rotate(translate(pt)) for pt in shape]

def boundary_conflict(piece):
    '''Determines if the given piece lies outside the cube'''
    tshape = transform(piece)
    for pt in tshape:
        if any(coord < 0 or coord >= cube_size for coord in pt):
            return True
    return False

def shape_conflict(piece, cube):
    '''Determines if the given piece interferes with another in the given cube'''
    tshape = transform(piece)
    for pt in tshape:
        if cube[pt[0][0]][pt[1][0]][pt[2][0]] != -1:
            return True
    return False

def conflict(piece, cube):
    '''Determines if given piece has any conflicts in given cube'''
    if boundary_conflict(piece):
        return True
    elif shape_conflict(piece, cube):
        return True
    else:
        return False

def iter_posn(posn):
    '''Iterates the given posn'''
    if posn[-1] == cube_size - 1:
        return np.append(iter_posn(posn[:-1]), np.array([[0]]), axis=0)
    else:
        return np.append(posn[:-1], posn[-1] + np.array([[1]]), axis=0)

def iter_place(place):
    '''Iterates the given place'''
    if place[1] == 23:
        return [iter_posn(place[0]), 0]
    else:
        return [place[0], place[1] + 1]

def iter_piece(piece):
    '''Iterates the placement of the given piece'''
    piece[2] = iter_place(piece[2])
    return piece

def last_iter(piece):
    '''Determines if the given piece has the last possible placement'''
    place = piece[2]
    return (np.array_equal(place[0], np.array([[cube_size - 1],
                                               [cube_size - 1],
                                               [cube_size - 1]])) and
            place[1] == 23)

def insert(piece, cube):
    '''Inserts the given piece into the given cube'''
    tshape = transform(piece)
    pid = piece[0]
    for pt in tshape:
        cube[pt[0][0]][pt[1][0]][pt[2][0]] = pid
    return cube

def remove(piece, cube):
    '''Removes the given piece from the given cube'''
    tshape = transform(piece)
    for pt in tshape:
        cube[pt[0][0]][pt[1][0]][pt[2][0]] = -1
    return cube

def solved(cube):
    '''Determines whether the cube is solved'''
    return cube[cube == -1].size == 0

def progress():
    '''Displays progress'''
    print('Progress:')
    print(current_cube)
    print()
    elapsed = time.time() - start
    print('Time Elapsed: ' + str(timedelta(seconds=elapsed)))
    print()
    print()


start = time.time()

##### SOLVING ALGORITHM #####

# Initialize iteration variable
i = 0
# Initialize empty cube
current_cube = -1 * np.ones((cube_size, cube_size, cube_size), dtype='int')

# Iterate over list of pieces
while i < len(pieces):
    # Check if current piece fits in the current spot
    if not conflict(pieces[i], current_cube):
        # It fits, insert it and go to the next piece
        current_cube = insert(pieces[i], current_cube)
        progress()
        i = i + 1
        continue
    # It doesn't fit. Check if there are any other spots left to try
    elif last_iter(pieces[i]):
        # No spots left.
        # If this is the first piece, the puzzle is invalid
        if i == 0:
            raise Exception('Invalid Cube')
        # Reset the placement of the current piece
        pieces[i][2] = default_place
        # Remove the previous piece from the cube
        current_cube = remove(pieces[i-1], current_cube)
        progress()
        # If the previous piece has other spots left to try, try the next one
        if not last_iter(pieces[i-1]):
            pieces[i-1] = iter_piece(pieces[i-1])
        # Go back to the previous piece
        i = i - 1
        continue
    # There are spots left, try the next one
    else:
        pieces[i] = iter_piece(pieces[i])
        continue

#Ensure the solution is valid
if not solved(current_cube):
    raise Exception('No solution found')

total_time = time.time() - start

with open('solution.txt', 'w') as f:
    print(current_cube, file=f)
    print(file=f)
    print('Calculation Time: ' + str(timedelta(seconds=total_time)), file=f)
    print(file=f)
    print(pieces, file=f)

print('Finished!')