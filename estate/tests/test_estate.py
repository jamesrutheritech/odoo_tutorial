from . import test_estate
from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import UserError
from odoo.tests import Form


@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.Property = cls.env["estate.property"]
        cls.Offer = cls.env["estate.property.offer"]

        cls.property = cls.Property.create({
            "name": "Test Property",
        })

        cls.partner = cls.env["res.partner"].create({
            "name": "Partner Test",
        })

    # -----------------------------------------------------
    # TEST 1: Cannot create offer on sold property
    # -----------------------------------------------------
    def test_cannot_create_offer_on_sold_property(self):
        self.property.state = "sold"

        with self.assertRaises(UserError):
            self.Offer.create({
                "price": 100000,
                "partner_id": self.partner.id,
                "property_id": self.property.id,
            })

    # -----------------------------------------------------
    # TEST 2: Cannot sell property without accepted offer
    # -----------------------------------------------------
    def test_cannot_sell_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_sold()

    # -----------------------------------------------------
    # TEST 3: Selling property with accepted offer works
    # -----------------------------------------------------
    def test_successful_sale(self):
        offer = self.Offer.create({
            "price": 50000,
            "partner_id": self.partner.id,
            "property_id": self.property.id,
        })

        offer.status = "accepted"
        self.property.action_sold()

        self.assertEqual(self.property.state, "sold")

    # -----------------------------------------------------
    # TEST 4: Garden reset when garden is unchecked
    # -----------------------------------------------------
    def test_garden_reset(self):
        form = Form(self.property)

        form.garden = True
        form.garden_area = 50
        form.garden_orientation = 'south'

        # Uncheck garden → onchange should reset
        form.garden = False
        rec = form.save()

        self.assertEqual(rec.garden_area, 0)
        self.assertFalse(rec.garden_orientation)
