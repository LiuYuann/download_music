import aiohttp
import json


class Download_lyc():
    async def __get_content(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.read()
        return result

    async def get(self, d):
        url = 'http://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=1'.format(d['id'])
        content = await self.__get_content(url)
        lyc = json.loads(content).get("lrc").get("lyric")
        lyc_head = "[ar:{}]\n[ti:{}]\n[al:{}]\n[by:Marcus]\n".format(d['artist'], d['name'], d['album'])
        with open(d['name'] + '.lrc', 'w', encoding='utf-8') as f:
            f.write(lyc_head + lyc)
