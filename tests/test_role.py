#!/usr/bin/env python
#
# (c) Copyright 2019-2022 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import opsramp.binding
import requests_mock


class ApiTest(unittest.TestCase):
    def setUp(self):
        fake_url = 'mock://api.example.com'
        fake_token = 'unit-test-fake-token'
        self.ormp = opsramp.binding.Opsramp(fake_url, fake_token)

        self.fake_client_id = 'client_for_unit_test'
        self.client = self.ormp.tenant(self.fake_client_id)
        assert self.client.is_client()

        self.permission_sets = self.client.permission_sets()
        assert 'PermissionSets' in str(self.permission_sets)

        self.roles = self.client.roles()
        assert 'Roles' in str(self.roles)

    def test_permission_sets_search(self):
        group = self.permission_sets
        thisid = 111111
        expected = {'id': thisid}
        pattern = 'whatever'
        with requests_mock.Mocker() as m:
            url = group.api.compute_url('?%s' % pattern)
            m.get(url, json=expected, complete_qs=True)
            actual = group.search(pattern)
            assert actual == expected

    def test_role_search(self):
        group = self.roles
        thisid = 222222
        expected = {'id': thisid}
        pattern = 'whatever'
        with requests_mock.Mocker() as m:
            url = group.api.compute_url('search?%s' % pattern)
            m.get(url, json=expected, complete_qs=True)
            actual = group.search(pattern)
            assert actual == expected

    def test_role_create(self):
        group = self.roles
        thisid = 345678
        expected = {'id': thisid}
        fake_defn = {'name': 'bishop brennan'}
        with requests_mock.Mocker() as m:
            url = group.api.compute_url()
            m.post(url, json=expected, complete_qs=True)
            actual = group.create(definition=fake_defn)
            assert actual == expected

    def test_role_update(self):
        group = self.roles
        thisid = 123456
        expected = {'id': thisid}
        fake_defn = {'name': 'fr noel furlong'}
        with requests_mock.Mocker() as m:
            url = group.api.compute_url(thisid)
            m.post(url, json=expected, complete_qs=True)
            actual = group.update(uuid=thisid, definition=fake_defn)
            assert actual == expected

    def test_role_delete(self):
        group = self.roles
        thisid = 789012
        expected = {'id': thisid}
        with requests_mock.Mocker() as m:
            url = group.api.compute_url(thisid)
            m.delete(url, json=expected, complete_qs=True)
            actual = group.delete(uuid=thisid)
        assert actual == expected
