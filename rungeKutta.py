from tkinter import *
from tkinter import messagebox as mb
import matplotlib.pyplot as plt
import numpy as np
import math
from decimal import *

y = Decimal('1')
pr_y = Decimal('0')
step = Decimal('0.1')
sigma = Decimal('1')
error = Decimal('0.0001')
begin = 0
end = 10
n = 0

def check():
    flag = True
    global n
    n = 0
    try:
        flag = True
        global y , pr_y, step, sigma, error, begin, end
        y = Decimal (y_e.get())
        pr_y = Decimal(pr_y_e.get())
        step = Decimal (step_e.get())
        sigma = Decimal (sigma_e.get())
        error = Decimal (error_e.get())
        begin = int (begin_e.get())
        end = int (end_e.get())
    except:
        flag = False
        mb.showerror("Error", "Не правильно введены поля!")
    if begin>end :
        flag = False
        mb.showerror("Error", "Неправильно введен интервал!")
    if (step > end-begin):
        flag = False
        mb.showerror("Error", "Шаг не может превосходить размер интервала!")
    if (error > 0.0001):
        flag = False
        mb.showwarning("Warning", "Метод Рунге - Кутта довольно точный, поэтому не рекомендуется ставить погрешность выше 0.0001")
    #printInfo()
    if flag :
        res_x, res_y, res_z = [], [] ,[]
        res_x, res_y, res_z = RungeKutta(begin, end, y, pr_y, error, step,sigma)

        mng = plt.get_current_fig_manager()
        mng.resize(1000, 600)


        plt.subplot(121)
        plt.title("Частные решения")
        plt.grid(True)
        ax1 = plt.gca()
        st = "x="+str(y)+" x'="+str(pr_y)+" k="+str(sigma)
        ax1.axhline(y=0, color='k')
        ax1.axvline(x=0, color='k')
        ax1.set_xlabel('t')
        ax1.set_ylabel('x')
        ax1.plot(res_x, res_y, label = st)
        ax1.legend()


        plt.subplot(122)
        plt.title("Фазовый портрет")
        plt.grid(True)
        ax2 = plt.gca()
        faz_x, faz_y, faz_z = [], [] ,[]
        for i in range(-3, 4):
             faz_x, faz_y, faz_z = RungeKutta(begin, end, y, i, error, step,sigma)
             ax2.plot(faz_y, faz_z, color = '#0a0b0c')
             faz_x, faz_y, faz_z = RungeKutta(begin, end, i, pr_y, error, step,sigma)
             ax2.plot(faz_y, faz_z, color = '#0a0b0c')
        ax2.axhline(y=0, color='k')
        ax2.axvline(x=0, color='k')
        ax2.set_xlabel('x')
        ax2.set_ylabel("x'")
        plt.show()

def printInfo():
    print(y,pr_y,step,sigma,error, begin, error)

def f(x, y, z , sigma):
    return Decimal(-sigma) * z - Decimal(math.sin(y))

def g(x, y, z):
    return z

def RungeKutta(begin, end, first, second, error, step, sigma):
    count = int((end - begin) / step)
    x = [begin]
    y = [first]
    z = [second]
    for i in range(0,count+1):
        k1 = g(x[i], y[i], z[i])
        l1 = f(x[i], y[i], z[i], sigma)
        k2 = g(x[i] + step/2, y[i] + (step * k1/2), z[i] + (step * l1/2))
        l2 = f(x[i] + step/2, y[i] + (step * k1/2), z[i] + (step * l1/2), sigma)
        k3 = g(x[i] + step/2, y[i] + (step * k2/2), z[i] + (step * l2/2))
        l3 = f(x[i] + step/2, y[i] + (step * k2/2), z[i] + (step * l2/2), sigma)
        k4 = g(x[i] + step, y[i] + (step * k3), z[i] + (step * l3))
        l4 = f(x[i] + step, y[i] + (step * k3), z[i] + (step * l3), sigma)
        tmp_y = y[i] + ((k1 + 2 * k2 + 2 * k3 + k4) * step) / 6 + error
        tmp_z = z[i] + ((l1 + 2 * l2 + 2 * l3 + l4) * step) / 6
        x.append(x[i]+step)
        y.append(tmp_y)
        z.append(tmp_z)
    return x, y, z

#Design main menu
root =  Tk()
root.title('Метод Рунге-Кутты')
root.geometry("250x250")
root.resizable(width=False, height=False)

#Labels
equation_lbl= Label(root, text = "x''+ k*x' + sin x = 0", font='Arial 13')
y_lbl = Label(root, text = "x")
pr_y_lbl = Label (root , text="x'")
step_lbl = Label(root, text="Шаг")
sigma_lbl = Label(root, text="k")
error_lbl = Label(root, text="Погрешность")
begin_lbl = Label(root, text="От")
end_lbl = Label(root, text="До")

equation_lbl.place(relx = .3, rely = .05)
y_lbl.place(relx = .3, rely = .15)
pr_y_lbl.place(relx = .3, rely = .25)
step_lbl.place(relx = .3, rely = .35)
sigma_lbl.place(relx = .3, rely = .45)
error_lbl.place(relx = .2, rely = .55)
begin_lbl.place(relx = .2, rely = .65)
end_lbl.place(relx = .55, rely = .65)

#Entry
y_e= Entry(root, width = 10)
pr_y_e = Entry(root, width = 10)
step_e = Entry(root, width = 10)
sigma_e = Entry(root, width = 10)
error_e = Entry(root, width = 10)
begin_e = Entry(root, width = 7)
end_e = Entry(root, width = 7)

y_e.insert(0, y)
pr_y_e.insert(0,pr_y)
step_e.insert(0, step)
sigma_e.insert(0,sigma)
error_e.insert(0, error)
begin_e.insert(0, begin)
end_e.insert(0, end)

y_e.place(relx = .6, rely = .15)
pr_y_e.place(relx = .6, rely = .25)
step_e.place(relx = .6, rely = .35)
sigma_e.place(relx = .6, rely = .45)
error_e.place(relx = .6, rely = .55)
begin_e.place(relx = .3, rely = .65)
end_e.place(relx = .65, rely = .65)

#Button
build_draw_btn = Button(root, text="Нарисовать", command = check)
build_draw_btn.place(relx = .35, rely = .8)

root.mainloop()
