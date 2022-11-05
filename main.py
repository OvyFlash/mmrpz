import re

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
    def lineIntersection(p1, p2, p3, p4) -> bool:
        denom = (p4.y-p3.y)*(p2.x-p1.x) - (p4.x-p3.x)*(p2.y-p1.y)
        if denom == 0: # parallel
            return False
        ua = ((p4.x-p3.x)*(p1.y-p3.y) - (p4.y-p3.y)*(p1.x-p3.x)) / denom
        if ua < 0 or ua > 1: # out of range
            return False
        ub = ((p2.x-p1.x)*(p1.y-p3.y) - (p2.y-p1.y)*(p1.x-p3.x)) / denom
        if ub < 0 or ub > 1: # out of range
            return False
        return True

class Figure:
    points = []  
    def __init__(self, *points):
        for i in range(len(points)):
            if isinstance(points[i], Point):
                self.points.append(points[i])

    def addPoint(self, point):
        if isinstance(point, Point):
            self.points.append(point)

    def hasFourPoints(self) -> bool:
        return len(self.points) == 4

    def isQuadrilateral(self) -> bool:
        for i in range(len(self.points)-1):
            if Point.lineIntersection(
                self.points[i % len(self.points)], 
                self.points[(i+1) % len(self.points)], 
                self.points[(i+2) % len(self.points)], 
                self.points[(i+3) % len(self.points)]):
                return False  

        return True

    def _crossProduct(self, A) -> int:
        X1 = (A[1].x - A[0].x)
        Y1 = (A[1].y - A[0].y)
        X2 = (A[2].x - A[0].x)
        Y2 = (A[2].y - A[0].y)
        return (X1 * Y2 - Y1 * X2)

    # опуклість
    def isConvexQuadrilateral(self) -> bool:
        prev = 0
        curr = 0
        N = len(self.points)
        for i in range(N):
            temp = [self.points[i], self.points[(i + 1) % N],
                           self.points[(i + 2) % N]]
            curr = self._crossProduct(temp)
 
            if (curr != 0):
                if (curr * prev < 0):
                    return False
                else:                 
                    prev = curr
        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        if not self.hasFourPoints():
            return "Ви не ввели 4 точки"
        print("Чотирикутник: {}".format("Yes" if self.isQuadrilateral() else "No"))
        isConvex = self.isConvexQuadrilateral()
        print("Опуклий: {}".format("Yes" if isConvex else "No"))
        print("Неопуклий: {}".format("Yes" if not isConvex else "No"))
        return ""

def parseCoordArray(func) -> list: # returns array of coords
    nums = re.findall("[+-]?\d+[.,]?", func())
    res = []
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
