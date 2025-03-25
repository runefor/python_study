from tkinter import *


def buttonClickPrintText(et:Entry):
    ent_text = et.get()
    print(ent_text)


def mainView(win: Tk):
    lb = Label(win, text="아래 빈칸에 텍스트를 입력하세요.", width=40)
    et = Entry(win, width=40)
    bt = Button(win, text="확인", width=40, bg="pink", command=lambda: buttonClickPrintText(et))
    lb.pack()
    et.pack()
    bt.pack()


if __name__ == "__main__":

    window = Tk()
    window.title("이벤트 만들기")

    mainView(window)

    window.mainloop()