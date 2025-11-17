"""Main FastAPI application for Concept Design Support System."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from .services.design_exploration import DesignExplorationEngine
from .services.graph_conversion import GraphConversionEngine
from .services.interactive_exploration import InteractiveExplorationEngine
from .services.knowledge_base import KnowledgeBase

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
knowledge_base = KnowledgeBase()
design_engine = DesignExplorationEngine(knowledge_base)
conversion_engine = GraphConversionEngine()
interactive_engine = InteractiveExplorationEngine(knowledge_base)


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
            {"type": "SI", "name": "Situation Assessment", "description": "Assess the current situation"},
            {"type": "PI", "name": "Problem Identification", "description": "Identify problems in the system"},
            {"type": "EI", "name": "Establish Intention", "description": "Establish intention to solve the problem"},
            {"type": "DI", "name": "Decompose Intention", "description": "Decompose intention into sub-intentions"},
            {"type": "CB", "name": "Conditional Branch", "description": "Branch based on conditions"},
            {"type": "SA", "name": "Solution Assignment", "description": "Assign solution to the system"}
        ],
        "si_components": [
            {"type": "CND", "name": "Condition", "description": "Role division based on situations"},
            {"type": "BUP", "name": "Backups", "description": "Backup relationship between subsystems"},
            {"type": "COL", "name": "Collaboration", "description": "Subsystems work together"},
            {"type": "ALT", "name": "Alternative", "description": "Multiple options available"},
            {"type": "EXO", "name": "Exclusive", "description": "Exactly one option must be chosen"}
        ]
    }


# Interactive Exploration Endpoints

class StartExplorationRequest(BaseModel):
    """Request to start interactive exploration."""
    initial_system: str


class StepRequest(BaseModel):
    """Request for a step in exploration."""
    pass


class SituationRequest(BaseModel):
    """Request to assess situation."""
    situation: str


class ProblemRequest(BaseModel):
    """Request to identify problem."""
    problem: str


class IntentionRequest(BaseModel):
    """Request to establish intention."""
    intention: str


class DecomposeRequest(BaseModel):
    """Request to decompose intention."""
    sub_intentions: List[str]
    sub_systems: List[str]


class SolutionRequest(BaseModel):
    """Request to apply solution."""
    solution: str


@app.post("/api/interactive/start")
async def start_interactive_exploration(request: StartExplorationRequest):
    """Start interactive design exploration.

    Args:
        request: Initial system to explore

    Returns:
        Next step information
    """
    try:
        interactive_engine.reset()
        result = interactive_engine.start_exploration(request.initial_system)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interactive/situation")
async def assess_situation_step(request: SituationRequest):
    """Execute situation assessment step.

    Args:
        request: Situation to assess

    Returns:
        Next step information
    """
    try:
        result = interactive_engine.assess_situation(request.situation)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interactive/problem")
async def identify_problem_step(request: ProblemRequest):
    """Execute problem identification step.

    Args:
        request: Problem to identify

    Returns:
        Next step information
    """
    try:
        result = interactive_engine.identify_problem(request.problem)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interactive/intention")
async def establish_intention_step(request: IntentionRequest):
    """Execute intention establishment step.

    Args:
        request: Intention to establish

    Returns:
        Next step information
    """
    try:
        result = interactive_engine.establish_intention(request.intention)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interactive/decompose")
async def decompose_intention_step(request: DecomposeRequest):
    """Execute intention decomposition step.

    Args:
        request: Sub-intentions and sub-systems

    Returns:
        Next step information
    """
    try:
        result = interactive_engine.decompose_intention(
            request.sub_intentions,
            request.sub_systems
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interactive/solution")
async def apply_solution_step(request: SolutionRequest):
    """Execute solution application step.

    Args:
        request: Solution to apply

    Returns:
        Next step information
    """
    try:
        result = interactive_engine.apply_solution(request.solution)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/interactive/state")
async def get_exploration_state():
    """Get current exploration state.

    Returns:
        Current state information
    """
    try:
        return interactive_engine.get_current_state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge-base")
async def get_knowledge_base():
    """Get knowledge base contents.

    Returns:
        Knowledge base data
    """
    try:
        return knowledge_base.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge-base/systems")
async def get_all_systems():
    """Get all known systems from knowledge base."""
    try:
        return {"systems": knowledge_base.get_all_systems()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
