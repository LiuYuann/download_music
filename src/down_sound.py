import aiohttp


class Download_sound():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    async def __get_content(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                result = await response.read()
        return result

    async def get(self, d):
        url = 'http://music.163.com/song/media/outer/url?id={}'.format(d['id'])
        sound_content = await self.__get_content(url)
        with open(str(d['id']) + '.mp3', 'wb') as f:
            f.write(sound_content)
        return '{}下载成功'.format(d['name'])
