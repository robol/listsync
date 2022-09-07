import configparser
from listsync.json import JsonSource

from listsync.mailman import MailmanServer

class Instance():

    def __init__(self, config_handle, verbose = False):
        self._sources = {}
        self._targets = {}
        self._lists = {}
        self._verbose = verbose

        if verbose:
            print("Loading the configuration file:")

        self._parse_config(config_handle)
        self._check_config()

    def sync(self):
        for name, list in self._lists.items():
            if self._verbose:
                print("Syncing list %s" % name)

            source = self._sources[list['source']]
            target = self._targets[list['target']]

            current_members = set(target.get_members(name))
            desired_members = set(source.get_members())

            missing_members = desired_members.difference(current_members)
            additional_members = current_members.difference(desired_members)

            for member in missing_members:
                if self._verbose:
                    print(" > Subscribing %s" % member)
                target.add_member(name, member)

            for member in additional_members:
                if self._verbose:
                    print(" > Unsubscribing %s" % member)
                target.delete_member(name, member)


    def _check_config(self):
        for name, list in self._lists.items():
            if not list['source'] in self._sources.keys():
                raise RuntimeError("List %s uses missing source %s" % (name, list['source']))
            if not list['target'] in self._targets.keys():
                raise RuntimeError("List %s uses missing target %s" % (name, list['target']))

            if self._verbose:
                print(" > Loaded list %s" % name)

    def _parse_config(self, h):
        self._config = configparser.ConfigParser()
        self._config.read_file(h)

        # Parse all different sources and targets
        for section in self._config.sections():
            s = self._config[section]

            if section == 'source':
                self._configure_source(s)
            elif section == 'target':
                self._configure_target(s)
            elif section == 'list':
                self._configure_list(s)
            else:
                raise RuntimeError('Unsupported section found: %s' % section)
    
    def _configure_source(self, s):
        # Check that we have a name for the source of data 
        if not "name" in s.keys():
            raise RuntimeError("Please provide a name for all configured sources")

        name = s['name']

        if not "module" in s.keys():
            raise RuntimeError("Please provide a module for the source %s" % name)

        if s['module'] == 'json':
            self._sources[name] = JsonSource(s['url'], s.get('user', None), s.get('password', None))
        else:
            raise RuntimeError("Unsupported module: %s" % s['module'])

        if self._verbose:
            print(" > Loaded source %s" % name)


    def _configure_target(self, s):
        # Check that we have a name for the source of data 
        if not "name" in s.keys():
            raise RuntimeError("Please provide a name for all configured targets")

        name = s['name']

        if not "module" in s.keys():
            raise RuntimeError("Please provide a module for the target %s" % name)

        if s['module'] == 'mailman3':
            self._targets[name] = MailmanServer(s['url'], s['user'], s['password'])
        else:
            raise RuntimeError("Unsupported module: %s" % s['module'])

        if self._verbose:
            print(" > Loaded target %s" % name)

    def _configure_list(self, s):
        # Check that we have a name for the source of data 
        if not "name" in s.keys():
            raise RuntimeError("Please provide a name for all configured lists")

        name = s['name']

        self._lists[name] = {
            'source': s['source'], 
            'target': s['target']
        }
