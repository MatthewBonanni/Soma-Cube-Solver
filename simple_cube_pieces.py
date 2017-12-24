import numpy as np

cube_size = 2
default_place = [np.array([[0], [0], [0]]), 0]

shape0 = [np.array([[0],[0],[0]]),
          np.array([[1],[0],[0]]),
          np.array([[0],[1],[0]])]
shape1 = [np.array([[0],[0],[0]]),
          np.array([[1],[0],[0]])]
shape2 = [np.array([[0],[0],[0]]),
          np.array([[1],[0],[0]])]
shape3 = [np.array([[0], [0], [0]])]

shapes = [shape0,
          shape1,
          shape2,
          shape3]
ids = [i for i in range(len(shapes))]
places = [default_place for shape in shapes]

pieces = [list(x) for x in zip(ids, shapes, places)]
