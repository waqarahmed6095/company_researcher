from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .graph import Graph  # Adjust this import if necessary

app = FastAPI()

# Specify the template folder (replace 'frontend/templates' with your actual path)
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Render the HTML template with the form
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/research")
async def company_research(companyName: str = Form(...), companyUrl: str = Form(...), outputFormat: str = Form("pdf")):
    # Initialize and run the graph for the specified company and URL
    graph = Graph()
    await graph.run(company=companyName, url=companyUrl, output_format=outputFormat)
    return {"message": "Research completed", "output_format": outputFormat}
