from Jasmin import Jasmin
from Routers.MTRouter import MTRouter
from Routers.MORouter import MORouter


class JasminRouter(MTRouter, MORouter):
    def __init__(self, jasmin: Jasmin):
        super().__init__(jasmin)

    def process_mt_router_action(self, json_action):
        if str(json_action['method']).lower() == 'add':
            if not json_action['data'].get('smpp_client_id') is None:
                if not json_action['data'].get('filters') is None:
                    data = json_action['data']
                    json_action['data']['rate'] = data['rate'] if data.get('rate') else '0.0'
                    json_action['data']['order'] = data['order'] if data.get('order') else '10'
                    self.add_mt_router(smpp_client_id=json_action['data'].get('smpp_client_id'),
                                       filters=json_action['data'].get('filters'),
                                       rate=json_action['data'].get('rate'),
                                       order=json_action['data'].get('order'),
                                       route_type=json_action['data'].get('route_type'))
                else:
                    data = json_action['data']
                    json_action['data']['rate'] = data['rate'] if data.get('rate') else '0.0'
                    self.add_default_mt_router(smpp_client_id=json_action['data'].get('smpp_client_id'),
                                               rate=json_action['data'].get('rate'))
        elif str(json_action['method']).lower() == 'remove':
            if not json_action['data'].get('order') is None:
                self.remove_mt_router(json_action['data'].get('order'))
        elif str(json_action['method']).lower() == 'get':
            return {'mt-routers': str(self.get_mt_routers())}

    def process_mo_router_action(self, json_action):
        if str(json_action['method']).lower() == 'add':
            if not json_action['data'].get('http_client_id') is None:
                if not json_action['data'].get('filters') is None:
                    self.add_mo_router(http_client_id=json_action['data'].get('http_client_id'),
                                       filters=json_action['data'].get('filters'),
                                       order=json_action['data'].get('order'),
                                       route_type=json_action['data'].get('route_type'))
                else:
                    self.add_default_mo_router(http_client_id=json_action['data'].get('http_client_id'))
        elif str(json_action['method']).lower() == 'remove':
            if not json_action['data'].get('order') is None:
                self.remove_mo_router(json_action['data'].get('order'))
        elif str(json_action['method']).lower() == 'get':
            return {'mo-routers': str(self.get_mo_routers())}
