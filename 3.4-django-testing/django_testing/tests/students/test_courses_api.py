import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    """Фабрика для создания студентов"""
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    """Фабрика для создания курсов"""
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_api(client, student_factory, course_factory):
    students = student_factory(_quantity=10)
    courses = course_factory(_quantity=10)

    for course in courses:
        course.students.set(students)

    response = client.get("/api/v1/courses/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course["name"] == courses[i].name


@pytest.mark.django_db
def test_create_course(client, course_factory):

    """
    Проверка получения первого курса (retrieve-логика):
    создаем курс через фабрику;
    строим урл и делаем запрос через тестовый клиент;
    проверяем, что вернулся именно тот курс, который запрашивали;
    """

    course = course_factory(_quantity=1)
    response = client.get(f"/api/v1/courses/1/")
    assert response.status_code == 200
    assert response.json()["name"] == course.name


@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    """
    Проверка получения списка курсов (list-логика):
    аналогично — сначала вызываем фабрики, затем делаем запрос и проверяем результат;
    """
    courses = course_factory(_quantity=10)
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    response_courses_count = len(response.json())
    assert response_courses_count == len(courses)


@pytest.mark.django_db
def test_filter_by_id(client, course_factory):
    """
    Проверка фильтрации списка курсов по `id`:
    создаем курсы через фабрику, передать ID одного курса в фильтр, проверить результат запроса с фильтром;
    """
    courses = course_factory(_quantity=10)
    response = client.get(f"/api/v1/courses/?id={courses[0].id}")
    assert response.status_code == 200
    response_courses_count = len(response.json())
    assert response_courses_count == 1
    assert response.json()[0]["name"] == courses[0].name


@pytest.mark.django_db
def test_filter_by_name(client, course_factory):
    """
    Проверка фильтрации списка курсов по `name`;
    """
    courses = course_factory(_quantity=10)
    response = client.get(f"/api/v1/courses/?name={courses[0].name}")
    assert response.status_code == 200
    response_courses_count = len(response.json())
    assert response_courses_count == 1
    assert response.json()[0]["name"] == courses[0].name


@pytest.mark.django_db
def test_create_course(client):
    """
    Тест успешного создания курса:
    здесь фабрика не нужна, готовим JSON-данные и создаём курс;
    """

    course = Course.objects.create(name="Test course")
    response = client.post(f"/api/v1/courses/", data={"name": course.name})
    assert response.status_code == 201
    assert response.json()["name"] == course.name


@pytest.mark.django_db
def test_update_course(client, course_factory):
    """
    Тест успешного обновления курса:
    сначала через фабрику создаём, потом обновляем JSON-данными;
    """
    course = course_factory(_quantity=1)
    response = client.put(f"/api/v1/courses/{course[0].id}/", data={"name": "Updated course"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated course"


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    """
    Тест успешного удаления курса.
    """
    course = course_factory(_quantity=1)
    response = client.delete(f"/api/v1/courses/{course[0].id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_course_max_students(client, course_factory, settings, student_factory):
    """
    Тест проверки максимального количества студентов в курсе.
    """
    courses = course_factory(_quantity=1,)
    students = student_factory(settings.MAX_STUDENTS_PER_COURSE)
    for course in courses:
        course.students.add(*students)
    response = client.get(f"/api/v1/courses/{courses[0].id}/")
    assert response.status_code == 200
    assert len(response.json()["students"]) == settings.MAX_STUDENTS_PER_COURSE
