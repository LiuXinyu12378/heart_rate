import random

import tkinter.messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import numpy as np
import tkinter as tk
from PIL import Image
from heartrate_monitor import run_sensor
from get_data import measure

window = tk.Tk()      #创建一个TK对象
window.title('高精度脉搏检测仪')    #设置窗口名称
window.geometry('1000x900')    #设置窗口大小

def do_job():
    tk.messagebox.showinfo(title='说明', message='测量脉搏，使用高性能树莓派4b处理器和高精度血氧模块，可实时测量，保存数据信息，可以根据脉搏估计血压')  # 提示信息

#---------------------------------------------菜单
menubar = tk.Menu(window)   #创建menu菜单


#---------------------------------------------用户信息

filemenu = tk.Menu(menubar,tearoff=0)  #创建filemenu菜单
menubar.add_cascade(label='File',menu=filemenu)  #添加filemenu菜单到menu菜单
filemenu.add_command(label='说明',command=do_job)   #添加New选项到filemenu菜单
filemenu.add_separator()                            #添加分割符------
filemenu.add_command(label='退出',command=window.quit)   #添加退出选项到filemenu菜单

tk.Label(window,text='用户信息登记',bg='yellow',font=('SimHei',18),width=15,height=1).place(x=400,y=10)
tk.Label(window,text='姓名:').place(x=200,y=50)
tk.Label(window,text='年龄:').place(x=200,y=80)
tk.Label(window,text='性别:').place(x=200,y=110)
tk.Label(window,text='登记号:').place(x=200,y=140)

var_usr_name = tk.StringVar()
var_usr_age = tk.StringVar()
var_usr_gender = tk.IntVar()
GIRLS = [("男", 1),("女", 2)]
var_usr_id = tk.StringVar()
var_usr_id.set(1)
entry_usr_name = tk.Entry(window,textvariable=var_usr_name).place(x=300,y=50)
entry_usr_age = tk.Entry(window,textvariable=var_usr_age).place(x=300,y=80)
for idx,(girl, num) in enumerate(GIRLS):
    b = tk.Radiobutton(window, text=girl, variable=var_usr_gender, value=num)
    if idx ==0:
        b.place(x=300, y=110)
    else:
        b.place(x=350,y=110)
entry_usr_id = tk.Entry(window,textvariable=var_usr_id).place(x=300,y=140)


tk.Label(window,text='脉搏:').place(x=550,y=50)
tk.Label(window,text='均值:').place(x=550,y=80)
tk.Label(window,text='估计高压:').place(x=550,y=110)
tk.Label(window,text='估计低压:').place(x=550,y=140)
var_pix = tk.IntVar()     #一个tk自带类型的string变量
var_ave_pix = tk.IntVar()    #一个tk自带类型的string变量
var_high = tk.IntVar()    #一个tk自带类型的string变量
var_low = tk.IntVar()    #一个tk自带类型的string变量
pix = tk.Label(window,textvariable=var_pix,bg='blue',font=('Arial',12),width=10,height=1).place(x=650,y=50)    #设定一个label标签
ave_pix = tk.Label(window,textvariable=var_ave_pix,bg='blue',font=('Arial',12),width=10,height=1).place(x=650,y=80)    #设定一个label标签
high_val = tk.Label(window,textvariable=var_high,bg='blue',font=('Arial',12),width=10,height=1).place(x=650,y=110)    #设定一个label标签
low_val = tk.Label(window,textvariable=var_low,bg='blue',font=('Arial',12),width=10,height=1).place(x=650,y=140)    #设定一个label标签

#------------------------------------------------------画图区域

frame1 = Frame(window, bg="#ffffff")
frame1.place(x=50, y=200, width=900, height=600)
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
fig = plt.figure(figsize=(9,6), edgecolor='blue')
canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.draw()
canvas.get_tk_widget().place(x=10, y=0)

