import logging

FORMAT = '%(asctime)s %(name)s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger()
logger.debug('this will probably not show up')
logger.warning('warning is above info, should appear')
