from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskModelTests(TestCase):
    def test_str_returns_title(self):
        task = Task.objects.create(title='Buy milk')
        self.assertEqual(str(task), 'Buy milk')


class TaskListViewTests(TestCase):
    def test_list_shows_existing_tasks(self):
        Task.objects.create(title='Write report')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Write report')

    def test_list_shows_empty_message_when_no_tasks(self):
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, 'No tasks yet.')


class TaskCreateViewTests(TestCase):
    def test_create_saves_new_task(self):
        response = self.client.post(reverse('task_create'), {
            'title': 'New task',
            'description': '',
            'completed': False,
        })
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(Task.objects.filter(title='New task').exists())


class TaskUpdateViewTests(TestCase):
    def test_update_changes_task_fields(self):
        task = Task.objects.create(title='Old title')
        response = self.client.post(reverse('task_update', args=[task.pk]), {
            'title': 'Updated title',
            'description': '',
            'completed': True,
        })
        self.assertRedirects(response, reverse('task_list'))
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated title')
        self.assertTrue(task.completed)


class TaskToggleViewTests(TestCase):
    def test_toggle_flips_completed_status(self):
        task = Task.objects.create(title='Toggle me', completed=False)
        self.client.post(reverse('task_toggle', args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.completed)

        self.client.post(reverse('task_toggle', args=[task.pk]))
        task.refresh_from_db()
        self.assertFalse(task.completed)


class TaskDeleteViewTests(TestCase):
    def test_delete_removes_task(self):
        task = Task.objects.create(title='Delete me')
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