t_list = []
result_list = []
t = 0
def usr_measuring():
    info = usr_save()
    if info != 0:
        drawImg()
        with open("users_info/用户信息.txt",'a',encoding='utf-8') as f_write:
            f_write.write(info+" "+str(var_ave_pix.get())+" "+str(var_high.get())+" "+str(var_low.get())+'\n')
        tk.messagebox.showinfo(title='提示', message='用户信息更新成功！')
    elif info == 0:
        tk.messagebox.showerror(title='提示', message='请输入用户信息！')

def drawImg():
    global t
    global t_list
    global result_list
    global var_pix,var_ave_pix
    global fig,canvas
    pix_values = run_sensor()

    plt.close(fig)
    canvas.close_event()
    canvas.flush_events()
    fig = plt.figure(figsize=(9, 6), edgecolor='blue')
    canvas = FigureCanvasTkAgg(fig, master=frame1)
    canvas.draw()
    canvas.get_tk_widget().place(x=10, y=0)
    for t in range(100):
        t_list.append(t)
        pix_value = pix_values[t]
        var_pix.set(np.int(pix_value))
        result_list.append(pix_value)
        var_ave_pix.set(np.int(np.mean(result_list)))
        low, high = measure(np.int(np.int(np.mean(result_list))))
        var_high.set(np.int(high))
        var_low.set(np.int(low))
        if len(t_list) > 60:
            plt.clf()
            t_list = t_list[:]
            result_list = result_list[:]
        plt.plot(t_list, result_list, c='r', ls='-', marker='o', mec='b', mfc='w')  ## 保存历史数据

        canvas.draw()
    plt.savefig("users_pic/"+var_usr_name.get() + var_usr_id.get()+".png")
    afterHandler = window.after(60, drawImg)
    window.after_cancel(afterHandler)

def usr_find():
    window_find = tk.Toplevel(window)     #在原窗口的基础上创建一个新的窗口
    window_find.geometry('550x200')
    window_find.title('用户查找')

    usr_name = tk.StringVar()
    usr_id = tk.StringVar()
    tk.Label(window_find,text='姓名:').place(x=10,y=10)
    entry_name = tk.Entry(window_find,textvariable=usr_name).place(x=150,y=10)
    tk.Label(window_find,text='登记号:').place(x=10,y=40)
    entry_id = tk.Entry(window_find,textvariable=usr_id).place(x=150,y=40)

    def start_find():
        if usr_id.get() == '' or usr_name.get() == '':
            tk.messagebox.showinfo(title='提示', message='请输入姓名和登记号')
        else:
            #try:
            with open('users_info/用户信息.txt','r',encoding="utf-8") as usr_file:
                lines = usr_file.readlines()
            for line in lines:
                id,name,age,gender,pix,high,low = line.strip().split()
                if id == usr_id.get() and name == usr_name.get():
                    tk.Label(window_find, bg='yellow',font=28,text='姓名:{} 性别:{} 年龄:{} 登记号:{} 心率:{} 估计高压:{} 估计低压:{}'.format(name,gender,age,id,pix,high,low)).place(x=25, y=100)
                    im = Image.open('users_pic/'+name+id+'.png')
                    im.show()

            # except :
            #     tk.messagebox.showinfo(title='结果', message='没有找到用户'+usr_name.get()+'信息')

    button_find = tk.Button(window_find, text='查找', command=start_find).place(x=200, y=150)

def usr_save():
    usr_name = var_usr_name.get()
    usr_age = var_usr_age.get()
    usr_gender = "男" if var_usr_gender.get() ==1 else "女"
    usr_id = var_usr_id.get()

    if all([usr_name,usr_age,usr_gender,usr_id]):

        usr_info = usr_id+" "+usr_name+" "+usr_age+" "+usr_gender
        print(usr_info)
        try:
            with open('users_info/用户信息.txt','a',encoding="utf-8") as usr_file:
                pass
        except :
            with open('users_info/用户信息.txt','w',encoding="utf-8") as usr_file:
                pass
        return usr_info
    else:
        return 0


btn_measuring = tk.Button(window,text='测量并保存',command=usr_measuring).place(x=400,y=820)
btn_find = tk.Button(window,text='查找',command=usr_find).place(x=500,y=820)

window.config(menu=menubar)   #配置menubar菜单到窗口

window.mainloop()    #窗口不断刷新