import numpy as np

def gene_to_pos(gene=None):
    if gene is None:
        gene = [802, 2176, 3158, 1956, 3622]
    rows = 58
    cols = 73

    # From one dimensional genes to binary grid cell
    grid = np.zeros((rows * cols), dtype='int32')
    for i in range(len(gene)):
        grid[gene[i]] = 1
    grid = grid.reshape(rows, cols)

    # From binary grid cell to grid coordinate
    pos = np.zeros((len(gene), 2), dtype='float64')
    n = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 0:
                pos[n] = i, j
                n += 1

    # From grid coordinate to real coordinate
    lat_min, lat_max, long_min, long_max = 55.6350646, 55.7140006, -4.3633451, -4.1843088
    row_range = lat_max - lat_min
    col_range = long_max - long_min
    pos[:, 0] = pos[:, 0] * row_range / rows + lat_min
    pos[:, 1] = pos[:, 1] * col_range / cols + long_min
    return pos


if __name__ == '__main__':
    gene_to_pos([802, 2176, 3158, 1956, 3622])