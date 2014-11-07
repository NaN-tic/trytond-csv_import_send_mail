# This file is part of csv_import_send_mail module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.tests.test_tryton import test_view, test_depends
import os
import sys
import trytond.tests.test_tryton
import unittest



class CSVImportSendMailTestCase(unittest.TestCase):
    'Test CSV Import Send Mail module'

    def setUp(self):
        trytond.tests.test_tryton.install_module('csv_import_send_mail')

    def test0005views(self):
        'Test views'
        test_view('csv_import_send_mail')

    def test0006depends(self):
        'Test depends'
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        CSVImportSendMailTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
