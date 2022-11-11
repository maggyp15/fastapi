from locust import HttpUser, task


class PerformanceTests(HttpUser):

    @task
    def prime_number(self):
        self.client.get(url='prime/11')

    @task
    def post_img(self):
        in_file = open('lena.jpg', 'rb')
        data = in_file.read()
        self.client.post(url="picture/invert", files={'img': data})

    @task
    def check_user(self):
        self.client.get(url='users/me', headers={"username": "johndoe", "password": "secret"})

