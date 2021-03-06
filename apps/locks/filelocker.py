# coding: utf-8
from django.conf import settings
import os
import subprocess
import shutil
from django.utils.crypto import get_random_string
from django.utils.timezone import now as django_now


class FileLocker(object):

    def __init__(self):
        self._working_dir_path = self._create_working_dir_path()
        self._container_name = self._create_container_name()

    def _create_working_dir_path(self):
        return '%s/%s' % (
            settings.FILELOCKER_WORKING_ROOT,
            get_random_string(32),
        )

    def _create_container_name(self):
        return django_now().strftime('gs-locked-%Y%m%d%H%M%S')

    def _copy(self, uploaded_file, destination_file_path):
        fh = open(destination_file_path, 'w')
        for chunk in uploaded_file.chunks():
            fh.write(chunk)
        fh.close()

    def _to_zip(self, zip_file_path, zipped_dir_path, password):
        subprocess.check_output([
            'zip',
            '-r',
            '-j',
            '-P' + password,
            zip_file_path,
            zipped_dir_path,
        ])

    def lock(self, uploaded_file, password):
        os.makedirs(self._get_container_dir_path())
        self._copy(
            uploaded_file,
            self._get_container_dir_path() + '/' + uploaded_file.name
        )
        self._to_zip(
            self.get_locked_file_path(),
            self._get_container_dir_path(),
            password
        )

    def _get_container_dir_path(self):
        return self._working_dir_path + '/' + self._container_name

    def get_locked_file_name(self):
        return self._container_name + '.zip'

    def get_locked_file_path(self):
        return self._working_dir_path + '/' + self.get_locked_file_name()

    def clean(self):
        shutil.rmtree(self._working_dir_path)
