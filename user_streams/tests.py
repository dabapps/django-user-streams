# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured


from user_streams import BACKEND_SETTING_NAME, get_backend, add_stream_item, get_stream_items
from user_streams.backends.dummy import DummyBackend
from user_streams.utils import TestCase, override_settings


DUMMY_BACKEND_SETTINGS = {BACKEND_SETTING_NAME: 'user_streams.backends.dummy.DummyBackend'}


class GetBackendTestCase(TestCase):

    def test_missing_setting(self):
        with self.assertRaises(ImproperlyConfigured):
            get_backend()

    def test_invalid_backend_path(self):
        settings = {BACKEND_SETTING_NAME: 'invalid'}
        with self.settings(**settings):
            with self.assertRaises(ImproperlyConfigured):
                get_backend()

    def test_incorrect_backend_path(self):
        settings = {BACKEND_SETTING_NAME: 'foo.bar.invalid.InvalidClass'}
        with self.settings(**settings):
            with self.assertRaises(ImproperlyConfigured):
                get_backend()

    def test_correct_backend_returned(self):
        with self.settings(**DUMMY_BACKEND_SETTINGS):
            backend = get_backend()
            self.assertTrue(isinstance(backend, DummyBackend))


class StreamStorageTestMixin(object):

    """
    A mixin providing a set of test cases that can be run to test
    any backend. Note that the backend MUST be emptied (all messages
    should be removed) between each test. If a database backend
    is being tested, this will happen automatically. Otherwise, you
    are responsible for deleting all the messages between tests.
    """

    def test_single_user(self):
        user = User.objects.create()
        content = 'Test message'

        add_stream_item(user, content)

        items = get_stream_items(user)
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item.content, content)

    def test_multiple_users(self):
        user_1 = User.objects.create(username='test1')
        user_2 = User.objects.create(username='test2')
        user_3 = User.objects.create(username='test3')
        content = 'Broadcast message'

        add_stream_item(User.objects.all(), content)

        for user in user_1, user_2, user_3:
            self.assertEqual(get_stream_items(user)[0].content, content)

    def test_message_ordering(self):
        user = User.objects.create()
        now = datetime.now()

        add_stream_item(user, 'Message 1', created_at=now)
        add_stream_item(user, 'Message 2', created_at=now + timedelta(minutes=1))
        add_stream_item(user, 'Message 3', created_at=now + timedelta(minutes=2))

        stream_items = get_stream_items(user)

        self.assertEqual(stream_items[0].content, 'Message 3')
        self.assertEqual(stream_items[1].content, 'Message 2')
        self.assertEqual(stream_items[2].content, 'Message 1')

    def test_identical_messages(self):
        """Check that identical messages are handled properly. Mostly
        an issue for the Redis backend (which uses sets to store messages)"""
        user = User.objects.create()
        message = 'Test message'

        add_stream_item(user, message)
        add_stream_item(user, message)

        items = get_stream_items(user)
        self.assertEqual(len(items), 2)

    def test_unicode_handled_properly(self):
        user = User.objects.create()
        message = u'☃'

        add_stream_item(user, message)

        items = get_stream_items(user)
        self.assertEqual(items[0].content, message)



@override_settings(**DUMMY_BACKEND_SETTINGS)
class DummyBackendStreamTestCase(TestCase, StreamStorageTestMixin):

    def setUp(self):
        dummy_backend = get_backend()
        dummy_backend.flush()
