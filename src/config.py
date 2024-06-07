from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    file_name: str = "loan_approval_dataset.csv"
    data_path: str = f"../data/{file_name}"
    model_path: str = str(Path.cwd().joinpath("model/model.txt"))
    seed: int = 2024
    target: str = "loan_status"
    n_tree: int = 1000
    drop_cols: list = ["loan_id", target]
    params: dict = {
    "boosting_type": "gbdt", 
    "feature_fraction": 0.5,
    "learning_rate": 0.1,
    "max_depth": -1,
    "metric": "binary_logloss",
    "n_jobs": -1,
    "num_leaves": 31,
    "objective": "binary",
    "random_state": seed,
    "bagging_fraction": 0.5,
    "verbosity": -1,
    "subsample_freq": 5,
    "bagging_seed": seed,
}
 