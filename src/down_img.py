import aiohttp


class Download_img():
    async def __get_content(self,url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.read()
        return result

    async def get(self, d):
        url = d['pic_url']
        image_content = await self.__get_content(url)
        with open(str(d['id']) + '.jpg', 'wb') as f:
            f.write(image_content)