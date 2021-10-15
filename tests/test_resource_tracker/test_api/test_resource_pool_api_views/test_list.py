from rest_framework import status
from rest_framework.reverse import reverse

from resource_tracker.api.serializers.resource_pool.resource_pool_serializer import ResourcePoolSerializer
from resource_tracker.models import ResourcePool
from tests.test_resource_tracker.test_api.base_test_api import BaseTestAPI


class TestResourcePoolList(BaseTestAPI):

    def setUp(self):
        super(TestResourcePoolList, self).setUp()
        self.url = reverse('api_resource_pool_list_create')

    def test_resource_pool_list(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ResourcePool.objects.all().count(), len(response.data))
        all_instances = ResourcePool.objects.all()
        serializer = ResourcePoolSerializer(all_instances, many=True)
        self.assertEqual(response.data, serializer.data)