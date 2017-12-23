import numpy as np
from functools import reduce

# A Piece is an [ID, Shape, Place]

# A Place is a [Posn, Orient]
# A Posn is an np.array([[x], [y], [z]])
# An Orient is an Integer in [0, 23]

from tetris_cube_pieces import pieces, cube_size

# General repeater function allowing for 1 extra parameter
def repeat(func, arg, n):
    return lambda a: reduce(lambda x, _: func(x, arg), range(n), a)

def simple_rot(posn, axis):
    ax = np.matrix('1 0 0; 0 0 -1; 0 1 0')
    ay = np.matrix('0 0 1; 0 1 0; -1 0 0')
    az = np.matrix('0 -1 0; 1 0 0; 0 0 1')
    return {
        'x': np.dot(ax, posn),
        'y': np.dot(ay, posn),
        'z': np.dot(az, posn)
    }[axis]

# Generate list of possible rotation functions
rot_list = []

for x_count in range(4):
    for y_count in range(4):
        def compose_rot(posn, x_count=x_count, y_count=y_count):
            x_rot = repeat(simple_rot, 'x', x_count)(posn)
            return repeat(simple_rot, 'y', y_count)(x_rot)
        rot_list.append(compose_rot)

for z_count in [1, 3]:
    for y_count in range(4):
        def compose_rot(posn, z_count=z_count, y_count=y_count):
            z_rot = repeat(simple_rot, 'z', z_count)(posn)
            return repeat(simple_rot, 'y', y_count)(z_rot)
        rot_list.append(compose_rot)

def transform(piece):
    shape = piece[1]
    place = piece[2]
    def tf_point(pt):
        translated = pt + place[0]
        return rot_list[place[1]](translated)
    return [tf_point(pt) for pt in shape]

def boundary_conflict(piece):
    tshape = transform(piece)
    for pt in tshape:
        if any(coord < 0 or coord > cube_size for coord in pt):
            return True
    return False

def shape_conflict(piece, cube):
    tshape = transform(piece)
    for pt in tshape:
        if cube[pt[0][0]][pt[1][0]][pt[2][0]] != -1:
            return True
    return False

def conflict(piece, cube):
    if boundary_conflict(piece):
        return True
    elif shape_conflict(piece, cube):
        return True
    else:
        return False

def iter_posn(posn):
    if posn[-1] == cube_size - 1:
        return np.append(iter_posn(posn[:-1]), np.array([[0]]), axis=0)
    else:
        return np.append(posn[:-1], posn[-1] + np.array([[1]]), axis=0)

def iter_place(place):
    if place[1] == 23:
        return [iter_posn(place[0]), 0]
    else:
        return [place[0], place[1] + 1]

def iter_piece(piece):
    piece[2] = iter_place(piece[2])
    return piece

def last_iter(piece):
    place = piece[2]
    return (np.array_equal(place[0], np.array([[cube_size - 1],
                                               [cube_size - 1],
                                               [cube_size - 1]])) and
            place[1] == 23)

def insert(piece, cube):
    tshape = transform(piece)
    pid = piece[0]
    for pt in tshape:
        cube[pt[0][0]][pt[1][0]][pt[2][0]] = pid
    return cube

def cube_solve(pieces):
    def cube_solve_acc(pieces, current_cube):
        # Last piece
        if len(pieces) == 1:
            # If it fits, insert it
            if not conflict(pieces[0], current_cube):
                current_cube = insert(pieces[0], current_cube)
                return current_cube
            # Else if it's out of spots, there's a problem
            elif last_iter(pieces[0]):
                return False
            # Else try the next spot
            else:
                pieces[0] = iter_piece(pieces[0])
                return cube_solve_acc(pieces, current_cube)
        # Multiple pieces left to insert
        else:
            # Check if first piece fits
            if not conflict(pieces[0], current_cube):
                # It fits
                # Check if there will be trouble with the next piece
                if not cube_solve_acc(pieces[1:], insert(pieces[0], current_cube)):
                    # Rest of pieces will not fit
                    # If this is the last spot, there's a problem
                    if last_iter(pieces[0]):
                        return False
                    # Try the next spot for the first piece
                    else:
                        pieces[0] = iter_piece(pieces[0])
                        return cube_solve_acc(pieces, current_cube)
                else:
                    # Rest of the pieces fit
                    # Insert piece and move on
                    return cube_solve_acc(pieces[1:], insert(pieces[0], current_cube))
            else:
                # Try the next spot for the first piece
                pieces[0] = iter_piece(pieces[0])
                return cube_solve_acc(pieces, current_cube)
    empty_cube = -1 * np.ones((cube_size, cube_size, cube_size), dtype='int')
    return cube_solve_acc(pieces, empty_cube)

solved_cube = cube_solve(pieces)
print(solved_cube)
