import numpy as np

filelist = ['/Users/stuart/CardiffProject/postprocessing/11_21_river_6.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_647.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_7.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_519.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_113.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_1076.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_1532.csv']

elev = []
dist = []


def padder(x):
    output = []
    longest = len(x[0])
    for a in x:
        if len(a) > longest:
            longest = len(a)

    for a in x:
        if len(a) <= longest:
            tmp = np.empty((longest))

            tmp[:] = np.NAN
            for i, b in enumerate(a):
                tmp[i] = b

            output.append(tmp)

    return output


for filename in filelist:

    data = np.genfromtxt(filename, delimiter=',')

    elev.append(data[:, 4])
    dist.append(data[:, 5])


dists = padder(dist[::-1])
elevs = padder(elev[::-1])

e_cols = np.column_stack(elevs)
d_cols = np.column_stack(dists)


with open('e.txt', 'w') as f:
    for e in e_cols:
        f.write('{}\n'.format('\t'.join([str(q) for q in e])))

with open('d.txt', 'w') as f:
    for d in d_cols:
        f.write('{}\n'.format('\t'.join([str(q) for q in d])))
