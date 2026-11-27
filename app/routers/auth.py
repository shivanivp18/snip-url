
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth.dependencies import get_current_client
from app.models import ApiClient


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


class ClientResponse(BaseModel):
    id: int
    name: str


@router.get("/me", response_model=ClientResponse)
def get_me(
    client: Annotated[
        ApiClient,
        Depends(get_current_client)
    ],
):
    return ClientResponse(
        id=client.id,
        name=client.name,
    )
