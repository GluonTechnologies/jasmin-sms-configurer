from Jasmin.Routers.MTRouter import MTRouter
from Jasmin.jasmin import Jasmin


class MTProcessor(MTRouter):
    def __init__(self, jasmin: Jasmin):
        super().__init__(jasmin)

    def add_default_router(self, json_data):
        rate
        self.add_mt_router(smpp_client_id=json_action['data'].get('smpp_client_id'),
                           filters=json_action['data'].get('filters'),
                           rate=json_action['data'].get('rate'),
                           order=json_action['data'].get('order'),
                           route_type=json_action['data'].get('route_type'))
