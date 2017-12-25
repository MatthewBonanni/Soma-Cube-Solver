import numpy as np

cube_size = 4
default_place = [np.array([[0], [0], [0]]), 0]

shape0 = [np.array([[0],[0],[0]]),
          np.array([[1],[0],[0]]),
          np.array([[2],[0],[0]]),
          np.array([[0],[1],[0]]),
          np.array([[0],[2],[0]])]
shape1 = [np.array([[0],[0],[0]]),
          np.array([[0],[1],[0]]),
          np.array([[1],[1],[0]]),
          np.array([[0],[2],[0]]),
          np.array([[0],[3],[0]])]
shape2 = [np.array([[0],[0],[0]]),
          np.array([[0],[0],[1]]),
          np.array([[1],[0],[0]]),
          np.array([[0],[1],[0]]),
          np.array([[1],[1],[0]])]
shape3 = [np.array([[0],[0],[0]]),
          np.array([[0],[0],[1]]),
          np.array([[0],[1],[0]]),
          np.array([[1],[1],[0]]),
          np.array([[2],[1],[0]]),
          np.array([[1],[2],[0]])]
shape4 = [np.array([[0],[0],[0]]),
          np.array([[1],[0],[0]]),
          np.array([[2],[0],[0]]),
          np.array([[0],[1],[0]]),
          np.array([[0],[1],[1]])]
shape5 = [np.array([[0],[0],[0]]),
          np.array([[1],[0],[0]]),
          np.array([[2],[0],[0]]),
          np.array([[1],[1],[0]]),
          np.array([[1],[1],[1]])]
shape6 = [np.array([[0],[0],[0]]),
          np.array([[1],[0],[0]]),
          np.array([[1],[1],[0]]),
          np.array([[1],[1],[1]]),
          np.array([[2],[1],[1]])]
shape7 = [np.array([[0],[1],[0]]),
          np.array([[1],[1],[0]]),
          np.array([[1],[2],[0]]),
          np.array([[2],[1],[0]]),
          np.array([[1],[0],[1]]),
          np.array([[1],[1],[1]])]
shape8 = [np.array([[0],[0],[0]]),
          np.array([[1],[0],[0]]),
          np.array([[2],[0],[0]]),
          np.array([[0],[1],[0]]),
          np.array([[0],[2],[0]]),
          np.array([[0],[1],[1]])]
shape9 = [np.array([[0],[0],[0]]),
          np.array([[1],[0],[0]]),
          np.array([[2],[0],[0]]),
          np.array([[0],[1],[0]]),
          np.array([[0],[2],[0]]),
          np.array([[0],[2],[1]])]
shape10 = [np.array([[0],[0],[0]]),
           np.array([[0],[0],[1]]),
           np.array([[1],[0],[0]]),
           np.array([[1],[1],[0]]),
           np.array([[2],[1],[0]])]
shape11 = [np.array([[0],[0],[0]]),
           np.array([[0],[1],[0]]),
           np.array([[1],[1],[0]]),
           np.array([[1],[2],[0]]),
           np.array([[1],[3],[0]])]

shapes = [shape0,
          shape1,
          shape2,
          shape3,
          shape4,
          shape5,
          shape6,
          shape7,
          shape8,
          shape9,
          shape10,
          shape11]

piece_count = len(shapes)

ids = [i for i in range(piece_count)]
tshapes = [[] for i in range(piece_count)]
locns = [0 for i in range(piece_count)]

pieces = [list(x) for x in zip(ids, shapes, tshapes, locns)]
