import requests
import os

class Service:
    def __init__(self, name, k8s_name):
        self.name = name
        self.ip = os.environ.get("{}_SERVICE_HOST".format(k8s_name))
        self.host = "http://{}".format(self.ip)

    def get(self, url, **kwargs):
        return requests.get('{}/'.format(self.host)+url, **kwargs)

    def post(self, url, **kwargs):
        return requests.post('{}/'.format(self.host)+url, **kwargs)

    def put(self, url, **kwargs):
        return requests.put('{}/'.format(self.host)+url, **kwargs)

    def patch(self, url, **kwargs):
        return requests.patch('{}/'.format(self.host)+url, **kwargs)

    def delete(self, url, **kwargs):
        return requests.delete('{}/'.format(self.host)+url, **kwargs)


class Services:
    """docstring for Services."""
    def __init__(self, app=None):
        self.services = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app, depenencies=[]):
        '''Initalizes the application with the extension.
        :param app: The Flask application object.
        '''
        self.service_name = app.config.get('SERVICE_NAME', None)
        self.k8s_name = app.config.get("K8S_SERVICE_NAME", None)
        self.dependencies = app.config.get('DEPENDENCIES', [])

        self.services_url = "http://{}".format(os.environ.get('VLE_SERVICE_SERVICE_HOST'))

        if not app.config.get('NO_REGISTER', False):
            self.register()
            self.list()
            self.check_dependencies()
            self.add_services()

    def register(self):
        payload = {'name': self.service_name, 'k8s_name': self.k8s_name}
        response = requests.post(self.services_url + "/register", json=payload)
        if response.status_code != 201:
            raise Exception("Status Code: {}".format(response))

    def list(self):
        response = requests.get(self.services_url + "/services")
        json = response.json()
        self.services = {}
        for service in json['services']:
            self.services[service['name']] = Service(service['name'], service['k8s_name'])

    def add_services(self):
        self.__dict__.update(self.services)

    def check_dependencies(self):
        names = [service.name for service in self.services.values()]
        for dependency in self.dependencies:
            if dependency not in names:
                raise Exception("Missing Service: {}".format(dependency))
