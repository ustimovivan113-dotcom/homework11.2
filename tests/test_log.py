from src.decorators import log

@log(filename="mylog.txt")
def add(x, y):
    return x + y

add(1, 2)