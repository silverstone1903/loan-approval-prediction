import warnings

warnings.filterwarnings("ignore")
from fastapi import FastAPI, APIRouter
import uvicorn
from fastapi.exceptions import RequestValidationError
from src import endpoints
from src.utils import (
    validation_exception_handler,
    not_found_exception_handler,
)
from uvicorn.config import LOGGING_CONFIG
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from src.readme import description

NAMESPACE = "prediction_service"
SUBSYSTEM = "loan_approval"

app = FastAPI(title="Loan Approval Prediction API", version="0.1")
app.include_router(endpoints.router)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(404, not_found_exception_handler)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics", "/metrics/", "/docs/", "openapi.json"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True
)

instrumentator.add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM))
instrumentator.add(
    metrics.response_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM))
instrumentator.add(
    metrics.requests(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM))
instrumentator.add(
    metrics.latency(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM))

Instrumentator().instrument(app).expose(app, tags=["metrics"])

if __name__ == "__main__":
    # https://stackoverflow.com/questions/62934384/how-to-add-timestamp-to-each-request-in-uvicorn-logs#comment113099430_63496366
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'

    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )