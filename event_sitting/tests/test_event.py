# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .. import exceptions
from openerp.tests.common import TransactionCase


class DuplicatedSittingCase(TransactionCase):
    def setUp(self):
        super(DuplicatedSittingCase, self).setUp()
        self.event = self.env.ref("event.event_0")
        # todo : create one sitting

    def test_allowed(self):
        """No problem when it is not forbidden."""
    # todo : create another sitting at same moment

    def test_forbidden(self):
        """Cannot when it is forbidden."""
        self.event.forbid_duplicates_sittings = True
    #    with self.assertRaises(exceptions.UniqueSittingValidationError):
        # todo : create another sitting at same moment

    # todo : modify this one
    def test_saved_in_exception(self):
        """The failing partners are saved in the exception."""
        self.event.forbid_duplicates = True
        # try:
        #     # todo create a copy
        # except exceptions.UniqueSittingValidationError as error:
        #     self.assertEqual(error._kwargs["registrations"], self.registration)

    # todo : modify this one
    def test_duplicates_already_exist(self):
        """Cannot forbid what already happened."""
        # todo create a copy
        #    with self.assertRaises(exceptions.UniqueSittingValidationError):
        # todo : ?
