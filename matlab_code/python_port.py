from scipy import stats
import numpy as np
import matplotlib.pyplot as plt


A = np.genfromtxt('d.txt', delimiter='\t')
B = np.genfromtxt('e.txt', delimiter='\t')

m, n = A.shape

offset_norm_elev = np.empty((m, n))
offset_norm_elev[:] = np.NAN
median_norm_offset = np.empty((m, n))
median_norm_offset[:] = np.NAN
iqr_norm_offset = np.empty((m, n))
iqr_norm_offset[:] = np.NAN

for i in range(0, n):
    X = A[:, i]
    E = B[:, i]

    R = np.nanmax(B[:, i]) - np.nanmin(B[:, i])

    x1 = A[0, i]
    x2 = np.nanmax(A[:, i])

    y1 = B[0, i]
    y2 = np.nanmax(B[:, i])  # where x1,y1 x2,y2 are the long profile endpoints
    x = [x1, x2]
    y = [y1, y2]

    result = stats.linregress(x, y)

    m = result[0]
    b = result[1]

    Y = m * X + b  # Y values on the line
    offset_elev = (E - Y) / R
    offset_norm_elev[:, i] = offset_elev
    median_norm_offset[i] = np.nanmedian(offset_elev)

    iqr_norm_offset[i] = stats.iqr(offset_elev, nan_policy='omit')


# Need to transpose the data into the expcted shape for python boxplots and
# remove the nans.
x = []
for a in offset_norm_elev.transpose():
    x.append(a[~np.isnan(a)])


mean = np.nanmean(median_norm_offset)
std = np.nanstd(median_norm_offset, ddof=n)
stderror = std / np.sqrt(n)

print(round(mean, 4), round(std, 4), round(stderror, 4))

plt.boxplot(x, notch=True)
plt.xlabel('River')
plt.ylabel('Normalised concavity index')
plt.xlim(0.5, 7.5)
plt.ylim(-1, 0.5)
plt.show()
