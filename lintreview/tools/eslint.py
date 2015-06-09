import logging
import os
from lintreview.tools import Tool
from lintreview.tools import run_command
from lintreview.utils import in_path
from lintreview.utils import npm_exists

log = logging.getLogger(__name__)


class Eslint(Tool):

    name = 'eslint'

    def check_dependencies(self):
        """
        See if eslint is on the system path.
        """
        return in_path('eslint') or npm_exists('eslint')

    def match_file(self, filename):
        base = os.path.basename(filename)
        name, ext = os.path.splitext(base)
        return ext == '.js'

    def process_files(self, files):
        """
        Run code checks with eslint.
        Only a single process is made for all files
        to save resources.
        """
        log.debug('Processing %s files with %s', files, self.name)
        command = self.create_command(files)
        output = run_command(
            command,
            ignore_error=True)
        self._process_checkstyle(output)

    def create_command(self, files):
        cmd = 'eslint'
        if npm_exists('eslint'):
            cmd = os.path.join(os.getcwd(), 'node_modules', '.bin', 'eslint')
        command = [cmd, '--format', 'checkstyle']
        # Add config file if its present
        if self.options.get('config'):
            command += ['--config', self.apply_base(self.options['config'])]
        command += files
        return command
