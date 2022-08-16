from django.test import TestCase
from django.test import Client

from jobs.models import Job, JobTypes, Cities


class JobTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.job = Job.objects.create(job_name="Java开发工程师", job_type=JobTypes[0][0], job_city=Cities[1][0], job_requirement="精通Java开发")

    def test1(self):
        pass

    def test_index(self):
        client = Client()
        response = client.get('/joblist/')
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        response = self.client.get('/job/')
        self.assertEqual(response.status_code, 200)

        job = response.context['job']
        self.assertEqual(job.job_name, JobTests.job.job_name)
