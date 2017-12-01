files = []

with open('file_list.txt') as f:
    for q in f.readlines():
        if q.endswith('.csv\n'):
            files.append(q.strip())

with open('file_list_cleaned.txt', 'w') as f:
    for q in files:
        # NEED TO ADD THE FOLDER NAME TO THE FILE TO BUILD THE FULL PATH:
        # EG IF THE FILENAME IS 8_26_RIVER_5.CSV IT SHOULD READ:
        # <FULL LEGION PATH TO THE SRTM_ORIGINAL FOLDER>/8_26/8_26_RIVER_5.CSV
        f.write(q + '\n')
