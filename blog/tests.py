from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
        )
        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user,
        )

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        self.assertEquals(self.post.get_absolute_url(), '/post/1/')

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.body}', 'Nice body content')
        self.assertEqual(f'{self.post.author}', 'testuser')

    def test_post_list_view(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Nice body content')
        self.assertTemplateUsed(resp, 'home.html')

    def test_post_detail_view(self):
        re = self.client.get('/post/1/')
        no_re = self.client.get('/post/10000/')
        self.assertEqual(re.status_code, 200)
        self.assertEqual(no_re.status_code, 404)
        self.assertContains(re, 'A good title')
        self.assertTemplateUsed(re, 'post_detail.html')

    def test_post_create_view(self):
        resp = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'New title')
        self.assertContains(resp, 'New text')

    def test_post_update_view(self,):
        resp = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'body': 'Updated text',
        })
        self.assertEqual(resp.status_code, 200)  # Returns 302

    def test_post_delete_view(self):
        resp = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(resp.status_code, 200)
