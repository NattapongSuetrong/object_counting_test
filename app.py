# import RPi.GPIO as GPIO
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from detectionV3 import ObjectCounter
import systems
import cv2

# GPIO.setmode(GPIO.BCM)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

#recieve which pin to change from the button press on index.html
#each button returns a number that triggers a command in this function

@app.post("/status/{status}")
def recieve_status(status: str):
    if status == 'ON':
        systems.Start()
        print('ON')
    elif status == 'OFF':
        systems.Stop()
    else:
        raise HTTPException(status_code=404, detail="Status not found")
    
    return {"message": f"Status {status} processed successfully"}
    
    # return RedirectResponse(url="/") # redirect to the home page

@app.get("/video")
async def video_feed():
    counter = ObjectCounter(0, "object_counting_output.avi")
    return StreamingResponse(counter.process_video(), media_type="multipart/x-mixed-replace; boundary=frame")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)