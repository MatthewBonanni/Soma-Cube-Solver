import json
import numpy as np
from functools import reduce

# A Place is a (Posn, Orient)

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

def transform(piece, place):
    def tf_point(pt):
        translated = pt + place[0]
        return rot_list[place[1]](translated)
    return [tf_point(pt) for pt in piece]

def boundary_conflict(tpiece):
    for pt in tpiece:
        if pt[pt < 0].size:
            return False
    return True

def piece_conflict(tpiece, id, cube):
    for pt in tpiece:
        if !isnan(cube[pt[1], pt[2], pt[3]]):
            return False
    return True

def conflict(piece, place, id, cube):
    if boundary_conflict(transform(piece, place)):
        return True
    elif piece_conflict(transform(piece, place), id, cube):
        return True
    else:
        return False
