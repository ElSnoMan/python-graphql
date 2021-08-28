""" Tests against our LogRocket service

1. Spin up uvicorn server
    $ poetry run poe logrocket

2. Run tests
"""
import pytest
import requests


URL = "http://localhost:8000"


def test_get_courses():
    QUERY = """
    query getCourses {
        getCourses {
            id
            title
            instructor
        }
    }
    """
    response = requests.post(URL, json={"query": QUERY})
    assert response.ok


COURSE_IDS = ["1", "2", "3"]


@pytest.mark.parametrize("course_id", COURSE_IDS)
def test_get_course_by_id(course_id):
    QUERY = """
    query getCourseById($id: String!) {
        getCourseById(id: $id) {
            id
            title
            instructor
        }
    }
    """
    variables = {"id": course_id}
    response = requests.post(URL, json={"query": QUERY, "variables": variables})
    assert response.ok
