import re
import matplotlib.pyplot as plt
from numpy import*
from itertools import*

class Point:
    x: float
    y: float
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"x:{self.x} y:{self.y}"

    @staticmethod
    def crossProduct(p1, p2, p3) -> int:
        # 0 forward
        # -1 right
        # 1 left 
        if not all(isinstance(i, Point) for i in [p2, p3, p3]):
            raise Exception("you passed not points")
        res = (p2.x-p1.x)*(p3.y-p1.y) - (p3.x-p1.x)*(p2.y-p1.y)
        if res == 0: 
            return res
        return 1 if res > 0 else -1

    @staticmethod
    def countTriangleArea(p1, p2, p3) -> float:
        if not all(isinstance(i, Point) for i in [p1, p2, p3]):
            raise Exception("you passed not points")
        # determinant method
        return 1 / 2 * abs(p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y))

class Figure:
    __points = []  
    __smallestArea = float('inf')
    __smallestPointsIdx = []

    def __init__(self, *points):
        if not all(isinstance(i, Point) for i in points):
            raise Exception("you passed not points")
        self.__points = list(points)

    def addPoint(self, point):
        if isinstance(point, Point):
            self.__points.append(point)

    def plotFigure(self):
        coords = []
        for _, value in enumerate(self.__points):
            coords.append([value.x, value.y])
        coords.append(coords[0])
        xs, ys = zip(*coords)
        plt.figure()
        plt.plot(xs, ys) 
        
        if len(self.__smallestPointsIdx) != 0:
            coords = []
            for _, idx in enumerate(self.__smallestPointsIdx):
                p = self.__points[idx]
                coords.append([p.x, p.y])
            coords.append(coords[0])
            xs, ys = zip(*coords)
            plt.plot(xs, ys)

        plt.show() 

    def __calculateSmallestTriangle(self):
        maxFirstIndex = (len(self.__points) - 2)
        index1 = 0
        area = 0

        for idx0, p0 in enumerate(self.__points[:maxFirstIndex]):
            index1 = idx0 + 1
            for idx1, p1 in enumerate(self.__points[index1:]):
                index2 = index1 + idx1 + 1
                for idx2, p2 in enumerate(self.__points[index2:]):
                    # для трикутників, які знаходяться не всередині полігону
                    if Point.crossProduct(p0, p1, p2) != -1:
                        continue
                    area = Point.countTriangleArea(p0, p1, p2) 
                    if area < self.__smallestArea:
                        self.__smallestArea = area
                        self.__smallestPointsIdx = [idx0, index1+idx1, index2+idx2]

    def __repr__(self):
        return str(self)

    def __str__(self):
        if len(self.__points) < 3:
            return "Ви не ввели хоча б 3 точки"
        self.__calculateSmallestTriangle()
        return f"Індекси: {self.__smallestPointsIdx}\nПлоща: {self.__smallestArea}"

def parseCoordArray(func) -> list: # returns array of coords
    res = []
    nums = re.findall("[-+]?\d+[\.]?\d*", func(), re.MULTILINE)
    nums = nums[1:]
    for i in range(int(len(nums) / 2)):
        res.append(list(map(float, nums[i*2:(i+1)*2])))
    return res

@parseCoordArray
def getFileLines() -> str:
    with open("input.txt") as f:
        return f.read()

if __name__ == "__main__":
    f = Figure() 
    for index, value in enumerate(getFileLines):
        f.addPoint(Point(value[0], value[1]))

    print(f)
    f.plotFigure()
