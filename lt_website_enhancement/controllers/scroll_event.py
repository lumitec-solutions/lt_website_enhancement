##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
import base64
import datetime
SITEMAP_CACHE_TIME = datetime.timedelta(hours=12)
LOC_PER_SITEMAP = 45000
import logging
from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.web import Home
_logger = logging.getLogger(__name__)


class WebsiteVisitor(Home):

    @http.route('/sitemap.xml', type='http', auth="public", website=True,
                multilang=False, sitemap=False)
    def sitemap_xml_index(self, **kwargs):
        current_website = request.website
        Attachment = request.env['ir.attachment'].sudo()
        View = request.env['ir.ui.view'].sudo()
        mimetype = 'application/xml;charset=utf-8'
        content = None
        dom = [('url', '=', '/sitemap-%d.xml' % current_website.id),
               ('type', '=', 'binary')]
        sitemap = Attachment.search(dom, limit=1)
        if sitemap:
            content = base64.b64decode(sitemap.datas)
        return request.make_response(content, [('Content-Type', mimetype)])

    @http.route(['/website/update_visitor_last_connection'], type='json',
                auth="public", website=True)
    def update_visitor_last_connection(self):
        """Update last_connection_datetime based on scrolling the website"""
        visitor_sudo = request.env['website.visitor']._get_visitor_from_request()
        if visitor_sudo:
            visitor_sudo.write({'last_connection_datetime': datetime.now()})
            return True
        return False
