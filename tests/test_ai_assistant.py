"""
Automated Unit Tests for AI Amazon KDP Research & Metadata Assistant
"""

import pytest
from app.generators.ai_kdp_assistant import AIKDPAssistant


def test_ai_trending_niches_fallback():
    ai = AIKDPAssistant()
    niches = ai.get_trending_niche_ideas(target_age="Ages 4-8")
    assert isinstance(niches, list)
    assert len(niches) >= 5
    for n in niches:
        assert "niche_name" in n
        assert "demand_score" in n
        assert "sample_title" in n
        assert "recommended_price" in n
        assert n["demand_score"] >= 80


def test_ai_metadata_generation():
    ai = AIKDPAssistant()
    meta = ai.generate_kdp_metadata(
        topic_or_niche="Cute Safari Jungle Animals",
        book_type="coloring_book",
        target_age="Ages 2-4",
        author_name="Creative Kids Studio"
    )
    assert "title" in meta
    assert "subtitle" in meta
    assert "backend_keywords" in meta
    assert len(meta["backend_keywords"]) == 7
    for kw in meta["backend_keywords"]:
        assert len(kw) <= 70
    assert "recommended_categories" in meta
    assert len(meta["recommended_categories"]) >= 2
    assert "html_description" in meta
    assert "<h2>" in meta["html_description"] or "<h3>" in meta["html_description"]


def test_ai_key_storage_and_retrieval(tmp_path, monkeypatch):
    ai = AIKDPAssistant()
    saved = ai.save_api_key("test_mock_gemini_key_12345")
    assert saved is True
    assert ai.get_api_key() == "test_mock_gemini_key_12345"
