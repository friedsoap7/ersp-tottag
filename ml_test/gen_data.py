from random import choice

train_data = ""
train_file = open("train.csv", 'w')

for i in range(50):
    train_data = train_data + str(i) + ","
train_data = train_data + "category\n"

for dist in [1, 2, 4, 5, 6, 8, 9, 11]:
    for i in range(50):
        curr_measurement = choice([dist, dist, dist, dist - 1, dist - 1, dist + 1, dist + 1, dist - 2, dist + 2])
        if curr_measurement < 0:
            curr_measurement = 0
        train_data = train_data + str(curr_measurement) + ","
    if dist < 6:
        train_data = train_data + "close\n"
    else:
        train_data = train_data + "far\n"

train_file.write(train_data)