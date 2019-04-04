# Copyright (c) Extreme Networks, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential.
# See the LICENSE file included with this work for details.

import six

from st2tests.fixturesloader import FixturesLoader

from tests.base import APIControllerWithRBACTestCase

http_client = six.moves.http_client

__all__ = [
    'RunnerTypesControllerRBACTestCase'
]

FIXTURES_PACK = 'generic'
TEST_FIXTURES = {
    'runners': ['testrunner1.yaml'],
    'actions': ['action1.yaml', 'local.yaml'],
    'triggers': ['trigger1.yaml'],
    'triggertypes': ['triggertype1.yaml']
}


class RunnerTypesControllerRBACTestCase(APIControllerWithRBACTestCase):
    fixtures_loader = FixturesLoader()

    def setUp(self):
        super(RunnerTypesControllerRBACTestCase, self).setUp()
        self.fixtures_loader.save_fixtures_to_db(fixtures_pack=FIXTURES_PACK,
                                                 fixtures_dict=TEST_FIXTURES)

    def test_get_all_and_get_one_no_permissions(self):
        # get all
        user_db = self.users['no_permissions']
        self.use_user(user_db)

        resp = self.app.get('/v1/runnertypes', expect_errors=True)
        expected_msg = ('User "no_permissions" doesn\'t have required permission '
                        '"runner_type_list"')
        self.assertEqual(resp.status_code, http_client.FORBIDDEN)
        self.assertEqual(resp.json['faultstring'], expected_msg)

        # get one
        resp = self.app.get('/v1/runnertypes/test-runner-1', expect_errors=True)
        expected_msg = ('User "no_permissions" doesn\'t have required permission '
                        '"runner_type_view" on resource "runner_type:test-runner-1"')
        self.assertEqual(resp.status_code, http_client.FORBIDDEN)
        self.assertEqual(resp.json['faultstring'], expected_msg)

    def test_put_disable_runner_no_permissions(self):
        user_db = self.users['admin']
        self.use_user(user_db)

        runnertype_id = 'test-runner-1'
        resp = self.app.get('/v1/runnertypes/%s' % runnertype_id)

        # Disable the runner
        user_db = self.users['no_permissions']
        self.use_user(user_db)

        update_input = resp.json
        update_input['enabled'] = False

        resp = self.__do_put(runnertype_id, update_input)
        expected_msg = ('User "no_permissions" doesn\'t have required permission '
                        '"runner_type_modify" on resource "runner_type:test-runner-1"')
        self.assertEqual(resp.status_code, http_client.FORBIDDEN)
        self.assertEqual(resp.json['faultstring'], expected_msg)

    def __do_put(self, runner_type_id, runner_type):
        return self.app.put_json('/v1/runnertypes/%s' % runner_type_id, runner_type,
                                expect_errors=True)
