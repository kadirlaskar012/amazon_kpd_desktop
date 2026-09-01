"""
Disclaimer & Copyright Page Generator for KDP Book Studio.
Generates fully editable vector canvas pages containing copyright notices, publisher info, and legal metadata.
"""

import datetime
from typing import Dict, Any, List
from .front_matter_models import FrontMatterConfig, DisclaimerFieldsConfig


class DisclaimerGenerator:
    @staticmethod
    def generate_disclaimer_page(project_data: Dict[str, Any], config: Optional[FrontMatterConfig] = None) -> Dict[str, Any]:
        """
        Generates a standard editable Disclaimer & Copyright Page.
        """
        if config is None:
            config = FrontMatterConfig()

        fields: DisclaimerFieldsConfig = config.disclaimer_fields
        proj_name = project_data.get("name", "Untitled Book")
        author_name = project_data.get("author", "Author Name")
        current_year = str(datetime.datetime.now().year)

        elements: List[Dict[str, Any]] = []

        # 1. Outer Decorative Frame
        elements.append({
            "id": "disclaimer_frame",
            "type": "border",
            "x": 35,
            "y": 30,
            "w": 440,
            "h": 600,
            "locked": False
        })

        # 2. Main Book Title
        elements.append({
            "id": "disclaimer_title",
            "type": "title",
            "x": 45,
            "y": 70,
            "w": 420,
            "h": 40,
            "text": proj_name.upper(),
            "font_size": 24,
            "color": "#0f172a",
            "alignment": "center"
        })

        # 3. Subtitle / Book Edition
        elements.append({
            "id": "disclaimer_subtitle",
            "type": "title",
            "x": 45,
            "y": 120,
            "w": 420,
            "h": 25,
            "text": f"{fields.edition_text} • Premium KDP Edition",
            "font_size": 13,
            "color": "#475569",
            "alignment": "center"
        })

        # 4. Copyright Line
        copyright_text = f"Copyright © {current_year} by {author_name}"
        elements.append({
            "id": "disclaimer_copyright",
            "type": "title",
            "x": 45,
            "y": 200,
            "w": 420,
            "h": 25,
            "text": copyright_text,
            "font_size": 14,
            "color": "#1e293b",
            "alignment": "center"
        })

        # 5. Rights Reserved Notice
        elements.append({
            "id": "disclaimer_rights",
            "type": "title",
            "x": 45,
            "y": 230,
            "w": 420,
            "h": 20,
            "text": fields.rights_text,
            "font_size": 12,
            "color": "#475569",
            "alignment": "center"
        })

        # 6. Legal Notice Paragraph
        legal_p1 = "No part of this publication may be reproduced, distributed, or transmitted in any form"
        legal_p2 = "or by any means, including photocopying, recording, or other electronic methods,"
        legal_p3 = "without the prior written permission of the author and publisher."

        elements.append({
            "id": "disclaimer_notice_1",
            "type": "title",
            "x": 45,
            "y": 280,
            "w": 420,
            "h": 20,
            "text": legal_p1,
            "font_size": 10,
            "color": "#64748b",
            "alignment": "center"
        })
        elements.append({
            "id": "disclaimer_notice_2",
            "type": "title",
            "x": 45,
            "y": 305,
            "w": 420,
            "h": 20,
            "text": legal_p2,
            "font_size": 10,
            "color": "#64748b",
            "alignment": "center"
        })
        elements.append({
            "id": "disclaimer_notice_3",
            "type": "title",
            "x": 45,
            "y": 330,
            "w": 420,
            "h": 20,
            "text": legal_p3,
            "font_size": 10,
            "color": "#64748b",
            "alignment": "center"
        })

        # 7. Publisher & ISBN Info
        elements.append({
            "id": "disclaimer_publisher",
            "type": "title",
            "x": 45,
            "y": 420,
            "w": 420,
            "h": 20,
            "text": f"Published by: {fields.publisher_name_text}",
            "font_size": 11,
            "color": "#334155",
            "alignment": "center"
        })
        elements.append({
            "id": "disclaimer_isbn",
            "type": "title",
            "x": 45,
            "y": 450,
            "w": 420,
            "h": 20,
            "text": f"ISBN-13: {fields.isbn_text}",
            "font_size": 11,
            "color": "#334155",
            "alignment": "center"
        })

        # 8. Contact & Web info
        elements.append({
            "id": "disclaimer_contact",
            "type": "title",
            "x": 45,
            "y": 500,
            "w": 420,
            "h": 20,
            "text": f"Visit us: {fields.website_text} • Contact: {fields.contact_text}",
            "font_size": 10,
            "color": "#64748b",
            "alignment": "center"
        })

        # 9. Printed in USA notice
        elements.append({
            "id": "disclaimer_printed",
            "type": "title",
            "x": 45,
            "y": 560,
            "w": 420,
            "h": 20,
            "text": "Printed for Amazon KDP Distribution • First Printing",
            "font_size": 9,
            "color": "#94a3b8",
            "alignment": "center"
        })

        return {
            "page_number": 1,
            "page_type": "front_matter_disclaimer",
            "title": "Disclaimer & Copyright",
            "layout": "disclaimer_standard",
            "is_locked": False,
            "elements": elements
        }
