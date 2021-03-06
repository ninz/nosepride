from re import match
from os import getcwd
from os.path import commonprefix, relpath


class Traceback(object):

    def __init__(self, error):
        splitted_lines = error.splitlines()
        self.error_lines = iter(splitted_lines)

        self.assertion_message = splitted_lines[-1]
        self.formatted_lines = []

        self.skip_first_line()

    def skip_first_line(self):
        self.error_lines.next()

    def skip_a_line(self):
        self.error_lines.next()

    def format_line(self):
        matches = match(
            self.source_file_matcher, unicode(self.error_lines.next())
        )

        if matches:
            path, no, method = matches.groups()
            project_path = self.intersect(path)
            if not project_path is path:
                self.formatted_lines.append(
                    "# {0}:{1}:in {2}".format(project_path, no, method
                ))

    def report(self):
        try:
            while True:
                self.format_line()
        except StopIteration:
            return self.formatted_lines

    @staticmethod
    def intersect(path):
        if commonprefix([getcwd(), path]) != "/":
            return relpath(path, commonprefix([getcwd(), path]))
        else:
            return path

    @property
    def source_file_matcher(self):
        return r"^  File \"(.+)\", line (\d+), in (.*)$"
