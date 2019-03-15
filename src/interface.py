from math import ceil
from tkinter import *
from tkinter.messagebox import askyesno, showwarning, showinfo
from .songinfomation import *
from .scheduler import *


class Interface():

    def __init__(self):
        self.__songinfo = SongInformation()
        self.sch = Scheduler()
        self.__master = Tk()
        self.__v = IntVar()
        self.__v.set(value=30)  # 记录当前页码
        self.__frame1 = Frame(self.__master)
        self.__frame1.pack()
        self.__label = Label(self.__frame1, text='关键词：')
        self.__label.grid(row=0, column=0)
        self.__e = Entry(self.__frame1)
        self.__e.grid(row=0, column=1)
        self.__e.insert(0, "泫雅")
        self.__song_list = self.__songinfo.get_info(self.__e.get())
        song_count = self.__song_list["songCount"]
        self.__pages = ceil(song_count / 30)
        Label(self.__frame1, text='         ').grid(row=0, column=2)
        self.__search_button = Button(self.__frame1, text='搜索', relief='raised', command=self.__search)
        self.__search_button.grid(row=0, column=3)
        self.__frame2 = Frame(self.__master)
        self.__frame2.pack()
        self.__sb = Scrollbar(self.__frame2)
        self.__listb = Listbox(self.__frame2, height=20, width=60, selectmode="extended")
        self.__DATA = self.__song_list['songs']
        for i in self.__DATA:
            self.__listb.insert(END, i["name"] + '--' + i["ar"][0]["name"])
        self.__listb.pack(side=LEFT)
        self.__sb.pack(side=RIGHT, fill=Y)
        self.__sb.config(command=self.__listb.yview)
        self.__next_Button = Button(self.__master, text="下一页", command=self.__next_page)
        self.__next_Button.pack()
        self.__download_Button = Button(self.__master, text="下载", command=self.download)
        self.__download_Button.pack()
        self.__master.mainloop()

    def __search(self):
        page = 0
        self.__v.set(page)
        self.__listb.delete(0, END)
        song_list = self.__songinfo.get_info(self.__e.get(), page)
        self.__DATA = song_list['songs']
        for i in self.__DATA:
            self.__listb.insert(END, i["name"] + '--' + i["ar"][0]["name"])
        self.__v.set(page)

    def __next_page(self):
        page = self.__v.get() + 30
        song_list = self.__songinfo.get_info(self.__e.get(), page)
        self.__DATA += song_list['songs']
        for i in song_list['songs']:
            self.__listb.insert(END, i["name"] + '--' + i["ar"][0]["name"])
        self.__v.set(page)

    def download(self):
        m = askyesno('提示', '要下载选中的歌曲吗?')  # 确认是否要下载
        if m:
            songs = []
            for i in self.__listb.curselection():
                # print(self.__listb.get(i))
                self.__listb.selection_clear(i)
                copyright = self.__DATA[i]['privilege']['fee']
                if copyright == 8:
                    song = {
                        'name': self.__DATA[i]['name'].replace(' ', ''),  # 删去字符串内部空格，防止在命令中出现参数错误
                        'id': self.__DATA[i]['id'],
                        'pic_url': self.__DATA[i]['al']['picUrl'] + '?param=100y100',
                        'copyright': self.__DATA[i]['privilege']['fee'],
                        'artist': '/'.join([j['name'] for j in self.__DATA[i]['ar']]),
                        'album': self.__DATA[i]['al']['name'].replace(' ', '')
                    }
                    showinfo('信息', song['name'] + '正在下载......')
                    songs.append(song)
                else:
                    showwarning('提示', '歌曲《{}》因为没有版权，无法下载'.format(self.__DATA[i]['name']))
            if songs:
                res = self.sch.run(songs)
            else:
                res = ['下载失败']
            showinfo('下载结果', '\n'.join(res))
