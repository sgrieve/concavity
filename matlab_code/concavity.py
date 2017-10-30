import sys
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

offset_elevs = []
median_norm_offsets = []

n = len(sys.argv[1:])

filelist = ['/Users/stuart/CardiffProject/postprocessing/11_21_river_6.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_647.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_7.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_519.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_113.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_1076.csv',
            '/Users/stuart/CardiffProject/postprocessing/11_21_river_1532.csv']

n = 7

# for filename in sys.argv[1:]:
for filename in filelist:

    data = np.genfromtxt(filename, delimiter=',')

    A = data[:, 4]
    B = data[:, 5]

    R = np.nanmax(B) - np.nanmin(B)

    # where x1,y1 x2,y2 are the long profile endpoints
    x = [A[0], np.nanmax(A)]
    y = [B[0], np.nanmax(B)]

    result = stats.linregress(x, y)

    m = result[0]
    b = result[1]

    Y = m * A + b  # Y values on the line
    offset_elev = (B - Y) / R
    print(offset_elev)
    offset_elevs.append(offset_elev)

    median_norm_offsets.append(np.nanmedian(offset_elev))

mean = np.nanmean(median_norm_offsets)
std = np.nanstd(np.array(median_norm_offsets))
stderror = std / np.sqrt(n)

print(round(mean, 4), round(std, 4), round(stderror, 4))

plt.boxplot(offset_elevs, notch=True)
plt.xlabel('River')
plt.ylabel('Normalised concavity index')
plt.xlim(0.5, n + 0.5)
plt.ylim(-1, 0.5)
plt.savefig('test.png')
