"""Define tests for django-use-email-as-username."""

import filecmp
import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest import mock

from django.core.exceptions import FieldDoesNotExist
from django.core.management import call_command
from django.test import TestCase

from custom_user_test.models import User
from django_use_email_as_username.admin import BaseUserAdmin
from django_use_email_as_username.models import BaseUserManager


def contains_recursive(nl, target):
    """Recursive search for an element in list, sets and tuples."""
    if type(nl) is dict:
        nl = nl.values()
    for thing in nl:
        if type(thing) in (list, set, tuple, dict):
            if contains_recursive(thing, target):
                return True
        if thing == target:
            return True
    return False


class TestContainsRecursive(TestCase):
    """Quick test for our recursive function."""

    test_list = [1, "a"]
    test_tuple = [2, "b"]
    test_set = {3, "c"}
    test_dict = {"int": 4, "str": "d"}

    test_nested = {
        "list": [test_list, test_tuple, test_set, test_dict],
    }

    def test_list_search(self):
        """Test it finds elements in lists."""
        self.assertTrue(contains_recursive(self.test_list, 1))
        self.assertFalse(contains_recursive(self.test_list, 10))
        self.assertTrue(contains_recursive(self.test_list, "a"))
        self.assertFalse(contains_recursive(self.test_list, "zz"))

    def test_tuple_search(self):
        """Test it finds elements in tuples."""
        self.assertTrue(contains_recursive(self.test_tuple, 2))
        self.assertTrue(contains_recursive(self.test_tuple, "b"))
        self.assertFalse(contains_recursive(self.test_tuple, 10))
        self.assertFalse(contains_recursive(self.test_tuple, "zz"))

    def test_set_search(self):
        """Test it finds elements in sets."""
        self.assertTrue(contains_recursive(self.test_set, 3))
        self.assertTrue(contains_recursive(self.test_set, "c"))
        self.assertFalse(contains_recursive(self.test_set, 10))
        self.assertFalse(contains_recursive(self.test_set, "zz"))

    def test_dict_search(self):
        """Test it finds elements in dictionaries."""
        self.assertTrue(contains_recursive(self.test_dict, 4))
        self.assertTrue(contains_recursive(self.test_dict, "d"))
        self.assertFalse(contains_recursive(self.test_dict, 10))
        self.assertFalse(contains_recursive(self.test_dict, "zz"))

    def test_nested_search(self):
        """Test it finds elements in nested structures."""
        self.assertTrue(contains_recursive(self.test_nested, 1))
        self.assertTrue(contains_recursive(self.test_nested, "a"))
        self.assertTrue(contains_recursive(self.test_nested, 2))
        self.assertTrue(contains_recursive(self.test_nested, "b"))
        self.assertTrue(contains_recursive(self.test_nested, 3))
        self.assertTrue(contains_recursive(self.test_nested, "c"))
        self.assertTrue(contains_recursive(self.test_nested, 4))
        self.assertTrue(contains_recursive(self.test_nested, "d"))
        self.assertFalse(contains_recursive(self.test_nested, 10))
        self.assertFalse(contains_recursive(self.test_nested, "zz"))


class TestAppGeneration(TestCase):
    """Test custom app generations."""

    def setUp(self):
        """
        Prepare test environment.

        - Create temp directory to use in tests.
        - Avoid `CommandError` from `validate_name:
            - Ensure `apps` is not in sys.path to .
            - Remove `custom_user_test` from `sys.modules`.
        """
        self.test_dir = tempfile.mkdtemp()
        self.original_path = sys.path[:]
        sys.path.remove(os.path.dirname(os.path.abspath(__file__)) + "/apps")
        self.custom_user_test_module = sys.modules.pop("custom_user_test")

    def tearDown(self):
        """
        Revert modifications made by the test.

        - Remove temp directory used in tests.
        - Reset `sys.path`.
        - Add `custom_user_test` back to `sys.modules`.
        """
        shutil.rmtree(self.test_dir)
        sys.path = self.original_path
        sys.modules["custom_user_test"] = self.custom_user_test_module

    def test_custom_app_is_created(self):
        """Test that create_custom_user_app command creates the app."""
        call_command(
            "create_custom_user_app", "custom_user_test", directory=self.test_dir
        )
        custom_user_test_path = (
            os.path.dirname(os.path.abspath(__file__)) + "/apps/custom_user_test"
        )

        base_files = set()
        for path in Path(self.test_dir).glob("**/*.py"):
            base_files.add(str(path.relative_to(self.test_dir)))

        test_files = set()
        for path in Path(custom_user_test_path).glob("**/*.py"):
            test_files.add(str(path.relative_to(custom_user_test_path)))

        all_files = base_files.union(test_files)
        difference = base_files.symmetric_difference(test_files)

        comparison = filecmp.cmpfiles(self.test_dir, custom_user_test_path, all_files)

        self.assertEqual(difference, {"migrations/0001_initial.py"})
        self.assertEqual(difference, set(comparison[2]))
        self.assertEqual(base_files, set(comparison[0]))


