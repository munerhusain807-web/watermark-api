from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import subprocess, os, uuid

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    filename = str(uuid.uuid4()) + ".mp4"
    input_path = f"uploads/{filename}"
    output_path = f"outputs/processed_{filename}"
    with open(input_path, "wb") as f:
        f.write(await file.read())
    subprocess.run(["ffmpeg", "-i", input_path, "-vf", "delogo=x=W-200:y=0:w=200:h=60:show=0", output_path])
    return {"status": "done", "output": "processed_" + filename}

@app.get("/download/{filename}")
async def download(filename: str):
    return FileResponse(f"outputs/{filename}", media_type="video/mp4", filename=filename)
