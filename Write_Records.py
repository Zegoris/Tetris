import csv
import os

def write_records(user, gm, score):
    yes = False
    with open('records.csv', encoding="utf8") as csvf:
        reader = csv.reader(csvf, delimiter=',', quotechar='"')
        reader = list(reader)
    os.remove('records.csv')
    for i in reader:
        if user in i:
            yes = True
            index = reader.index(i)
            if gm == 1:
                if score > int(reader[index][1]):
                    reader[index] = [user, score, i[2]]

            elif gm == 2:
                if score > int(reader[index][2]):
                    reader[index] = [user, i[1], score]
            break
    if not yes:
        if gm == 1:
            reader.append([user, score, '0'])
        elif gm == 2:
            reader.append([user, '0', score])
    with open('records.csv', 'w', newline='') as csvf:
        writer = csv.writer(
            csvf,)
        writer.writerows(reader)

