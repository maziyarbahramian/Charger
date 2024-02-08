from locust import HttpUser, task, between



class WebsiteUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def task(self):
        data = {
            'phone_number': '+989114412191',
            'amount': "1.0"
        }
        headers = {
            'Authorization': 'Token ce9f66b37b1a144da4c8863ec61e1a546fac69a2'
        }
        self.client.post(
            '/api/request/charge-phone-number',
            json=data, headers=headers
        )
