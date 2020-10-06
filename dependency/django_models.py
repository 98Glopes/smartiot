import os
from micro_framework.dependencies import Dependency


class DjangoModels(Dependency):

    def bind(self, worker):
        """Initialize the dependency"""
        import django
        django.setup()

    def before_call(self, worker):
        # import django
        # django.setup()
        if os.environ.get('DJANGO_NAMEKO_STANDALONE_SETTINGS_MODULE'):
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get('DJANGO_NAMEKO_STANDALONE_SETTINGS_MODULE'))
        elif not os.environ.get('DJANGO_SETTINGS_MODULE'):
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    def get_dependency(self, worker):
        """Get the dependency for the concrete service"""
        from django.apps import apps
        from django.conf import settings
        from django.contrib.auth.models import User

        apps_config = map(apps.get_app_config, settings.DJANGO_NAMEKO_STANDALONE_APPS)
        models = type('NonExistingClass_', (), {})

        for config in apps_config:
            for model in config.get_models():
                setattr(models, model.__name__, model)
        setattr(models, User.__name__, User)
        return models

    def after_call(self, worker, result, exc):
        """Close all the connections on teardown
        TODO: Autocommit??
        """
        from django.db import connections
        connections.close_all()


__all__ = ["DjangoModels"]
