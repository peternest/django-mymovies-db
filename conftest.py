import pytest
from django.core.management import call_command
from pytest_django import DjangoDbBlocker


@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker: DjangoDbBlocker) -> None:
    with django_db_blocker.unblock():
        call_command("loaddata", "data/my_fixture.json")
