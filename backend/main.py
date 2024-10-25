from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import aiohttp
import json
import os
import aiofiles
import requests
import uvicorn

app = FastAPI()

if not os.path.exists("backend/public"):
    os.makedirs("public")

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
app.mount("/public", StaticFiles(directory="backend/public"), name="public")

@app.get("/external-data")
async def get_external_data():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://api.npoint.io/88fcfcbf4fde970ba6f2") as response:
                data = await response.json()
                async with aiofiles.open ("data.json", "w") as file:
                    await file.write(json.dumps(data, indent=4))


                for user in data["users"]:
                    avatar_url = user["avatar"] 
                    user_id = user["id"]

                    file_name = f"user_{user_id}.jpg"
                    file_path = os.path.join("public", file_name)

                    async with session.get(avatar_url) as img_response:
                        if img_response.status == 200:
                            async with aiofiles.open(file_path, "wb") as image_file:
                                content = await img_response.read()
                                await image_file.write(content)
                        else:
                            return {"error": f"Failed to download image for user {user_id}"}


                return data
        except Exception as e:
            return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
async def main_page():
    async with aiofiles.open("backend/static/index.html", "r") as file:
        html_content = await file.read()
    return HTMLResponse(content=html_content)

if  __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# @app.get("/test")
# def get_data():
#     try:
#         response = requests.get("https://api.npoint.io/88fcfcbf4fde970ba6f2")
#         data = response.json()
#         with open ("data.json", "w") as file:
#             json.dump(data, file, indent=4)

#         for user in data["users"]:
#             avatar_link = user["avatar"]
#             user_id = user["id"]

#             file_name = f"user_{user_id}.jpg"
#             file_path = os.path.join("public", file_name)
            
#             requests.get(avatar_link)
#             with open(file_path, "wb") as img:
#                 img.write(requests.get(avatar_link).content)

#         return {"message": "JSON and images saved to public folder"}
#     except Exception as e:
#         return {"error": str(e)}
