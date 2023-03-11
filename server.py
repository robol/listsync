#
# ListSync script -- this script synchronizes mailing list users from different
# sources.

import sys, traceback, time, argparse, logging

from listsync.server import Instance
from listsync.log import logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Keep mailing list member in sync.')

    parser.add_argument('--config', dest='config', type=str,
        default='config.ini',
        help='configuration file for the server')

    parser.add_argument('--verbose', dest='verbose', action='store_const',
        const=True, default=False,
        help='print a detailed log of the server operation')

    parser.add_argument('--interval', dest = 'interval', type = int,
        help = 'number of minutes to wait between updates', default = 30)

    args = parser.parse_args()
    interval = args.interval * 60

    logger.setLevel("INFO" if args.verbose else "WARNING")

    config_file = args.config

    instance = None

    try:
        with open(config_file, "r") as handle:
            instance = Instance(handle)
    except Exception as e:
        print("Error loading the configuration file: %s" % config_file)
        print(traceback.format_exc())

    # Start the server
    if instance is not None:
        while True:
            try:
                instance.sync()
                # logger.info("Sleeping, next sync will happen in %d seconds" % interval)
                if interval == 0:
                    break
                time.sleep(interval)
            except KeyboardInterrupt:
                sys.exit(0)
