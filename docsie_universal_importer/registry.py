from swag_auth.registry import ConnectorRegistry


class CustomConnectorRegistry(ConnectorRegistry):
    def get_list(self):
        self.load()
        return [connector_cls for connector_cls in self.connector_map.values()]

    def by_id(self, connector_id):
        self.load()
        return self.connector_map[connector_id]


connector_registry = CustomConnectorRegistry('docsie_universal_importer')
