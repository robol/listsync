#
# ListSync script -- this script synchronizes mailing list users from different
# sources.

import sys, traceback, time, argparse

from listsync.server import Instance

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Keep mailing list member in sync.')

    parser.add_argument('--config', dest='config', type=str,
        help='configuration file for the server')

    parser.add_argument('--verbose', dest='verbose', action='store_const',
        const=True, default=False,
        help='print a detailed log of the server operation')

    parser.add_argument('--interval', dest = 'interval', type = int,
        help = 'number of minutes to wait between updates', default = 30)

    args = parser.parse_args()
    interval = args.interval * 60

    config_file = args.config

    try:
        with open(config_file, "r") as handle:
            instance = Instance(handle, args.verbose)
    except Exception as e:
        print("Error loading the configuration file: %s" % config_file)
        print(traceback.format_exc())

    # Start the server
    while True:
        try:
            instance.sync()
            time.sleep(interval)
        except KeyboardInterrupt:
            sys.exit(0)
