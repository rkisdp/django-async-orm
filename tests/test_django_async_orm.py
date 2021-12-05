import asyncio

from django.test import TestCase, tag
from django.conf import settings
from django.apps import apps
from unittest import IsolatedAsyncioTestCase
import time

from .models import TestModel



class AppLoadingTestCase(TestCase):

    @tag('ci')
    def test_dao_loaded(self):
        self.assertTrue(apps.is_installed('django_async_orm'))


    @tag('ci')
    def test_manager_is_async(self):
        manager_class_name = TestModel.objects.__class__.__name__
        self.assertTrue(
            manager_class_name.startswith('MixinAsync'),
            'Manager class name is %s but should start with "MixinAsync"' % (manager_class_name) )


class ReadModelTestCase(TestCase, IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await TestModel.objects.async_create(name="setup 1", obj_type='setup')
        await TestModel.objects.async_create(name="setup 2", obj_type='setup')


    async def asyncTearDown(self):
        await TestModel.objects.async_delete()


    @tag('ci')
    async def test_async_get(self):
        result = await TestModel.objects.async_get(name="setup 1")

        self.assertEqual(result.name, "setup 1")

    @tag('ci')
    async def test_async_all(self):
        result = await TestModel.objects.async_all()

        print(result)
        self.assertEqual(len(result), 2)


    @tag('dev')
    async def test_async_earliest(self):
        # TODO: need new field date
        self.assertTrue(False)

    @tag('dev')
    async def test_async_latest(self):
        # TODO: need new field date
        self.assertTrue(False)


    @tag('ci')
    async def test_async_first_in_all(self):
        all_result = await TestModel.objects.async_all()

        first = await all_result.async_first()

        self.assertEqual(all_result[0].name, first.name)


    @tag('last')
    async def test_async_last_in_all(self):
        all_result = await TestModel.objects.async_all()

        last = await all_result.async_last()

        self.assertEqual(all_result[-1].name, last.name)


    @tag('dev')
    async def test_async_count(self):
        result = await TestModel.objects.async_all()

        print(result)
        self.assertEqual(result.count(), 1)

    @tag('dev')
    async def test_async_exists(self):
        ...

class WriteModelTestCase(IsolatedAsyncioTestCase, TestCase):

    @tag('ci')
    async def test_create(self):
        print(self._asyncioTestLoop)
        result = await TestModel.objects.async_create(name="test")
        self.assertEqual(result.name, 'test')

    @tag('ci')
    async def test_bulk_create(self):
        objs = await TestModel.objects.async_bulk_create([
            TestModel(name='bulk create 1'),
            TestModel(name='bulk create 2'),
        ])

        self.assertEqual(len(objs), 2)

    @tag('dev')
    async def test_delete(self):

        print(self._asyncioTestLoop)
        created = await TestModel.objects.async_create(name="to delete")
        print(created)
        print(self._asyncioTestLoop)
        all_created = await TestModel.objects.async_all()
        print(self._asyncioTestLoop)
        print(list(all_created))
        self.assertEqual(len(all_created), 1)

        await all_created.async_delete()
        all_after_delete = await TestModel.objects.async_all()
        self.assertEqual(len(all_after_delete), 0)

