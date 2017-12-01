import os

with open('wclock.txt', 'r') as seg:
    lines = seg.readlines()

polys = []

for l in lines:
    polys.append(' ' + l[2:].strip() + ' ')

print(len(polys))

with open('processing/array_params_0_1.txt', 'r') as one:
    params = one.readlines()

with open('processing/array_params_1_15.txt', 'r') as two:
    params += two.readlines()

with open('processing/array_params_15_60.txt', 'r') as three:
    params += three.readlines()

with open('processing/array_params_60_200.txt', 'r') as four:
    params += four.readlines()

final_params = []

for p in polys:
    for param in params:
        if p in param:
            final_params.append(param.strip())


with open('wclock_to_re_run_8hr.txt', 'w') as out1:
    with open('wclock_to_re_run_20hr.txt', 'w') as out2:
        for i, a in enumerate(final_params, start=1):
            count = int(a.split()[-1])
            if count < 55:
                out1.write('{} {}{}'.format(str(i).zfill(4), a[5:], '\n'))
            else:
                out2.write('{} {}{}'.format(str(i).zfill(4), a[5:], '\n'))
