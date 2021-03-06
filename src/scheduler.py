import asyncio
import time
from os import chdir, mkdir
from multiprocessing import Pool
from os.path import exists
from .down_lyc import *
from .down_img import *
from .down_sound import *
from .modify import *


class Scheduler():
    def __init__(self):
        # self.start = time.clock()
        if not exists('song'):
            mkdir('song')
        chdir('./song')

    def run(self, data):
        lyc = Download_lyc()
        img = Download_img()
        sound = Download_sound()
        modifier = Modification()
        lyc_tasks = [asyncio.ensure_future(lyc.get(d)) for d in data if d['d_lyc']]
        sound_tasks = [asyncio.ensure_future(sound.get(d)) for d in data]
        img_tasks = [asyncio.ensure_future(img.get(d)) for d in data if d['add_info']]
        download_task = lyc_tasks + img_tasks + sound_tasks  # 下载歌词、图片、歌曲
        if download_task:
            download_loop = asyncio.get_event_loop()
            download_loop.run_until_complete(asyncio.wait(download_task))
        res = []
        p = Pool(processes=len(sound_tasks))
        obj_l = []
        for d in data:
            if d['add_info']:  # 若勾选增加歌曲标签信息
                obj = p.apply_async(modifier.add_metadata, args=(d,))
                obj_l.append(obj)
            else:  # 重命名歌曲
                obj = p.apply_async(modifier.rename_file, args=(d,))
                obj_l.append(obj)
        p.close()
        p.join()
        for obj in obj_l:
            res.append(obj.get())
        print('用时{}s'.format(time.clock()))
        return res
