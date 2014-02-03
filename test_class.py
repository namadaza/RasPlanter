
class MyTestClass():
    def __init__(self, input1, input2):
        self.x = input1
        self.y = input2

    def getx(self):
        return self.x

    def setx(self, new_x):
        self.x = new_x
        
    def gety(self):
        return self.y

a = MyTestClass(10, 100)

print a.getx()
a_x = a.getx()
print a_x

a.setx(10)
print a.gety()
a_y = a.gety()
print a_y

b = MyTestClass(100010101, 123423512)

b.getx()

print dir(a)
print dir(b)
