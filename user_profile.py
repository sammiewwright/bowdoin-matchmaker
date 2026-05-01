class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = int(age)

class Profile(Person):
    def __init__(self, first_name, last_name, age, interest1, interest2, music_type, hometown, goal):
        super().__init__(first_name, last_name, age)
        self.last_name = last_name
        self.interest1 = interest1
        self.interest2 = interest2
        self.music_type = music_type
        self.hometown = hometown
        self.goal = goal

    def get_interests(self):
        return {self.interest1, self.interest2}