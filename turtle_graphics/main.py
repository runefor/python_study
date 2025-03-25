import turtle

def makeSquare():
    for _ in range(4):
        turtle.forward(100)
        turtle.left(90)


def makeCircle():
    for _ in range(360):
        turtle.forward(1)
        turtle.left(1)

def makeStar():
    for _ in range(5):
        turtle.forward(100)
        turtle.left(144)


def movePen(go_to=200):
    turtle.penup()
    turtle.goto(go_to, 0)
    turtle.pendown()

def pause():
    turtle.exitonclick()

if "__main__" == __name__:
    
    # makeSquare()
    # movePen()
    # makeCircle()
    
    makeStar()
    pause()