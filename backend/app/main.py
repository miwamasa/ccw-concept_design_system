"""Main FastAPI application for Concept Design Support System."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from .services.design_exploration import DesignExplorationEngine
from .services.graph_conversion import GraphConversionEngine

app = FastAPI(
    title="Concept Design Support System",
    description="API for component-based concept design visualization",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instances
design_engine = DesignExplorationEngine()
conversion_engine = GraphConversionEngine()


# Request/Response models
class ExplorationRequest(BaseModel):
    """Request model for design exploration."""
    initial_system: str
    situation: Optional[str] = None
    problem: Optional[str] = None
    intention: Optional[str] = None


class GraphResponse(BaseModel):
    """Response model for graph data."""
    type: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    hierarchies: Optional[Dict[str, List[str]]] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Concept Design Support System API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "explore": "/api/explore",
            "de_graph": "/api/graphs/de",
            "ld_graph": "/api/graphs/ld",
            "si_graph": "/api/graphs/si",
            "convert": "/api/convert"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/explore", response_model=GraphResponse)
async def explore_design(request: ExplorationRequest):
    """Execute design exploration and return DE graph.

    Args:
        request: Exploration request with initial system

    Returns:
        DE graph data
    """
    try:
        # Reset engine
        design_engine.reset()

        # Execute exploration
        de_graph = design_engine.explore(request.initial_system)

        # Convert to response format
        graph_dict = de_graph.to_dict()

        return GraphResponse(
            type=graph_dict["type"],
            nodes=graph_dict["nodes"],
            edges=graph_dict["edges"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/graphs/de", response_model=GraphResponse)
async def get_de_graph():
    """Get current DE graph.

    Returns:
        DE graph data
    """
    try:
        de_graph = design_engine.get_graph()
        graph_dict = de_graph.to_dict()

        return GraphResponse(
            type=graph_dict["type"],
            nodes=graph_dict["nodes"],
            edges=graph_dict["edges"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/graphs/ld", response_model=GraphResponse)
async def get_ld_graph():
    """Get LD graph converted from current DE graph.

    Returns:
        LD graph data
    """
    try:
        de_graph = design_engine.get_graph()

        # Convert to LD graph
        ld_graph = conversion_engine.convert_de_to_ld(de_graph)
        graph_dict = ld_graph.to_dict()

        return GraphResponse(
            type=graph_dict["type"],
            nodes=graph_dict["nodes"],
            edges=graph_dict["edges"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/graphs/si", response_model=GraphResponse)
async def get_si_graph():
    """Get SI graph converted from current DE graph.

    Returns:
        SI graph data
    """
    try:
        de_graph = design_engine.get_graph()

        # Convert to SI graph
        si_graph = conversion_engine.convert_de_to_si(de_graph)
        graph_dict = si_graph.to_dict()

        return GraphResponse(
            type=graph_dict["type"],
            nodes=graph_dict["nodes"],
            edges=graph_dict["edges"],
            hierarchies=graph_dict.get("hierarchies")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/convert", response_model=Dict[str, GraphResponse])
async def convert_graphs():
    """Convert current DE graph to LD and SI graphs.

    Returns:
        All three graph representations
    """
    try:
        de_graph = design_engine.get_graph()

        # Get DE graph
        de_dict = de_graph.to_dict()

        # Convert to LD
        ld_graph = conversion_engine.convert_de_to_ld(de_graph)
        ld_dict = ld_graph.to_dict()

        # Convert to SI
        si_graph = conversion_engine.convert_de_to_si(de_graph)
        si_dict = si_graph.to_dict()

        return {
            "de": GraphResponse(
                type=de_dict["type"],
                nodes=de_dict["nodes"],
                edges=de_dict["edges"]
            ),
            "ld": GraphResponse(
                type=ld_dict["type"],
                nodes=ld_dict["nodes"],
                edges=ld_dict["edges"]
            ),
            "si": GraphResponse(
                type=si_dict["type"],
                nodes=si_dict["nodes"],
                edges=si_dict["edges"],
                hierarchies=si_dict.get("hierarchies")
            )
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/component-types")
async def get_component_types():
    """Get available component types.

    Returns:
        Lists of DE and SI component types
    """
    return {
        "de_components": [
            {"type": "SI", "name": "Situation Assessment"},
            {"type": "PI", "name": "Problem Identification"},
            {"type": "EI", "name": "Establish Intention"},
            {"type": "DI", "name": "Decompose Intention"},
            {"type": "CB", "name": "Conditional Branch"},
            {"type": "SA", "name": "Solution Assignment"}
        ],
        "si_components": [
            {"type": "CND", "name": "Condition"},
            {"type": "BUP", "name": "Backups"},
            {"type": "COL", "name": "Collaboration"},
            {"type": "ALT", "name": "Alternative"},
            {"type": "EXO", "name": "Exclusive"}
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
