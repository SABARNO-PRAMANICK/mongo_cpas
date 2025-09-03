from fastapi import FastAPI, HTTPException, Body, Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uvicorn
import logging
from datetime import datetime
from pymongo.errors import DuplicateKeyError, OperationFailure
import crud  

logger = logging.getLogger(__name__)


app = FastAPI(title="User Input Storage API", description="API for storing and managing user inputs in MongoDB")


class UserInput(BaseModel):
    request_id: str = Field(..., description="Unique request ID")
    input: str = Field(..., description="User input string")
    metadata: Optional[Dict] = Field(default=None, description="Additional metadata")
    date_time: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="ISO-formatted timestamp")


class UserInputUpdate(BaseModel):
    input: Optional[str] = None
    metadata: Optional[Dict] = None
    date_time: Optional[str] = None

@app.post("/inputs/", response_model=UserInput, status_code=201)
async def create_input(input_data: UserInput = Body(...)):
    try:
        return crud.create_user_input(input_data.dict())
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Request ID already exists")
    except OperationFailure as e:
        logger.error(f"Insert failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to create input")

@app.get("/inputs/", response_model=List[UserInput])
async def get_all_inputs():
    return crud.get_all_user_inputs()

@app.get("/inputs/{request_id}", response_model=UserInput)
async def get_input(request_id: str = Path(..., description="Unique request ID")):
    input_doc = crud.get_user_input_by_id(request_id)
    if input_doc:
        return input_doc
    raise HTTPException(status_code=404, detail="Input not found")

@app.put("/inputs/{request_id}", response_model=UserInput)
async def update_input_full(
    request_id: str = Path(..., description="Unique request ID"),
    input_data: UserInput = Body(...)
):
    if input_data.request_id != request_id:
        raise HTTPException(status_code=400, detail="Request ID mismatch")
    updated_input = crud.replace_user_input(request_id, input_data.dict())
    if updated_input:
        return updated_input
    raise HTTPException(status_code=404, detail="Input not found")

@app.patch("/inputs/{request_id}", response_model=UserInput)
async def update_input_partial(
    request_id: str = Path(..., description="Unique request ID"),
    update_data: UserInputUpdate = Body(...)
):
    update_dict = {k: v for k, v in update_data.dict(exclude_unset=True).items() if v is not None}
    if not update_dict:
        raise HTTPException(status_code=400, detail="No update data provided")
    updated_input = crud.partial_update_user_input(request_id, update_dict)
    if updated_input:
        return updated_input
    raise HTTPException(status_code=404, detail="Input not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")