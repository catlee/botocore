# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import sys
import warnings
from tests import unittest, mock, BaseSessionTest

from botocore.exceptions import UnsupportedTLSVersionWarning


@unittest.skipIf(sys.version_info[:2] == (2, 6),
                 ("py26 is unable to detect openssl version"))
class TestOpensslVersion(BaseSessionTest):
    def test_incompatible_openssl_version(self):
        with mock.patch('ssl.OPENSSL_VERSION_INFO', new=(0, 9, 8, 11, 15)):
            with warnings.catch_warnings(record=True) as warn_messages:
                self.session.create_client('iot-data', 'us-east-1')
                self.assertIs(
                    warn_messages[0].category, UnsupportedTLSVersionWarning)

    def test_compatible_openssl_version(self):
        with mock.patch('ssl.OPENSSL_VERSION_INFO', new=(1, 0, 1, 1, 1)):
            with warnings.catch_warnings(record=True) as warn_messages:
                self.session.create_client('iot-data', 'us-east-1')
                self.assertEqual(len(warn_messages), 0)
