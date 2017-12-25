import numpy as np
import time
from datetime import timedelta
from functools import reduce
import pickle

from tetris_cube_pieces import pieces, cube_size, default_place
#from simple_cube_pieces import pieces, cube_size, default_place

# A Piece is an [ID, Shape, TShapes, Locn]

# A TShape is a transformed shape
# Locn is a number indicating which Transform currently represents the piece

# A Placement is a [Posn, Orient]
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

def transform(shape, place):
    '''Transforms the given shape according to the given place'''
    def translate(pt):
        return pt + place[0]
    def rotate(pt):
        return rot_list[place[1]](pt)
    return [rotate(translate(pt)) for pt in shape]

def boundary_conflict(tshape):
    '''Determines if the given piece lies outside the cube'''
    for pt in tshape:
        if any(coord < 0 or coord >= cube_size for coord in pt):
            return True
    return False

def shape_conflict(tshape, cube):
    '''Determines if the given piece interferes with another in the given cube'''
    for pt in tshape:
        if cube[pt[0][0]][pt[1][0]][pt[2][0]] != -1:
            return True
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

def last_iter(place):
    '''Determines if the given place is the last possible placement'''
    return (np.array_equal(place[0], np.array([[cube_size - 1],
                                               [cube_size - 1],
                                               [cube_size - 1]])) and
            place[1] == 23)

def last_locn(piece):
    '''Determines if the given piece's location is set to its last tshape'''
    return piece[3] == len(piece[2]) - 1

def insert(piece, cube):
    '''Inserts the given piece into the given cube'''
    pid = piece[0]
    locn = piece[3]
    for pt in piece[2][locn]:
        cube[pt[0][0]][pt[1][0]][pt[2][0]] = pid
    return cube

def remove(piece, cube):
    '''Removes the given piece from the given cube'''
    locn = piece[3]
    for pt in piece[2][locn]:
        cube[pt[0][0]][pt[1][0]][pt[2][0]] = -1
    return cube

def solved(cube):
    '''Determines whether the cube is solved'''
    return cube[cube == -1].size == 0

def disp_progress():
    '''Displays disp_progress'''
    print('Progress:')
    print()
    print(current_cube)
    print()
    elapsed = time.time() - start
    print('Time Elapsed: ' + str(timedelta(seconds=elapsed)))
    print()
    print()

##### SOLVING ALGORITHM #####

start = time.time()

try:
    print('Loading piece transformations...')
    with open('transformations.pckl', 'rb') as data:
        pieces = pickle.load(data)
except IOError:
    print('Data not available. Calculating piece transformations...')
    for piece in pieces:
        print('disp_progress: Piece ' + str(piece[0] + 1) + '/' + str(len(pieces)))
        current_place = default_place
        piece[2].append(piece[1])
        while not last_iter(current_place):
            tshape = transform(piece[1], current_place)
            current_place = iter_place(current_place)
            if not boundary_conflict(tshape):
                piece[2].append(tshape)
    with open('transformations.pckl', 'wb') as data:
        pickle.dump(pieces, data)
    print('DONE')
    print()

print('Assembling cube...')

loop_time = time.time()
# Initialize iteration variable
i = 0
# Initialize empty cube
current_cube = -1 * np.ones((cube_size, cube_size, cube_size), dtype='int')

# Iterate over list of pieces
while i < len(pieces):
    # Every 30 seconds, display the current status of the cube
    if time.time() - loop_time > 30:
        disp_progress()
        loop_time = time.time()
    current_locn = pieces[i][3]
    tshape = pieces[i][2][current_locn]
    # Check if current piece fits in the current spot
    if not shape_conflict(tshape, current_cube):
        # It fits, insert it and go to the next piece
        current_cube = insert(pieces[i], current_cube)
        i = i + 1
        continue
    # It doesn't fit. Check if there are any other spots left to try
    elif last_locn(pieces[i]):
        # No spots left.
        # If this is the first piece, the puzzle is invalid
        if i == 0:
            raise Exception('Invalid Cube')
        # Reset the placement of the current piece
        pieces[i][3] = 0
        # Remove the previous piece from the cube
        current_cube = remove(pieces[i-1], current_cube)
        # If the previous piece has other spots left to try, try the next one
        if not last_locn(pieces[i-1]):
            pieces[i-1][3] = pieces[i-1][3] + 1
        # Go back to the previous piece
        i = i - 1
        continue
    # There are spots left, try the next one
    else:
        pieces[i][3] = current_locn + 1
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