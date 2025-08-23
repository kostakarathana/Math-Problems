import matplotlib.pyplot as plt
import random

class Person:
    def __init__(self, name):
        self.name = name
        self.skill = 1
        self.skill_record = [self.skill]

    def increase(self, percentage: int):
        self.skill += self.skill * (percentage / 100)
        self.skill_record.append(self.skill)

    def stagnate(self):
        self.skill_record.append(self.skill)

    def decrease(self, percentage: int):
        self.skill -= self.skill * (percentage / 100)
        self.skill_record.append(self.skill)

    def get_skill(self):
        return self.skill

    def get_name(self):
        return self.name

    def get_skill_record(self):
        return self.skill_record


if __name__ == "__main__":
    person1 = Person("Improve Every Day")
    person2 = Person("Improve Every Day But One")

    # person 1, 5 years later
    for i in range(365*50):
        person1.increase(1)


    # person 2, 5 years later
    for i in range(365*50):
        if (i % 365) in {100, 101, 102, 103, 104, 105, 106, 107}:
            person2.stagnate()
        else:
            person2.increase(1)

    print(f"multiplier difference = {round(person1.get_skill_record()[-1] / person2.get_skill_record()[-1],2)}x")
    plt.plot(person1.skill_record)
    plt.plot(person2.skill_record)
    plt.show()





