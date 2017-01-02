class RGB:
    red = int(0)
    green = int(0)
    blue = int(0)

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __eq__(self, other):
        if not isinstance(other, RGB):
            return False

        return int(self.red) == int(other.red) and int(self.green) == int(other.green) and int(self.blue) == int(
            other.blue)

    def __hash__(self):
        return hash((self.red, self.green, self.blue))

    def __str__(self):
        return str(self.red) + ":" + str(self.green) + ":" + str(self.blue)


