============================
Django use Email as Username
============================

.. image:: https://badge.fury.io/py/django-use-email-as-username.svg
    :target: https://badge.fury.io/py/django-use-email-as-username

.. image:: https://github.com/jmfederico/django-use-email-as-username/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/jmfederico/django-use-email-as-username/actions/workflows/tests.yml

.. image:: https://codecov.io/gh/jmfederico/django-use-email-as-username/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jmfederico/django-use-email-as-username

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

A Django app to use email as username for user authentication.


Features
--------

* Custom User model with no username field
* Use email as username
* Includes a django-admin command for quick install
* Follow Django `best practices`_ for new Django projects and User models.

.. _`best practices`: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project


Quickstart
----------

#. Install **Django use Email as Username**:

   .. code-block:: shell

      # Run in your terminal
      pip install django-use-email-as-username

#. Add it to your *INSTALLED_APPS*:

   .. code-block:: python

      # In your settings.py file
      INSTALLED_APPS = (
          ...
          'django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig',
          ...
      )

#. Create your new django app:

   .. code-block:: shell

      # Run in your terminal
      python manage.py create_custom_user_app

#. Add the new app to your *INSTALLED_APPS*:

   .. code-block:: python

      # In your settings.py file
      INSTALLED_APPS = (
          ...
          'django_use_email_as_username.apps.DjangoUseEmailAsUsernameConfig',
          'custom_user.apps.CustomUserConfig',
          ...
      )

#. Now instruct Django to use your new model:

   .. code-block:: python

      # In your settings.py file
      AUTH_USER_MODEL = 'custom_user.User'

#. Create and run migrations:

   .. code-block:: shell

      # Run in your terminal
      python manage.py makemigrations
      python manage.py migrate

You now have a new Django app which provides a custom User model.

You can further modify the new User Model any time in the future, just remember
to create and run the migrations.


Notes
-----

This app gives you a custom User model, which is `good practice`_ for new
Django projects.

`Changing to a custom user model mid-project`_ is not easy.

.. _`good practice`: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
.. _`Changing to a custom user model mid-project`: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#changing-to-a-custom-user-model-mid-project

It is recommended to always create a custom User model at the beginning of every
Django project.

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `Cookiecutter Django Package`_ by jmfederico_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`Cookiecutter Django Package`: https://github.com/jmfederico/cookiecutter-djangopackage
.. _jmfederico: https://github.com/jmfederico
