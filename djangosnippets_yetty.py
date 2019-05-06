from collections import OrderedDict

from django.utils.translation import ugettext_noop as _
from django.contrib.auth.hashers import BasePasswordHasher


class PlainTextPassword(BasePasswordHasher):
    algorithm = 'plain'

    def salt(self):
        return ''

    def verify(self, password, encoded):
        return self.encode(password) == encoded

    def encode(self, password, salt=None):
        return "%s$1$%s" % (self.algorithm, password)

    def safe_summary(self, encoded):
        algorithm, iterations, password = encoded.split('$', 2)
        return OrderedDict([
            (_('algorithm'), algorithm),
            (_('iterations'), iterations),
            (_('password'), password),
        ])
