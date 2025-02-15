# -*- coding: utf-8 -*-

# Shamelessly copied from geocoder plugin's cache_utils.py

import logging
import os
import pwd
import tempfile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='Plugin: Text to speech | %(levelname)s - %(message)s')


class CustomTmpFile(object):

    def __init__(self, sub_directory=None):
        self.cache_relative_dir = '.tmp/dss/plugins/speech-to-text'
        if sub_directory:
            self.cache_relative_dir += '/{}'.format(sub_directory)
        self.tmp_output_dir = None

    def get_user_home_cache_location(self):
        """
        Return a per user cache location that is UIF safe
        :return: absolute location of cache
        """
        home_dir = pwd.getpwuid(os.getuid()).pw_dir
        cache_absolute_dir = os.path.join(home_dir, self.cache_relative_dir)
        if not os.path.exists(cache_absolute_dir):
            os.makedirs(cache_absolute_dir)
        return cache_absolute_dir

    def get_temporary_cache_dir(self):
        """
        Return a temporary directory with random name, output path will be:

            per_uid_cache_dir/random_dir/

        :return:
        """
        cache_absolute_path = self.get_user_home_cache_location()
        self.tmp_output_dir = tempfile.TemporaryDirectory(dir=cache_absolute_path)
        return self.tmp_output_dir

    def get_temporary_cache_file(self, output_file_name):
        """
        Return the path the temporary file in memory
        :param output_file_name:
        :return:
        """
        logger.info("Call to open method in upload exporter ...")
        cache_absolute_path = self.get_cache_location_from_user_config()
        # Create a random file path for the temporary write
        self.tmp_output_dir = tempfile.TemporaryDirectory(dir=cache_absolute_path)
        output_file = os.path.join(self.tmp_output_dir.name, output_file_name)
        return output_file

    def clean(self):
        """
        Remove cache
        :return:
        """
        self.tmp_output_dir.cleanup()