class TestUserModel(TestCase):
    """Test User model."""

    def test_user_has_no_username(self):
        """Test that the user model has no username field."""
        self.assertRaises(FieldDoesNotExist, User._meta.get_field, "username")

    def test_username_field_is_email(self):
        """Test that the value of USERNAME_FIELD is email."""
        self.assertEqual(User.USERNAME_FIELD, "email")

    def test_email_is_unique(self):
        """Test that the email field is unique."""
        email_field = User._meta.get_field("email")
        self.assertTrue(email_field.unique)

    def test_email_is_not_null(self):
        """Test that the email field is not null."""
        email_field = User._meta.get_field("email")
        self.assertFalse(email_field.null)

    def test_email_is_not_blank(self):
        """Test that the email field is not blank."""
        email_field = User._meta.get_field("email")
        self.assertFalse(email_field.blank)


class TestUserManager(TestCase):
    """Test User Manager."""

    def test_objects(self):
        """Test default manager (objects) is BaseUserManager."""
        self.assertIsInstance(User.objects, BaseUserManager)

    def test_create_superuser(self):
        """Test a super user is created."""
        user = User.objects.create_superuser("foo@domain.com", "bar")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(User.objects.last(), user)

    def test_create_superuser_forces_is_staff(self):
        """Test is_staff must be true."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser("foo@domain.com", "bar", is_staff=False)

    def test_create_superuser_forces_is_superuser(self):
        """Test is_superuser must be true."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser("foo@domain.com", "bar", is_superuser=False)

    def test_create_user(self):
        """Test a user is created."""
        user = User.objects.create_user("foo@domain.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(User.objects.last(), user)

    def test_create_user_respects_is_staff(self):
        """Test is_staff value is respected."""
        user = User.objects.create_user("foo@domain.com", is_staff=True)
        self.assertTrue(user.is_staff)

    def test_create_user_respects_is_superuser(self):
        """Test is_superuser value is respected."""
        user = User.objects.create_user("foo@domain.com", is_superuser=True)
        self.assertTrue(user.is_superuser)

    def test_create_user_passes_other_params(self):
        """Test is_superuser value is respected."""
        user = User.objects.create_user("foo@domain.com", is_active=False)
        self.assertFalse(user.is_active)

        user = User.objects.create_user("bar@domain.com", is_active=True)
        self.assertTrue(user.is_active)

    def test_password_is_set(self):
        """Test a user gets its password."""
        with self.subTest("For users"):
            user = User.objects.create_user("foo@domain.com", "bar")
            self.assertTrue(user.check_password("bar"))

        with self.subTest("For superusers"):
            user = User.objects.create_superuser("bar@domain.com", "foo")
            self.assertTrue(user.check_password("foo"))

    def test_user_is_created_with__create_user(self):
        """Test that _create_user is called by create_user."""
        User.objects._create_user = mock.MagicMock()

        User.objects.create_user("foo@domain.com")
        self.assertEqual(User.objects._create_user.call_count, 1)

    def test_superuser_is_created_with__create_user(self):
        """Test that _create_user is called by create_superuser."""
        User.objects._create_user = mock.MagicMock()

        User.objects.create_superuser("bar@domain.com", "foo")
        self.assertEqual(User.objects._create_user.call_count, 1)

    def test_email_is_normalized(self):
        """Test that _create_user is called."""
        User.objects.normalize_email = mock.MagicMock(
            wraps=User.objects.normalize_email
        )

        user = User.objects._create_user("foo@DOMAIN.com", "bar")

        User.objects.normalize_email.assert_called_once_with("foo@DOMAIN.com")
        self.assertEqual(user.email, "foo@domain.com")

    def test_email_is_required(self):
        """Test email is required by _create_user."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(False, None)

        with self.assertRaises(ValueError):
            User.objects.create_superuser("", None)


class TestUserAdmin(TestCase):
    """Test User Admin."""

    def test_fieldset_has_no_username(self):
        """Test username is not in the admin filedsets."""
        self.assertFalse(contains_recursive(BaseUserAdmin.fieldsets, "username"))

    def test_fieldset_has_email(self):
        """Test email is in the admin filedsets."""
        self.assertTrue(contains_recursive(BaseUserAdmin.fieldsets, "email"))

    def test_add_fieldsets_has_no_username(self):
        """Test username is not in the admin add_fieldsets."""
        self.assertFalse(contains_recursive(BaseUserAdmin.add_fieldsets, "username"))

    def test_add_fieldsets_has_email(self):
        """Test email is in the admin add_fieldsets."""
        self.assertTrue(contains_recursive(BaseUserAdmin.add_fieldsets, "email"))

    def test_list_display_has_no_username(self):
        """Test username is not in the admin list_display."""
        self.assertFalse(contains_recursive(BaseUserAdmin.list_display, "username"))

    def test_list_display_has_email(self):
        """Test email is in the admin list_display."""
        self.assertTrue(contains_recursive(BaseUserAdmin.list_display, "email"))

    def test_search_fields_has_no_username(self):
        """Test username is not in the admin search_fields."""
        self.assertFalse(contains_recursive(BaseUserAdmin.search_fields, "username"))

    def test_search_fields_has_email(self):
        """Test email is in the admin search_fields."""
        self.assertTrue(contains_recursive(BaseUserAdmin.search_fields, "email"))

    def test_ordering_has_no_username(self):
        """Test username is not in the admin ordering."""
        self.assertFalse(contains_recursive(BaseUserAdmin.ordering, "username"))

    def test_ordering_has_email(self):
        """Test email is in the admin ordering."""
        self.assertTrue(contains_recursive(BaseUserAdmin.ordering, "email"))
