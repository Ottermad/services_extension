import requests

class Service:
    def __init__(self, host):
        self.host = host

    def get(url, **kwargs):
        return requests.get('{}/'+url, **kwargs)

    def post(url, **kwargs):
        return requests.post('{}/'+url, **kwargs)

    def put(url, **kwargs):
        return requests.put('{}/'+url, **kwargs)

    def patch(url, **kwargs):
        return requests.patch('{}/'+url, **kwargs)

    def delete(url, **kwargs):
        return requests.delete('{}/'+url, **kwargs)


class Services:
    """docstring for Services."""
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app, depenencies=[]):
        '''Initalizes the application with the extension.
        :param app: The Flask application object.
        '''
        self.service_name = app.config.get('SERVICE_NAME', None)
        self.dependencies = app.config.get('DEPENDENCIES', [])
        if app.config.get('NO_REGISTER', False):
            self.register()
        self.list()
        self.check_dependencies()
        self.add_services()

    def register(self):
        payload = {'name': self.service_name}
        response = requests.post('http://services/register', json=payload)
        if response.status_code != 201:
            raise Exception("Status Code: {}".format(response))

    def list(self):
        response = requests.get('http://services/services')
        json = response.json()
        self.services = json['services']

    def add_services(self):
        service_objs = {}
        for service in self.services:
            service_objs[service['name']] = Service(service['host'])
        self.__dict__.update(service_objs)

    def check_dependencies(self):
        names = [service['name'] for service in self.services]
        for dependency in self.dependencies:
            if dependency not in names:
                raise Exception("Missing Service: {}".format(depenency))
