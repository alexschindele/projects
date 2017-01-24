from random import randint

class Die():

    def __init__(self, num_sides = 6):
        self.num_sides = num_sides

    def roll(self):
        return randint(1, self.num_sides)


die = Die()

results = []
for roll_num in range(100):
    results.append(die.roll())

print(results)