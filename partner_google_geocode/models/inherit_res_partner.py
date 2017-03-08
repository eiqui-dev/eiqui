# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Solucións Aloxa S.L. <info@aloxa.eu>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
import googlemaps
import logging

_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = ['res.partner']

    @api.multi
    def get_gelocation(self):
        website_id = self.env['website'].browser([1])
        gooClient = googlemaps.Client(key=website_id.google_maps_key)
        for record in self:
            address = self._display_address(record, without_company=True)
            gooRes = gooClient.geocode(address=address)
            _logger.info(gooRes)
            self.geo_lat = gooRes[0]
            record.geo_lon = gooRes[1]

    geo_lat = fields.Float(string="Latitude", default=0.0)
    geo_lon = fields.Float(string="Longitude", default=0.0)
