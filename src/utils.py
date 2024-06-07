import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    recall_score,
    precision_score,
    roc_auc_score,
    classification_report,
)
import numpy as np
import lightgbm as lgb
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status, Request
from prometheus_fastapi_instrumentator import Instrumentator, metrics

NAMESPACE = "prediction_service"
SUBSYSTEM = "loan_approval"

def lgb_cv(df_train, df_val, train_cols, target, params, n_tree=500):

    dtrain = lgb.Dataset(df_train[train_cols], df_train[target], free_raw_data=True)
    dval = lgb.Dataset(df_val[train_cols], df_val[target], reference=dtrain)

    model = lgb.train(
        params,
        dtrain,
        num_boost_round=n_tree,
        callbacks=[lgb.log_evaluation(period=10), lgb.early_stopping(5)],
        valid_sets=(dtrain, dval),
    )

    val_preds = model.predict(df_val[train_cols]).round(2)

    val_score = f1_score(df_val[target], np.round(val_preds))
    evaluate_model(df_val[target], val_preds)
    fi_model = fi(model)

    return model, fi_model


def evaluate_model(y_test, prediction):
    print("\n")
    print("\t\t\t Evaluation")
    print(f"Accuracy: {np.round(accuracy_score(y_test, np.round(prediction)))}")
    print(f"F1: {f1_score(y_test, np.round(prediction)).round(4)}")
    print(f"Precision: {precision_score(y_test, np.round(prediction)).round(4)}")
    print(f"Recall: {recall_score(y_test, np.round(prediction)).round(4)}")
    print(f"ROC: {roc_auc_score(y_test, prediction).round(4)}")
    print("\t\t\t Classification Report")
    print(classification_report(y_test, np.round(prediction)))


def fi(model):

    return (
        pd.DataFrame(
            zip(
                model.feature_name(),
                model.feature_importance(importance_type="gain"),
                model.feature_importance(importance_type="split"),
            ),
            columns=["feature", "gain", "split"],
        )
        .sort_values("split", ascending=False)
        .set_index("feature")
    )


# https://github.com/roy-pstr/fastapi-custom-exception-handlers-and-logs/blob/master/main.py
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "data": "Invalid input",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "success": False,
                "error": exc.errors(),
                "input_data": exc.body,
            }
        ),
    )


async def internal_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                "data": exc.body,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
            }
        ),
    )


async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(
            {
                "data": exc.detail,
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "url": request.url,
            }
        ),
    )


def load_model(model_path: str):
    mdl = lgb.Booster(model_file=model_path)
    train_cols = mdl.feature_name()
    return mdl, train_cols
