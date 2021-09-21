# Copyright 2020 The StackStorm Authors.
# Copyright (C) 2020 Extreme Networks, Inc - All Rights Reserved
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

from __future__ import absolute_import

from st2common.rbac.types import PermissionType
from st2common.rbac.types import ResourceType
from st2common.persistence.auth import User
from st2common.persistence.rbac import Role
from st2common.persistence.rbac import UserRoleAssignment
from st2common.persistence.rbac import PermissionGrant
from st2common.persistence.keyvalue import KeyValuePair
from st2common.models.db.keyvalue import KeyValuePairDB
from st2common.models.db.auth import UserDB
from st2common.models.db.rbac import RoleDB
from st2common.models.db.rbac import UserRoleAssignmentDB
from st2common.models.db.rbac import PermissionGrantDB

from st2rbac_backend.resolvers import KeyValuePermissionsResolver
from tests.unit.test_rbac_resolvers import BasePermissionsResolverTestCase

__all__ = ["KeyValuePermissionsResolver"]


class KeyValuePermissionsResolverTestCase(BasePermissionsResolverTestCase):
    def setUp(self):
        super(KeyValuePermissionsResolverTestCase, self).setUp()

        # Insert mock users
        user_1_db = UserDB(name="1_role_view_grant")
        user_1_db = User.add_or_update(user_1_db)
        self.users["custom_role_key_value_pair_view_grant"] = user_1_db

        user_2_db = UserDB(name="2_role_list_grant")
        user_2_db = User.add_or_update(user_2_db)
        self.users["custom_role_key_value_pair_list_grant"] = user_2_db

        user_3_db = UserDB(name="3_role_all_grant")
        user_3_db = User.add_or_update(user_3_db)
        self.users["custom_role_key_value_pair_all_grant"] = user_3_db

        user_4_db = UserDB(name="4_role_create_grant")
        user_4_db = User.add_or_update(user_4_db)
        self.users["custom_role_key_value_pair_create_grant"] = user_4_db

        user_5_db = UserDB(name="5_role_delete_grant")
        user_5_db = User.add_or_update(user_5_db)
        self.users["custom_role_key_value_pair_delete_grant"] = user_5_db

        user_6_db = UserDB(name="6_system_grant")
        user_6_db = User.add_or_update(user_6_db)
        self.users["st2kv_system_grant"] = user_6_db

        # Insert mock data
        kvp_1_db = KeyValuePairDB(
            uid="key_value_pair:st2kv.user:testu:key1",
            scope="st2kv.user",
            name="key1",
            value="val1",
        )
        kvp_1_db = KeyValuePair.add_or_update(kvp_1_db)
        self.resources["user_role_1"] = kvp_1_db

        kvp_2_db = KeyValuePairDB(
            uid="key_value_pair:st2kv.user:testu:key2",
            scope="st2kv.user",
            name="key2",
            value="val2",
        )
        kvp_2_db = KeyValuePair.add_or_update(kvp_2_db)
        self.resources["user_role_2"] = kvp_2_db

        kvp_3_db = KeyValuePairDB(
            uid="key_value_pair:st2kv.user:testu:key3",
            scope="st2kv.user",
            name="key3",
            value="val3",
        )
        kvp_3_db = KeyValuePair.add_or_update(kvp_3_db)
        self.resources["user_role_3"] = kvp_3_db

        kvp_4_db = KeyValuePairDB(
            uid="key_value_pair:st2kv.system:key4",
            scope="st2kv.system",
            name="key4",
            value="val4",
        )
        kvp_4_db = KeyValuePair.add_or_update(kvp_4_db)
        self.resources["system_role_4"] = kvp_4_db

        kvp_5_db = KeyValuePairDB(
            uid="key_value_pair:st2kv.system:key5",
            scope="st2kv.system",
            name="key5",
            value="val5",
        )
        kvp_5_db = KeyValuePair.add_or_update(kvp_5_db)
        self.resources["system_role_5"] = kvp_5_db

        kvp_6_db = KeyValuePairDB(
            uid="key_value_pair:st2kv.system:key6",
            scope="st2kv.system",
            name="key6",
            value="val6",
        )
        kvp_6_db = KeyValuePair.add_or_update(kvp_6_db)
        self.resources["system_role_6"] = kvp_6_db

        kvp_7_db = KeyValuePairDB(
            uid="key_value_pair:st2kv.system:key7",
            scope="st2kv.system",
            name="key7",
            value="val7",
        )
        kvp_7_db = KeyValuePair.add_or_update(kvp_7_db)
        self.resources["system_role"] = kvp_7_db

        kvp_8_db = KeyValuePairDB(
            uid="key_value_pair:st2kv.user:testu:key8",
            scope="st2kv.user",
            name="key8",
            value="val8",
        )
        kvp_8_db = KeyValuePair.add_or_update(kvp_8_db)
        self.resources["user_role_8"] = kvp_8_db

        kvp_9_db = KeyValuePairDB(
            uid="key_value_pair:st2kv.system:key9",
            scope="st2kv.system",
            name="key9",
            value="val9",
        )
        kvp_9_db = KeyValuePair.add_or_update(kvp_9_db)
        self.resources["system_role_9"] = kvp_9_db

        # Create some mock roles with associated permission grants
        # Custom role - View permission
        # "key_value_pair_view" on user_role_1
        grant_db = PermissionGrantDB(
            resource_uid=self.resources["user_role_1"].get_uid(),
            resource_type=ResourceType.KEY_VALUE_PAIR,
            permission_types=[PermissionType.KEY_VALUE_VIEW],
        )
        grant_db = PermissionGrant.add_or_update(grant_db)
        grant_1_db = PermissionGrantDB(
            resource_uid=self.resources["system_role_5"].get_uid(),
            resource_type=ResourceType.KEY_VALUE_PAIR,
            permission_types=[PermissionType.KEY_VALUE_VIEW],
        )
        grant_1_db = PermissionGrant.add_or_update(grant_1_db)
        permission_grants = [str(grant_db.id), str(grant_1_db.id)]
        role_1_db = RoleDB(
            name="custom_role_key_value_pair_view_grant",
            permission_grants=permission_grants,
        )
        role_1_db = Role.add_or_update(role_1_db)
        self.roles["custom_role_key_value_pair_view_grant"] = role_1_db

        # Custom role - List permission
        # "key_value_pair_list" on user_role_2
        grant_db = PermissionGrantDB(
            resource_uid=self.resources["user_role_2"].get_uid(),
            resource_type=ResourceType.KEY_VALUE_PAIR,
            permission_types=[PermissionType.KEY_VALUE_LIST],
        )
        grant_db = PermissionGrant.add_or_update(grant_db)
        permission_grants = [str(grant_db.id)]
        role_2_db = RoleDB(
            name="custom_role_key_value_pair_list_grant",
            permission_grants=permission_grants,
        )
        role_2_db = Role.add_or_update(role_2_db)
        self.roles["custom_role_key_value_pair_list_grant"] = role_2_db

        # Custom role - List permission
        # "key_value_pair_list" on system_role
        grant_6_db = PermissionGrantDB(
            resource_uid=self.resources["system_role"].get_uid(),
            resource_type=ResourceType.KEY_VALUE_PAIR,
            permission_types=[PermissionType.KEY_VALUE_LIST],
        )
        grant_6_db = PermissionGrant.add_or_update(grant_6_db)
        permission_grants = [str(grant_6_db.id)]
        role_7_db = RoleDB(
            name="st2kv_system_grant",
            permission_grants=permission_grants,
        )
        role_7_db = Role.add_or_update(role_7_db)
        self.roles["st2kv_system_grant"] = role_7_db

        # Custom role - ALL permission
        # "key_value_pair_all" on system_role
        grant_db = PermissionGrantDB(
            resource_uid=self.resources["system_role_6"].get_uid(),
            resource_type=ResourceType.KEY_VALUE_PAIR,
            permission_types=[PermissionType.KEY_VALUE_ALL],
        )
        grant_db = PermissionGrant.add_or_update(grant_db)
        permission_grants = [str(grant_db.id)]
        role_3_db = RoleDB(
            name="custom_role_key_value_pair_all_grant",
            permission_grants=permission_grants,
        )
        role_3_db = Role.add_or_update(role_3_db)
        self.roles["custom_role_key_value_pair_all_grant"] = role_3_db

        # Custom role - Set permission
        # "key_value_pair_set" on user_role_3
        grant_db = PermissionGrantDB(
            resource_uid=self.resources["user_role_3"].get_uid(),
            resource_type=ResourceType.KEY_VALUE_PAIR,
            permission_types=[PermissionType.KEY_VALUE_SET],
        )
        grant_db = PermissionGrant.add_or_update(grant_db)
        grant_2_db = PermissionGrantDB(
            resource_uid=self.resources["user_role_8"].get_uid(),
            resource_type=ResourceType.KEY_VALUE_PAIR,
            permission_types=[PermissionType.KEY_VALUE_SET],
        )
        grant_2_db = PermissionGrant.add_or_update(grant_2_db)
        grant_3_db = PermissionGrantDB(
            resource_uid=self.resources["system_role_9"].get_uid(),
            resource_type=ResourceType.KEY_VALUE_PAIR,
            permission_types=[PermissionType.KEY_VALUE_SET],
        )
        grant_3_db = PermissionGrant.add_or_update(grant_3_db)
        permission_grants = [str(grant_db.id), str(grant_2_db.id), str(grant_3_db.id)]
        role_4_db = RoleDB(
            name="custom_role_key_value_pair_create_grant",
            permission_grants=permission_grants,
        )
        role_4_db = Role.add_or_update(role_4_db)
        self.roles["custom_role_key_value_pair_create_grant"] = role_4_db

        # Custom role - Delete permission
        # "key_value_pair_delete" on system_role_4
        grant_db = PermissionGrantDB(
            resource_uid=self.resources["system_role_4"].get_uid(),
            resource_type=ResourceType.KEY_VALUE_PAIR,
            permission_types=[PermissionType.KEY_VALUE_DELETE],
        )
        grant_db = PermissionGrant.add_or_update(grant_db)
        permission_grants = [str(grant_db.id)]
        role_5_db = RoleDB(
            name="custom_role_key_value_pair_delete_grant",
            permission_grants=permission_grants,
        )
        role_5_db = Role.add_or_update(role_5_db)
        self.roles["custom_role_key_value_pair_delete_grant"] = role_5_db

        # Create some mock role assignments
        user_db = self.users["custom_role_key_value_pair_view_grant"]
        role_assignment_db = UserRoleAssignmentDB(
            user=user_db.name,
            role=self.roles["custom_role_key_value_pair_view_grant"].name,
            source="assignments/%s.yaml" % user_db.name,
        )
        UserRoleAssignment.add_or_update(role_assignment_db)

        user_db = self.users["custom_role_key_value_pair_list_grant"]
        role_assignment_db = UserRoleAssignmentDB(
            user=user_db.name,
            role=self.roles["custom_role_key_value_pair_list_grant"].name,
            source="assignments/%s.yaml" % user_db.name,
        )
        UserRoleAssignment.add_or_update(role_assignment_db)

        user_db = self.users["custom_role_key_value_pair_all_grant"]
        role_assignment_db = UserRoleAssignmentDB(
            user=user_db.name,
            role=self.roles["custom_role_key_value_pair_all_grant"].name,
            source="assignments/%s.yaml" % user_db.name,
        )
        UserRoleAssignment.add_or_update(role_assignment_db)

        user_db = self.users["custom_role_key_value_pair_create_grant"]
        role_assignment_db = UserRoleAssignmentDB(
            user=user_db.name,
            role=self.roles["custom_role_key_value_pair_create_grant"].name,
            source="assignments/%s.yaml" % user_db.name,
        )
        UserRoleAssignment.add_or_update(role_assignment_db)

        user_db = self.users["custom_role_key_value_pair_delete_grant"]
        role_assignment_db = UserRoleAssignmentDB(
            user=user_db.name,
            role=self.roles["custom_role_key_value_pair_delete_grant"].name,
            source="assignments/%s.yaml" % user_db.name,
        )
        UserRoleAssignment.add_or_update(role_assignment_db)

        user_db = self.users["st2kv_system_grant"]
        role_assignment_db = UserRoleAssignmentDB(
            user=user_db.name,
            role=self.roles["st2kv_system_grant"].name,
            source="assignments/%s.yaml" % user_db.name,
        )
        UserRoleAssignment.add_or_update(role_assignment_db)

    def test_user_resource_db_no_role_permissions(self):
        resolver = KeyValuePermissionsResolver()
        all_permission_types = PermissionType.get_valid_permissions_for_resource_type(
            ResourceType.KEY_VALUE_PAIR
        )

        resource_db = self.resources["user_role_1"]
        # No roles, should return false for everything
        user_db = self.users["no_roles"]
        self.assertUserDoesntHaveResourceDbPermissions(
            resolver=resolver,
            user_db=user_db,
            resource_db=resource_db,
            permission_types=all_permission_types,
        )

        # Custom role with no permission grants, should return false for everything
        user_db = self.users["1_custom_role_no_permissions"]
        self.assertUserDoesntHaveResourceDbPermissions(
            resolver=resolver,
            user_db=user_db,
            resource_db=resource_db,
            permission_types=all_permission_types,
        )

    def test_user_no_role_permissions(self):
        resolver = KeyValuePermissionsResolver()
        permission_type = PermissionType.KEY_VALUE_LIST

        # Custom role with no permission grants, should return false for everything
        user_db = self.users["1_custom_role_no_permissions"]
        self.assertUserDoesntHavePermission(
            resolver=resolver, user_db=user_db, permission_type=permission_type
        )

        # No roles, should return false for everything
        user_db = self.users["no_roles"]
        self.assertUserDoesntHavePermission(
            resolver=resolver, user_db=user_db, permission_type=permission_type
        )

    def test_get_all_system_success(self):
        resolver = KeyValuePermissionsResolver()
        all_permission_types = PermissionType.get_valid_permissions_for_resource_type(
            ResourceType.KEY_VALUE_PAIR
        )

        # Admin user, should always return true
        resource_db = self.resources["user_role_1"]
        user_db = self.users["admin"]

        self.assertUserHasResourceDbPermissions(
            resolver=resolver,
            user_db=user_db,
            resource_db=resource_db,
            permission_types=all_permission_types,
        )

        # Observer, should always return true for VIEW permission
        user_db = self.users["observer"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_VIEW,
        )
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_2"],
            permission_type=PermissionType.KEY_VALUE_LIST,
        )

    def test_get_all_system_failure(self):
        resolver = KeyValuePermissionsResolver()
        # Observer, should always return false for DELETE/SET permission
        user_db = self.users["observer"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_3"],
            permission_type=PermissionType.KEY_VALUE_DELETE,
        )

        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_8"],
            permission_type=PermissionType.KEY_VALUE_SET,
        )

    def test_get_all_user_permissions_success(self):
        resolver = KeyValuePermissionsResolver()

        user_db = self.users["custom_role_key_value_pair_list_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_2"],
            permission_type=PermissionType.KEY_VALUE_LIST,
        )

        user_db = self.users["custom_role_key_value_pair_view_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_VIEW,
        )

    def test_get_all_user_permissions_failure(self):
        resolver = KeyValuePermissionsResolver()

        user_db = self.users["custom_role_key_value_pair_delete_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_2"],
            permission_type=PermissionType.KEY_VALUE_DELETE,
        )

        user_db = self.users["custom_role_key_value_pair_create_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_2"],
            permission_type=PermissionType.KEY_VALUE_SET,
        )

    def test_get_user_permission(self):
        resolver = KeyValuePermissionsResolver()

        user_db = self.users["custom_role_key_value_pair_view_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_VIEW,
        )

        user_db = self.users["custom_role_key_value_pair_list_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_LIST,
        )

        user_db = self.users["custom_role_key_value_pair_delete_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_DELETE,
        )

        user_db = self.users["custom_role_key_value_pair_create_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_SET,
        )

    def test_set_user_permission(self):
        resolver = KeyValuePermissionsResolver()

        user_db = self.users["custom_role_key_value_pair_create_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_3"],
            permission_type=PermissionType.KEY_VALUE_SET,
        )

        user_db = self.users["custom_role_key_value_pair_view_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_VIEW,
        )

        user_db = self.users["custom_role_key_value_pair_list_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_LIST,
        )

        user_db = self.users["custom_role_key_value_pair_delete_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_DELETE,
        )

    def test_delete_user_permission(self):
        resolver = KeyValuePermissionsResolver()

        user_db = self.users["custom_role_key_value_pair_delete_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_4"],
            permission_type=PermissionType.KEY_VALUE_DELETE,
        )

        user_db = self.users["custom_role_key_value_pair_view_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_VIEW,
        )

        user_db = self.users["custom_role_key_value_pair_list_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_LIST,
        )

        user_db = self.users["custom_role_key_value_pair_create_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["user_role_1"],
            permission_type=PermissionType.KEY_VALUE_SET,
        )

    def test_get_all_system_permission(self):
        resolver = KeyValuePermissionsResolver()

        # System user should return true for VIEW permission
        user_db = self.users["st2kv_system_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role"],
            permission_type=PermissionType.KEY_VALUE_LIST,
        )
        user_db = self.users["custom_role_key_value_pair_create_grant"]
        # System user should return true for SET permission
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role"],
            permission_type=PermissionType.KEY_VALUE_SET,
        )
        user_db = self.users["custom_role_key_value_pair_view_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role"],
            permission_type=PermissionType.KEY_VALUE_VIEW,
        )
        user_db = self.users["custom_role_key_value_pair_delete_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role"],
            permission_type=PermissionType.KEY_VALUE_DELETE,
        )

    def test_set_system_permission(self):
        resolver = KeyValuePermissionsResolver()

        user_db = self.users["custom_role_key_value_pair_create_grant"]
        # System user should return true for SET permission
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_9"],
            permission_type=PermissionType.KEY_VALUE_SET,
        )
        # System user should return true for VIEW permission
        user_db = self.users["st2kv_system_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_9"],
            permission_type=PermissionType.KEY_VALUE_LIST,
        )
        user_db = self.users["custom_role_key_value_pair_view_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_5"],
            permission_type=PermissionType.KEY_VALUE_VIEW,
        )
        user_db = self.users["custom_role_key_value_pair_delete_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_9"],
            permission_type=PermissionType.KEY_VALUE_DELETE,
        )

    def test_get_system_permission(self):
        resolver = KeyValuePermissionsResolver()
        user_db = self.users["custom_role_key_value_pair_view_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_5"],
            permission_type=PermissionType.KEY_VALUE_VIEW,
        )
        # System user should return true for VIEW permission
        user_db = self.users["st2kv_system_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_5"],
            permission_type=PermissionType.KEY_VALUE_LIST,
        )
        user_db = self.users["custom_role_key_value_pair_create_grant"]
        # System user should return true for SET permission
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_5"],
            permission_type=PermissionType.KEY_VALUE_SET,
        )
        user_db = self.users["custom_role_key_value_pair_delete_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role"],
            permission_type=PermissionType.KEY_VALUE_DELETE,
        )

    def test_delete_system_permission(self):
        resolver = KeyValuePermissionsResolver()

        user_db = self.users["custom_role_key_value_pair_delete_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_4"],
            permission_type=PermissionType.KEY_VALUE_DELETE,
        )
        user_db = self.users["custom_role_key_value_pair_view_grant"]
        self.assertUserHasResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_5"],
            permission_type=PermissionType.KEY_VALUE_VIEW,
        )
        # System user should return true for VIEW permission
        user_db = self.users["st2kv_system_grant"]
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_4"],
            permission_type=PermissionType.KEY_VALUE_LIST,
        )
        user_db = self.users["custom_role_key_value_pair_create_grant"]
        # System user should return true for SET permission
        self.assertUserDoesntHaveResourceDbPermission(
            resolver=resolver,
            user_db=user_db,
            resource_db=self.resources["system_role_4"],
            permission_type=PermissionType.KEY_VALUE_SET,
        )
