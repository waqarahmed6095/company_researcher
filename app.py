from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request  # Import Request here
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import markdown2  # Import markdown2 to render markdown to HTML
from backend.graph import Graph  # Adjust this import if necessary 

from dotenv import load_dotenv
load_dotenv('.env')

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):  # Add the type hint here
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Receive initial data from the WebSocket client
        data = await websocket.receive_json()
        company_name = data.get("companyName")
        company_url = data.get("companyUrl")
        output_format = data.get("outputFormat", "pdf")
        
        # Initialize the Graph with company, URL, and output format
        graph = Graph(company=company_name, url=company_url, output_format=output_format, websocket=websocket)
        
        # Progress callback to send messages back to the client
        async def progress_callback(message):
            await websocket.send_text(message)

        # Run the graph process without additional arguments
        await graph.run(progress_callback=progress_callback)

        await websocket.send_text("Research completed.")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        timeout_keep_alive=1020  # Increase timeout to 120 seconds (or any value you prefer)
    )
