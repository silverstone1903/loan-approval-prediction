from locust import HttpUser, task, between, TaskSet
import random
from data import test_data


headers = {"Content-Type": "application/json", "Accept": "application/json"}


class MyTaskSet(TaskSet):
    @task(1)
    def post_request(self):
        dx = random.choice(test_data)

        response = self.client.post("/api/V1/predict", json=dx, headers=headers)

    @task(4)
    def get_request(self):

        response = self.client.get("/", headers=headers)


class MyUser(HttpUser):
    tasks = [MyTaskSet]
    wait_time = between(1, 25)
