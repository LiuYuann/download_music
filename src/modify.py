from subprocess import Popen, PIPE
from os import remove, rename


class Modification():
    def __init__(self):
        self.command1 = 'ffmpeg.exe -i ../song/%(id)d.mp3 -metadata title="%(name)s" -metadata artist="%(artist)s" ../song/%(id)d1.mp3'
        self.command2 = 'ffmpeg.exe -y -i ../song/%(id)d1.mp3 -i  ../song/%(id)d.jpg -map 0:0 -map 1:0 -c copy -id3v2_version 3 ../song/%(id)d.mp3'

    def modify(self, d):
        cwd = '../src/'
        mystr1 = Popen(
            self.command1 % {'id': d['id'], 'name': d['name'], 'artist': d['artist']},
            shell=True, cwd=cwd, stdout=None, stderr=PIPE)
        mystr1.communicate()
        if mystr1.returncode == 0:
            mystr2 = Popen(
                self.command2 % {'id': d['id']},
                shell=True, cwd=cwd)
            mystr2.communicate()
            remove('./{}1.mp3'.format(d['id']))
            remove('./' + str(d['id']) + '.jpg')
            try:
                rename('./' + str(d['id']) + '.mp3', d['name'] + '.mp3')
            except FileExistsError:
                rename('./' + str(d['id']) + '.mp3', d['name'] + '--' + d['artist'] + '.mp3')
            if mystr2.returncode == 0:
                return '{}下载成功'.format(d['name'])
            else:
                remove(d['name'] + '.lrc')
                return '{}下载失败1'.format(d['name'])
        else:
            remove('./{}.mp3'.format(d['id']))
            remove('./' + str(d['id']) + '.jpg')
            remove(d['name'] + '.lrc')
            return '{}下载失败2'.format(d['name'])
