import os
from glob import glob

zones = ['Af', 'Am', 'Aw', 'BSh', 'BSk', 'BWh', 'BWk', 'Cf', 'Cs', 'Cw', 'Df',
         'Ds', 'Dw']

for z in zones:
    with open('../{}_ll.csv'.format(z), 'w') as out:
        out.write('riverID,lat,long\n')
        pattern = '../Results/{}/*river*'.format(z)
        for f in glob(pattern):
            with open(f, 'r') as tmp:
                riverID = os.path.basename(f)[:-4]
                line = tmp.readline()
                split = line.split(',')
                out.write('{},{},{}\n'.format(riverID, split[2], split[3]))
