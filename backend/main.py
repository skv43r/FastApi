from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import aiohttp
import json
import os
import aiofiles
import uvicorn

app = FastAPI()

if not os.path.exists("public"):
    os.makedirs("public")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="static")

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
async def main_page(request: Request):
    try:
        async with aiofiles.open("data.json", "r") as file:
                data = json.loads(await file.read())
                ids = [user["id"] for user in data["users"]]
                names = [user["name"] for user in data["users"]]
                emails = [user["email"] for user in data["users"]]

                
                return templates.TemplateResponse("index.html", {
                    "request": request,
                    "ids": ids,
                    "names": names,
                    "emails": emails
                })
    except Exception as e:
        return HTMLResponse(content=f"Error: {str(e)}")
    
if  __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
