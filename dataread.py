import csv
with open('fandango_score_comparison.csv') as f:
    reader = csv.reader(f)
    w = []
    for row in reader:
        w.extend(row)
        movie = row[0]
        RT_cri = row[9],
        RT_user = row[10],
        Meta_cri = row[11],
        Meta_user = row[12],
        IMDB = row[13],
        print(movie, RT_cri)
