class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


# Example usage
rect = Rectangle(5, 3)
print("Length:", rect.length)
print("Width:", rect.width)
print("Area:", rect.area())

