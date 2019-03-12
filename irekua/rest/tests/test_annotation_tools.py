from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status

from .utils import BaseTestCase
from database.utils import simple_JSON_schema
from database.models import AnnotationTool


class AnnotationToolTestCase(BaseTestCase):
    def setUp(self):
        super(AnnotationToolTestCase, self).setUp()
        self.annotation_tool, _ = AnnotationTool.objects.get_or_create(
            name='Sample Annotation Tool',
            version='0',
            description='sample annotation tool',
            configuration_schema=simple_JSON_schema())

    def test_create_permissions(self):
        url = reverse('rest-api:annotationtool-list')
        annotation_tool = {
            'name': 'Sample annotation tool',
            'version': '1',
            'description': 'sample annotation tool',
            'configuration_schema': simple_JSON_schema()
        }

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, annotation_tool, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        annotation_tool['version'] = '2'
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(url, annotation_tool, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        annotation_tool['version'] = '3'
        self.client.force_authenticate(user=self.developer_user)
        response = self.client.post(url, annotation_tool, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_permissions(self):
        url = reverse(
            'rest-api:annotationtool-detail',
            args=[self.annotation_tool.id])
        annotation_tool = {
            'name': 'Sample annotation tool',
            'version': '1',
            'description': 'sample annotation tool',
            'configuration_schema': simple_JSON_schema()
        }

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(url, annotation_tool, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.put(url, annotation_tool, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.developer_user)
        response = self.client.put(url, annotation_tool, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_permissions(self):
        url = reverse('rest-api:annotationtool-detail', args=[self.annotation_tool.id])
        annotation_tool = {
            'version': '5',
        }

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, annotation_tool, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.developer_user)
        response = self.client.patch(url, annotation_tool, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.patch(url, annotation_tool, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
