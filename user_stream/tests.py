from django.core.exceptions import ImproperlyConfigured


from user_stream import BACKEND_SETTING_NAME, get_backend
from user_stream.backends.dummy import DummyBackend
from user_stream.utils import TestCase


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
        settings = {BACKEND_SETTING_NAME: 'user_stream.backends.dummy.DummyBackend'}
        with self.settings(**settings):
            backend = get_backend()
            self.assertTrue(isinstance(backend, DummyBackend))
