"""
FastAPI web application for rFactor Championship Creator.

Main application file that sets up routes, middleware, and static files.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from .routes import talents, championships, championship_creator, import_export, config as config_routes, vehicles, tracks
from ..__version__ import __version__

# Create FastAPI app
app = FastAPI(
    title="rFactor Championship Creator",
    description="Web interface for managing rFactor championships and talents",
    version=__version__,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# React build directory (production)
REACT_BUILD_DIR = BASE_DIR.parent.parent / "frontend" / "dist"

# Mount static files (old templates - keeping for backward compatibility)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Serve React build in production
if REACT_BUILD_DIR.exists():
    # Mount React static assets
    app.mount("/assets", StaticFiles(directory=str(REACT_BUILD_DIR / "assets")), name="react-assets")

# Setup templates (old Jinja2 templates - keeping for backward compatibility)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Include routers
app.include_router(talents.router, prefix="/api/talents", tags=["Talents"])
app.include_router(championships.router, prefix="/api/championships", tags=["Championships"])
app.include_router(championship_creator.router, prefix="/api/championships", tags=["Championship Creator"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["Vehicles"])
app.include_router(import_export.router, prefix="/api", tags=["Import/Export"])
app.include_router(config_routes.router, prefix="/api/config", tags=["Configuration"])
app.include_router(tracks.router, prefix="/api/tracks", tags=["Tracks"]) 


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Serve React app in production, fallback to old template in dev.
    """
    # Check if React build exists (production mode)
    react_index = BASE_DIR.parent.parent / "frontend" / "dist" / "index.html"

    if react_index.exists():
        # Production: Serve React build
        with open(react_index, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    else:
        # Development: Redirect to React dev server or show message
        return HTMLResponse(content="""
            <html>
                <head>
                    <title>rFactor Championship Creator</title>
                    <style>
                        body {
                            background: #0A0A0A;
                            color: #fff;
                            font-family: 'Segoe UI', sans-serif;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            height: 100vh;
                            margin: 0;
                        }
                        .container {
                            text-align: center;
                            padding: 2rem;
                        }
                        h1 { color: #E31E24; }
                        a {
                            color: #00D9FF;
                            text-decoration: none;
                            font-weight: bold;
                        }
                        .code {
                            background: #1F1F1F;
                            padding: 1rem;
                            border-left: 4px solid #E31E24;
                            margin: 1rem 0;
                            text-align: left;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>🏎️ rFactor Championship Creator</h1>
                        <h2>Mode Développement</h2>
                        <p>L'application React tourne sur un serveur séparé en développement.</p>
                        <div class="code">
                            <p><strong>Option 1 - Accéder au frontend React :</strong></p>
                            <p>→ <a href="http://localhost:3000" target="_blank">http://localhost:3000</a></p>
                        </div>
                        <div class="code">
                            <p><strong>Option 2 - Build production :</strong></p>
                            <p>cd frontend && npm run build</p>
                            <p>Puis rechargez cette page</p>
                        </div>
                        <div class="code">
                            <p><strong>API Documentation :</strong></p>
                            <p>→ <a href="/api/docs">/api/docs</a></p>
                        </div>
                    </div>
                </body>
            </html>
        """)


@app.get("/talents", response_class=HTMLResponse)
async def talents_page(request: Request):
    """Talents list page."""
    return templates.TemplateResponse("talents/list.html", {"request": request})


@app.get("/talents/new", response_class=HTMLResponse)
async def talent_new_page(request: Request):
    """Talent creation page."""
    return templates.TemplateResponse("talents/form.html", {"request": request, "mode": "create"})


@app.get("/talents/{name}/edit", response_class=HTMLResponse)
async def talent_edit_page(request: Request, name: str):
    """Talent edit page."""
    return templates.TemplateResponse("talents/form.html", {"request": request, "mode": "edit", "talent_name": name})


@app.get("/talents/{name:path}", response_class=HTMLResponse)
async def talent_detail_page(request: Request, name: str):
    """Talent detail page."""
    # Redirect special routes
    if name == "new":
        return await talent_new_page(request)
    if name.endswith("/edit"):
        talent_name = name.replace("/edit", "")
        return await talent_edit_page(request, talent_name)
    return templates.TemplateResponse("talents/detail.html", {"request": request, "talent_name": name})


@app.get("/championships", response_class=HTMLResponse)
async def championships_page(request: Request):
    """Championships list page."""
    return templates.TemplateResponse("championships/list.html", {"request": request})


@app.get("/championships/create/new", response_class=HTMLResponse)
async def championship_create_page(request: Request):
    """Custom championship creation page."""
    return templates.TemplateResponse("championships/create.html", {"request": request})


@app.get("/championships/{name}", response_class=HTMLResponse)
async def championship_detail_page(request: Request, name: str):
    """Championship detail page."""
    return templates.TemplateResponse("championships/detail.html", {"request": request, "championship_name": name})


@app.get("/vehicles", response_class=HTMLResponse)
async def vehicles_page(request: Request):
    """Vehicles list page."""
    return templates.TemplateResponse("vehicles/list.html", {"request": request})


@app.get("/vehicles/{path:path}", response_class=HTMLResponse)
async def vehicle_detail_page(request: Request, path: str):
    """Vehicle detail page."""
    return templates.TemplateResponse("vehicles/detail.html", {"request": request, "vehicle_path": path})


@app.get("/tracks", response_class=HTMLResponse)
async def tracks_page(request: Request):
    """Tracks list page."""
    return templates.TemplateResponse("tracks/list.html", {"request": request})


@app.get("/tracks/{path:path}", response_class=HTMLResponse)
async def track_detail_page(request: Request, path: str):
    """Track detail page."""
    return templates.TemplateResponse("tracks/detail.html", {"request": request, "track_path": path})


@app.get("/import", response_class=HTMLResponse)
async def import_page(request: Request):
    """CSV import page."""
    return templates.TemplateResponse("import.html", {"request": request})


@app.get("/config", response_class=HTMLResponse)
async def config_page(request: Request):
    """Configuration page."""
    return templates.TemplateResponse("config.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "rFactor Championship Creator"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
