import configparser
from listsync.json import JsonSource

from listsync.mailman import MailmanServer
from listsync.static import StaticSource
from listsync.wordpress import WordpressSource

class Instance():

    def __init__(self, config_handle, verbose = False):
        self._sources = {}
        self._servers = {}
        self._lists = {}
        self._verbose = verbose

        if verbose:
            print("Loading the configuration file")

        self._parse_config(config_handle)
        self._check_config()

    def sync(self):
        for name, list in self._lists.items():
            if self._verbose:
                print("Syncing list %s" % name)

            server = self._servers[list['server']]
            current_members = set(server.get_members(name))

            desired_members = set()            
            for source_name in list['sources']:
                source = self._sources[source_name]
                desired_members = desired_members.union(set(source.get_members()))

            missing_members = desired_members.difference(current_members)
            additional_members = current_members.difference(desired_members)

            for member in missing_members:
                if list['policy'] in [ 'subscribe', 'sync' ]:
                    if self._verbose:
                        print(" > Subscribing %s" % member)
                    server.add_member(name, member)

            for member in additional_members:
                if list['policy'] in [ 'sync', 'unsubscribe' ]:
                    if self._verbose:
                        print(" > Unsubscribing %s" % member)
                    server.delete_member(name, member)


    def _check_config(self):
        for name, list in self._lists.items():
            for source in list['sources']:
                if not source in self._sources.keys():
                    raise RuntimeError("List %s uses missing source %s" % (name, source))
            if not list['server'] in self._servers.keys():
                raise RuntimeError("List %s uses missing server %s" % (name, list['server']))

    def _parse_config(self, h):
        self._config = configparser.ConfigParser()
        self._config.read_file(h)

        # Parse all different sources and targets
        for section in self._config.sections():
            s = self._config[section]

            name = section

            if not "module" in s.keys():
                raise RuntimeError("Please provide a module for the section %s" % name)

            if s['module'] == 'json':
                self._sources[name] = JsonSource(s['url'], s.get('key', None), s.get('api_key', None))
            elif s['module'] == 'wordpress':
                self._sources[name] = WordpressSource(s['url'], s['filter'] if 'filter' in s.keys() else None)
            elif s['module'] == 'static':
                self._sources[name] = StaticSource([ email.strip() for email in s['emails'].split(",") ])
            elif s['module'] == 'mailman3':
                self._servers[name] = MailmanServer(s['url'], s['user'], s['password'])
            elif s['module'] == 'list':
                self._lists[name] = {
                    'sources': [ source.strip() for source in s['sources'].split(",") ], 
                    'server': s['server'], 
                    'policy': s['policy']
                }
