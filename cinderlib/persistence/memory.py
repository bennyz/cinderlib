# Copyright (c) 2018, Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cinderlib.persistence import base as persistence_base


class MemoryPersistence(persistence_base.PersistenceDriverBase):
    volumes = {}
    snapshots = {}
    connections = {}

    def __init__(self):
        # Create fake DB for drivers
        self.fake_db = persistence_base.DB(self)
        super(MemoryPersistence, self).__init__()

    @property
    def db(self):
        return self.fake_db

    def _filter_by(self, values, field, value):
        if not value:
            return values
        return [res for res in values if getattr(res, field) == value]

    def get_volumes(self, volume_id=None, volume_name=None, backend_name=None):
        res = [self.volumes[volume_id]] if volume_id else self.volumes.values()
        res = self._filter_by(res, 'display_name', volume_name)
        res = self._filter_by(res, 'availability_zone', backend_name)
        return res

    def get_snapshots(self, snapshot_id=None, snapshot_name=None,
                      volume_id=None):
        result = ([self.snapshots[snapshot_id]] if snapshot_id
                  else self.snapshots.values())

        result = self._filter_by(result, 'volume_id', volume_id)
        result = self._filter_by(result, 'display_name', snapshot_name)
        return result

    def get_connections(self, connection_id=None, volume_id=None):
        result = ([self.connections[connection_id]] if connection_id
                  else self.connections.values())
        result = self._filter_by(result, 'volume_id', volume_id)
        return result

    def set_volume(self, volume):
        self.volumes[volume.id] = volume
        super(MemoryPersistence, self).set_volume(volume)

    def set_snapshot(self, snapshot):
        self.snapshots[snapshot.id] = snapshot
        super(MemoryPersistence, self).set_snapshot(snapshot)

    def set_connection(self, connection):
        self.connections[connection.id] = connection
        super(MemoryPersistence, self).set_connection(connection)

    def delete_volume(self, volume):
        self.volumes.pop(volume.id, None)
        super(MemoryPersistence, self).delete_volume(volume)

    def delete_snapshot(self, snapshot):
        self.snapshots.pop(snapshot.id, None)
        super(MemoryPersistence, self).delete_snapshot(snapshot)

    def delete_connection(self, connection):
        self.connections.pop(connection.id, None)
        super(MemoryPersistence, self).delete_connection(connection)
