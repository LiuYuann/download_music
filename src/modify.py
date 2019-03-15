from subprocess import Popen, PIPE
from os import getcwd, remove, rename


class Modification():
    def __init__(self):
        self.command1 = 'ffmpeg -i %(id)d.mp3 -metadata title="%(name)s" -metadata artist="%(artist)s" %(id)d1.mp3'
        self.command2 = 'ffmpeg -y -i %(id)d1.mp3 -i  %(id)d.jpg -map 0:0 -map 1:0 -c copy -id3v2_version 3 %(id)d.mp3'

    def modify(self, d):
        cwd = getcwd()
        mystr1 = Popen(
            self.command1 % {'id': d['id'], 'name': d['name'], 'artist': d['artist']},
            shell=True, cwd=cwd, stdout=None, stderr=PIPE)
        mystr1.communicate()
        if mystr1.returncode == 0:
            mystr2 = Popen(
                self.command2 % {'id': d['id']},
                shell=True, cwd=cwd, stdout=None, stderr=PIPE)
            mystr2.communicate()
            remove('./{}1.mp3'.format(d['id']))
            remove('./' + str(d['id']) + '.jpg')
            try:
                rename('./' + str(d['id']) + '.mp3', d['name'] + '.mp3')
            except FileExistsError:
                rename('./' + str(d['id']) + '.mp3', d['name']+'--'+d['artist'] + '.mp3')
            if mystr2.returncode == 0:
                return '{}下载成功'.format(d['name'])
            else:
                remove(d['name'] + '.lrc')

                return '{}下载失败'.format(d['name'])
        else:
            remove('./{}.mp3'.format(d['id']))
            remove('./' + str(d['id']) + '.jpg')
            remove(d['name'] + '.lrc')
            return '{}下载失败'.format(d['name'])
