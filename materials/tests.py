from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@example.com', first_name='admin')
        self.course = Course.objects.create(title='test', description='test', preview='test', owner=self.user)
        self.lesson = Lesson.objects.create(title='test', description='test', preview='test', course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.course.title
        )

    def test_course_create(self):
        url = reverse('materials:course-list')
        data = {
            'title': 'test1',
            'description': 'test1',
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        data = {
            'title': 'test',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.course.title
        )

    def test_course_delete(self):
        url = reverse('materials:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        self.maxDiff = None
        url = reverse('materials:course-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "title": self.lesson.title,
                            "description": self.lesson.description,
                            "preview": "http://testserver/media/test",
                            "link": None,
                            "course": self.course.pk,
                            "owner": None
                        },
                    ],
                    "subscription": False,
                    "title": self.course.title,
                    "description": self.course.description,
                    "preview": "http://testserver/media/test",
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@example.com', first_name='admin')
        self.course = Course.objects.create(title='test2', description='test2', preview='test2', owner=self.user)
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(title='test2', description='test2', preview='test2', course=self.course,
                                            owner=self.user)
        print(self.user.__dict__)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson-retrieve', args=[self.lesson.pk])
        response = self.client.get(url)
        deta = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            deta.get('title'), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse('materials:lesson-create')
        data = {
            'title': 'test3',
            'description': 'test3',
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse('materials:lesson-update', args=(self.lesson.pk,))
        data = {
            'title': 'test2',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'), self.lesson.title
        )

    def test_lesson_delete(self):
        url = reverse('materials:lesson-delete', args=(self.lesson.pk,))
        print(self.user.__dict__)
        response = self.client.delete(url)

        self.assertEqual(self.lesson.owner, self.user)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        self.maxDiff = None
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {

            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": 'http://testserver/media/test2',
                    "link": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                },
            ]
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin@example.com', first_name='admin')
        self.course = Course.objects.create(title='test', description='test', owner=self.user)
        self.lesson = Lesson.objects.create(title='test', description='test', course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse('materials:subscription')
        data = {
            'user': self.user,
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Subscription.objects.all().count(), 1
        )

    def test_subscription_delete(self):
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('materials:subscription')
        data = {
            'user': self.user,
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, {'message': 'Подписка удалена'}
        )
