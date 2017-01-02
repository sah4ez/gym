class coordinates:
    X = int(0)
    Y = int(0)

    def __init__(self, X=0, Y=0):
        self.X = X
        self.Y = Y

    def __str__(self):
        r = "{:.2f} :: {:.2f}".format(self.X, self.Y)
        return r

    def __eq__(self, other):
        if not isinstance(other, coordinates):
            return False

        return int(self.X) == int(other.X) and int(self.Y) == int(other.Y)

    def __hash__(self):
        return hash((self.X, self.Y))
