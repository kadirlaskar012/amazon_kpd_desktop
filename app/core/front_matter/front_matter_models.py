"""
Front Matter Data Models & Configuration for KDP Studio.
Supports book-type independent disclaimer & contents generation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import datetime


class PageType(str, Enum):
    FRONT_MATTER_DISCLAIMER = "front_matter_disclaimer"
    FRONT_MATTER_CONTENTS = "front_matter_contents"
    CONTENT = "content"
    BACK_MATTER = "back_matter"


class ContentsListStyle(str, Enum):
    NUMBERED = "numbered"
    BULLET = "bullet"
    PLAIN = "plain"


@dataclass
class DisclaimerFieldsConfig:
    book_title: bool = True
    subtitle: bool = True
    author_name: bool = True
    publisher_name: bool = True
    copyright_year: bool = True
    copyright_notice: bool = True
    all_rights_reserved: bool = True
    isbn: bool = False
    edition: bool = True
    website: bool = False
    contact_info: bool = False
    custom_text_enabled: bool = False
    
    # Text overrides / defaults
    custom_text: str = ""
    notice_template: str = "No part of this publication may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher."
    rights_text: str = "All rights reserved."
    edition_text: str = "First Edition"
    publisher_name_text: str = "KDP Creative Publishing"
    isbn_text: str = "978-X-XXXXX-XXX-X"
    website_text: str = "www.kdpbooks.com"
    contact_text: str = "support@kdpbooks.com"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "book_title": self.book_title,
            "subtitle": self.subtitle,
            "author_name": self.author_name,
            "publisher_name": self.publisher_name,
            "copyright_year": self.copyright_year,
            "copyright_notice": self.copyright_notice,
            "all_rights_reserved": self.all_rights_reserved,
            "isbn": self.isbn,
            "edition": self.edition,
            "website": self.website,
            "contact_info": self.contact_info,
            "custom_text_enabled": self.custom_text_enabled,
            "custom_text": self.custom_text,
            "notice_template": self.notice_template,
            "rights_text": self.rights_text,
            "edition_text": self.edition_text,
            "publisher_name_text": self.publisher_name_text,
            "isbn_text": self.isbn_text,
            "website_text": self.website_text,
            "contact_text": self.contact_text,
        }

    @classmethod
    def from_dict(cls, d: Optional[Dict[str, Any]]) -> "DisclaimerFieldsConfig":
        if not d:
            return cls()
        return cls(
            book_title=d.get("book_title", True),
            subtitle=d.get("subtitle", True),
            author_name=d.get("author_name", True),
            publisher_name=d.get("publisher_name", True),
            copyright_year=d.get("copyright_year", True),
            copyright_notice=d.get("copyright_notice", True),
            all_rights_reserved=d.get("all_rights_reserved", True),
            isbn=d.get("isbn", False),
            edition=d.get("edition", True),
            website=d.get("website", False),
            contact_info=d.get("contact_info", False),
            custom_text_enabled=d.get("custom_text_enabled", False),
            custom_text=d.get("custom_text", ""),
            notice_template=d.get("notice_template", "No part of this publication may be reproduced..."),
            rights_text=d.get("rights_text", "All rights reserved."),
            edition_text=d.get("edition_text", "First Edition"),
            publisher_name_text=d.get("publisher_name_text", "KDP Creative Publishing"),
            isbn_text=d.get("isbn_text", "978-X-XXXXX-XXX-X"),
            website_text=d.get("website_text", "www.kdpbooks.com"),
            contact_text=d.get("contact_text", "support@kdpbooks.com"),
        )


@dataclass
class FrontMatterConfig:
    auto_front_matter: bool = True
    create_disclaimer: bool = True
    create_contents: bool = True
    auto_sync_contents: bool = True
    contents_style: str = "numbered"  # numbered, bullet, plain
    show_page_numbers: bool = True
    contents_heading: str = "TABLE OF CONTENTS"
    disclaimer_fields: DisclaimerFieldsConfig = field(default_factory=DisclaimerFieldsConfig)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "auto_front_matter": self.auto_front_matter,
            "create_disclaimer": self.create_disclaimer,
            "create_contents": self.create_contents,
            "auto_sync_contents": self.auto_sync_contents,
            "contents_style": self.contents_style,
            "show_page_numbers": self.show_page_numbers,
            "contents_heading": self.contents_heading,
            "disclaimer_fields": self.disclaimer_fields.to_dict() if isinstance(self.disclaimer_fields, DisclaimerFieldsConfig) else self.disclaimer_fields,
        }

    @classmethod
    def from_dict(cls, d: Optional[Dict[str, Any]]) -> "FrontMatterConfig":
        if not d:
            return cls()
        fields_raw = d.get("disclaimer_fields")
        fields_obj = DisclaimerFieldsConfig.from_dict(fields_raw) if isinstance(fields_raw, dict) else DisclaimerFieldsConfig()
        return cls(
            auto_front_matter=d.get("auto_front_matter", True),
            create_disclaimer=d.get("create_disclaimer", True),
            create_contents=d.get("create_contents", True),
            auto_sync_contents=d.get("auto_sync_contents", True),
            contents_style=d.get("contents_style", "numbered"),
            show_page_numbers=d.get("show_page_numbers", True),
            contents_heading=d.get("contents_heading", "TABLE OF CONTENTS"),
            disclaimer_fields=fields_obj,
        )
