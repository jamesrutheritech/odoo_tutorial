# estate/controllers/api.py

from odoo import http
from odoo.http import request
import json

class EstateAPIController(http.Controller):
    
    @http.route('/website/action/estate', type='http', auth='public', methods=['GET'], csrf=False)
    def get_properties(self, **kwargs):
        """
        Public API endpoint to retrieve published properties.
        Access: /website/action/estate
        """
        try:
            # Use sudo() to bypass access rights temporarily, 
            # but record rules will still apply
            properties = request.env['estate.property'].sudo().search([
                ('x_api_published', '=', True)
            ])
            
            # Prepare data for JSON response
            properties_data = []
            for prop in properties:
                property_dict = {
                    'id': prop.id,
                    'name': prop.name,
                    'description': prop.description or '',
                    'postcode': prop.postcode or '',
                    'expected_price': prop.expected_price,
                    'bedrooms': prop.bedrooms,
                    'living_area': prop.living_area,
                    'garden': prop.garden,
                    'garden_area': prop.garden_area,
                    'garden_orientation': prop.garden_orientation or '',
                    'state': prop.state,
                    'property_type': prop.x_property_type_id.name if prop.x_property_type_id else '',
                    'tags': [tag.name for tag in prop.x_property_tag_ids],
                }
                properties_data.append(property_dict)
            
            # Return JSON response
            return request.make_response(
                json.dumps({
                    'success': True,
                    'count': len(properties_data),
                    'properties': properties_data
                }, indent=2),
                headers=[
                    ('Content-Type', 'application/json'),
                    ('Access-Control-Allow-Origin', '*'),  # Enable CORS if needed
                ]
            )
            
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'success': False,
                    'error': str(e)
                }),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
