class Dog():
    """A class to represent a general dog"""

    def __init__(self, my_name, my_gender, my_age):
        """Initilize attributes"""
        self.name = my_name
        self.gender = my_gender
        self.age = my_age

    def eat(self):
        """Feed the dog"""
        if self.gender == "male":
            print("Here " + self.name + "! Good Boy!  Eat up.")
        else:
            print("Here " + self.name + "! Good Girl! Eat up.")

    def bark(self, is_loud):
        """Get the dog to speak"""
        if is_loud:
            print("WOOF WOOF WOOF WOOF")
        else:
            print("woof...")

    def compute_age(self):
        """Compute the age in dog years"""
        dog_years = self.age*7
        print(self.name + " is " + str(dog_years) + " years old in dog years.")

class Beagle(Dog):
    """A class to represent a specific type of dog"""

    def __init__(self, my_name, my_gender, my_age, is_gun_shy):
        #Call the initializtion of the super (parent) class
        super().__init__(my_name, my_gender, my_age)
        self.is_gun_shy = is_gun_shy

    def hunt(self):
        """If the dog is not gun shy, take them hunting"""
        if not self.is_gun_shy:
            self.bark(True)
            print(self.name + " just brought back a duck.")
        else:
            print(self.name + " is not a good hunting dog.")

    def bark(self, is_loud):
        """Get the dog to speak"""
        if is_loud:
            print("HOWL HOWL HOWWWWWWWWWWLLLLLLLLLLL")
        else:
            print("howl")



beagle = Beagle("kady", "female", 10, False)
beagle.eat()
beagle.bark(False)
beagle.compute_age()
print()
beagle.hunt()

#The Dog class can't hunt!
dog = Dog("spotty dog", "male", 3)
#dog.hunt()
dog.bark(True)