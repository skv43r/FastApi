import aiohttp
import aiofiles
import json
import os

class DataService:
    def __init__(self, api_url: str, storage_path: str = "public"):
        self.api_url = api_url
        self.storage_path = storage_path

    async def fetch_data(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to fetch data: {response.status}")
    
    async def save_json(self, data: dict, file_name: str = "data.json") -> None:
        async with aiofiles.open(file_name, "w") as file:
            await file.write(json.dumps(data, indent=4))

    async def download_image(self, url: str, file_name: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    file_path = os.path.join(self.storage_path, file_name)
                    async with aiofiles.open(file_path, "wb") as image_file:
                        content = await response.read()
                        await image_file.write(content)
                else:
                    raise Exception(f"Failed to download image: {response.status}")