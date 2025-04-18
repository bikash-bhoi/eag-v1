from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Tuple
from mcp.types import TextContent

class ReasoningStep(BaseModel):
    description: str
    type: str

class ShowReasoningInput(BaseModel):
    steps: List[ReasoningStep]

class CalculateInput(BaseModel):
    expression: str

class VerifyInput(BaseModel):
    expression: str
    expected: float

class ConsistencyStep(BaseModel):
    expression: str
    result: float

class CheckConsistencyInput(BaseModel):
    steps: List[str]

class ConsistencyResult(BaseModel):
    consistency_score: float
    issues: List[str]
    warnings: List[str]
    insights: List[str]

class RectangleInput(BaseModel):
    x1: int = Field(default=300, description="Starting x-coordinate")
    y1: int = Field(default=300, description="Starting y-coordinate")
    x2: int = Field(default=700, description="Ending x-coordinate")
    y2: int = Field(default=700, description="Ending y-coordinate")

class PaintTextInput(BaseModel):
    text: str

class TextResponse(BaseModel):
    content: TextContent