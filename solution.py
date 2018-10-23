"""
Rozwiązania do laboratorium 1 z Obrazowania Biomedycznego.
"""
import numpy as np

"""
3 - Kwadrat
"""
def square(size, side, start):
    image = np.zeros((size,size)).astype(np.uint8)
    image[start[1]:start[1]+side, start[0]:start[0]+side] = 255
    return image

"""
3 - Koło
"""
def midcircle(size):
    image = np.zeros((size)).astype(np.uint8)
    center = (size[0]/2, size[1]/2)
    radius = min(size)/4
    radius_squared = radius**2
    for i in range(size[0]):
        for j in range(size[1]):
            if (center[0]-i)**2 + (center[1]-j)**2 <= radius_squared:
                image[i, j] = 255
    return image


"""
3 - Szachownica.
"""
def checkerboard(size):
    image = np.zeros((size, size)).astype(np.uint8)
    field_size = size // 8
    for i in range(size):
        for j in range(size):
            if (i // field_size % 2 == 1) != (j // field_size % 2 == 1):
                image[j,i] = 255
    return image

"""
4 - Interpolacja najbliższych sąsiadów.
"""
def get_size_ratio(old_size, new_size):
    param_x = old_size[0] / new_size[0]
    param_y = old_size[1] / new_size[1]
    return param_x, param_y

def get_nearest_int(arg):
    if (arg - int(arg)) < 0.5:
        return int(arg)
    else:
        return int(arg)+1

def nearest_neighbour_index(x, y, max_index):
    nearest_x = get_nearest_int(x)
    nearest_y = get_nearest_int(y)

    #below we interpolate out frame by duplicating indexes
    if nearest_x >= max_index[0]:
        nearest_x = max_index[0]-1
    if nearest_y >= max_index[1]:
        nearest_y = max_index[1]-1
    
    return (nearest_x, nearest_y)

def nn_interpolation(source, new_size):
    image = np.zeros((new_size)).astype(np.uint8)
    x_ratio, y_ratio = get_size_ratio(source.shape, new_size)

    for i in range(new_size[0]):
        for j in range(new_size[1]):
            # full 
            image[i, j] = source[nearest_neighbour_index(i*x_ratio, j*y_ratio, source.shape)]

    return image

"""
5 - Interpolacja dwuliniowa
"""
def get_neighbours(image, x, y):
    f = []
    f.append(image[x, y]) # Q11
    f.append(image[x+1, y]) # Q21
    f.append(image[x, y+1]) # Q12
    f.append(image[x+1, y+1]) # Q22
    return f


def interpolation(source, x, y):

    # getting nodes
    x1 = int(x)
    x2 = int(x) +1 
    y1 = int(y)
    y2 = int(y) + 1

    f = get_neighbours(source, x1, y1)

    # interpolation in x
    r1 = f[0]*(x2 - x) + f[1]*(x - x1)
    r2 = f[2]*(x2 - x) + f[3]*(x - x1)

    result = r1*(y2 - y)+ r2*(y-y1)

    return result

def bilinear_interpolation(source, new_size):
    image = np.zeros((new_size)).astype(np.uint8)
    x_ratio, y_ratio = get_size_ratio(source.shape, new_size)

    for i in range(new_size[1]-1):
        for j in range(new_size[0]-1):
            image[i, j] = interpolation(source, x_ratio*i, y_ratio*j)

    return image
