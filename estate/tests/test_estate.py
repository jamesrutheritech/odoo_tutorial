# estate/tests/test_estate.py (CLEANED VERSION)

from odoo.tests.common import TransactionCase, Form
from odoo.tests import tagged
from odoo.exceptions import UserError
# from . import test_estate # <--- Removed the incorrect self-import

@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.Property = cls.env["estate.property"]
        cls.Offer = cls.env["estate.property.offer"]
        cls.Partner = cls.env["res.partner"]
        cls.partner = cls.Partner.create({"name": "Partner Test"})
        
        # 1. Property for Forbidden Offer Test
        cls.property_sold = cls.Property.create({"name": "Sold Property for Offer Test"})
        cls.property_sold.state = "sold" # Set state directly for constraint test

        # 2. Property for Successful Sale Test
        cls.property_to_sell = cls.Property.create({"name": "Property Ready for Sale", "expected_price": 100000.0})
        cls.offer_accepted = cls.Offer.create({
            "price": 105000.0,
            "partner_id": cls.partner.id,
            "property_id": cls.property_to_sell.id,
        })
        # Use the action method to trigger all related business logic (e.g., setting selling_price)
        cls.offer_accepted.action_accept() 

        # 3. Property for Forbidden Sale Test (no accepted offer)
        cls.property_new = cls.Property.create({"name": "New Property for Forbidden Sale"})
        
        # 4. Property for Garden Onchange Test
        cls.property_garden = cls.Property.create({"name": "Garden Onchange Test"})

    # -----------------------------------------------------
    # TEST 1: Cannot create offer on sold property
    # -----------------------------------------------------
    def test_1_cannot_create_offer_on_sold_property(self):
        """Tests the constraint on estate.property.offer's create method."""
        with self.assertRaises(UserError):
            self.Offer.create({
                "price": 100000,
                "partner_id": self.partner.id,
                "property_id": self.property_sold.id, # Use pre-sold property
            })

    # -----------------------------------------------------
    # TEST 2: Cannot sell property without accepted offer
    # -----------------------------------------------------
    def test_2_cannot_sell_without_accepted_offer(self):
        """Tests the constraint on estate.property's action_sold method."""
        with self.assertRaises(UserError):
            self.property_new.action_sold() # Use property with no accepted offer

    # -----------------------------------------------------
    # TEST 3: Selling property with accepted offer works
    # -----------------------------------------------------
    def test_3_successful_sale(self):
        """Tests that action_sold works when an offer has been accepted."""
        # Property is already in 'offer_accepted' state from setUpClass
        self.property_to_sell.action_sold()

        # Check the final state
        self.assertEqual(self.property_to_sell.state, "sold", "Property should be marked as 'sold'.")

    # -----------------------------------------------------
    # TEST 4: Garden reset when garden is unchecked
    # -----------------------------------------------------
    def test_4_garden_reset(self):
        """Tests the @api.onchange('garden') method."""
        # Use the dedicated garden property
        form = Form(self.property_garden) 

        # 1. Set values
        form.garden = True
        form.garden_area = 50
        form.garden_orientation = 'south'

        # 2. Uncheck garden → onchange should reset
        form.garden = False
        rec = form.save()

        # Assertions
        self.assertEqual(rec.garden_area, 0, "Garden area should be reset to 0.")
        self.assertFalse(rec.garden_orientation, "Garden orientation should be reset to False.")