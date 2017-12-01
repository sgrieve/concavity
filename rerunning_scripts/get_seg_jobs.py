import os

with open('segfaults.txt', 'r') as seg:
    lines = seg.readlines()

polys = []

for f in lines:
    f = f.replace('.e', '.o').strip()

    with open('remaining_results/{}'.format(f)) as stdout:
        for l in stdout.readlines():
            if l.startswith('Copying nodata values from source tmp.bil'):
                polys.append(l.split('destination ')[1].split('.')[0])

with open('processing/array_params_15_60.txt', 'r') as three:
    params = three.readlines()

with open('processing/array_params_60_200.txt', 'r') as four:
    params += four.readlines()

final_params = []

for p in polys:
    for param in params:
        if p in param:
            final_params.append(param.strip())


with open('segfaults_to_re_run.txt', 'w') as out:
    for i, a in enumerate(final_params, start=1):
        out.write('{} {}{}'.format(str(i).zfill(4), a[5:], '\n'))
