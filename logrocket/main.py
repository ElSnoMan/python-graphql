import json
from fastapi import FastAPI
from graphene import ObjectType, Field, List, String, Schema, Mutation
import graphene
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp
from logrocket.schemas import CourseType


class Query(ObjectType):
    course_list = None
    get_courses = List(CourseType)
    get_course_by_id = Field(CourseType, id=String())

    async def resolve_get_courses(self, info):
        with open("logrocket/courses.json") as courses:
            course_list = json.load(courses)
        return course_list

    async def resolve_get_course_by_id(self, info, id):
        with open("logrocket/courses.json") as courses:
            course_list = json.load(courses)
        if id:
            return next(course for course in course_list if course["id"] == id)
        return None


class CreateCourse(Mutation):
    course = Field(CourseType)

    class Arguments:
        id = String(required=True)
        title = String(required=True)
        instructor = String(required=True)

    async def mutate(self, info, id, title, instructor):
        with open("logrocket/courses.json", "r+") as courses:
            course_list = json.load(courses)
            course_list.append({"id": id, "title": title, "instructor": instructor})
            courses.seek(0)
            json.dump(course_list, courses, indent=2)
            for course in course_list:
                if course["id"] == id:
                    raise ValueError("Course with provided id already exists!")
        return CreateCourse(course=course_list[-1])


class Mutation(ObjectType):
    create_course = CreateCourse.Field()


app = FastAPI()
app.add_route(
    "/",
    GraphQLApp(
        schema=Schema(query=Query, mutation=Mutation), executor_class=AsyncioExecutor
    ),
)
