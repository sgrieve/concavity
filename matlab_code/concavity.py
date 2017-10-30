import sys
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

offset_elevs = []
median_norm_offsets = []

output_filename = sys.argv[1]

n = len(sys.argv[2:])

for filename in sys.argv[1:]:

    data = np.genfromtxt(filename, delimiter=',')

    A = data[:, 5]
    B = data[:, 4]

    R = np.nanmax(B) - np.nanmin(B)

    # where x1,y1 x2,y2 are the long profile endpoints
    x = [A[0], np.nanmax(A)]
    y = [B[0], np.nanmax(B)]

    result = stats.linregress(x, y)

    m = result[0]
    b = result[1]

    Y = m * A + b  # Y values on the line
    offset_elev = (B - Y) / R
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
plt.savefig('{}.png'.format(output_filename))
