import random

class RandomPassword:
    def __init__(self):
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
        self.numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
        self.allKeyPossibilities = [self.letters, self.numbers, self.symbols]

    def randomizer(self):
        """Is not used for hashes. Just generates a suggested semi random password that the user could use for a password for a site."""
        your_password_list = []
        your_password = None
        for i in range(0, random.randint(10, 26)):
            randomizer = random.randint(0, 2)
            your_password_list.append(self.allKeyPossibilities[randomizer]
                                      [random.randint(0, len(self.allKeyPossibilities[randomizer])) - 1])

        your_password = f"{''.join(your_password_list)}"
        return your_password



