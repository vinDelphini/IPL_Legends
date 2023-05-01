score = {
    1 : 200,
    2 : 190,
    3 : 180,
    4 : 170,
    5 : 160,
    6 : 150,
    7 : 140,
}

final_score = {
    'Vin Rayudu': 0,
    'iplmogudu': 0,
    'Seenu gadu': 0,
}

while True:
    for key, value in final_score.items():
        # print(key, value)
        match_pos = int(input(f'Enter the position for the match for {key}: '))
        # print(score[match_pos])
        final_score[key] += score[match_pos]
    print(final_score)
