from fastapi import APIRouter, status
import pandas as pd
from src.utils import load_model
from src.config import Settings
from src.datamodel import Data
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

router = APIRouter()
config = Settings()

model, cols = load_model(config.model_path)


@router.get(
    "/",
    status_code=200,
    summary="Returns 200 for healthcheck.",
    tags=["Root"],
)
def index():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "status": status.HTTP_200_OK,
                "success": True,
                "still": "alive",
            }
        ),
    )


@router.post("/api/V1/predict", tags=["predict"])
async def predict(input_data: Data):
    prediction = model.predict(pd.DataFrame([input_data.dict()])[cols])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "loan_approval_score": round(prediction[0], 4),
                "loan_approval_status": (
                    "Approved" if prediction[0] > 0.5 else "Rejected"
                ),
            }
        ),
    )

