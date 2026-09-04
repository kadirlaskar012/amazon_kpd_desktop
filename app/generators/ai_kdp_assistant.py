"""
AI-Powered Amazon KDP Research & Metadata Assistant
Integrates Google Gemini AI API with fallback heuristic intelligence engine
for Trending Niche Ideas, Bestselling Titles, 7 Amazon Backend Keywords, Categories, and HTML Descriptions.
"""

import json
import os
import re
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "kdp_ai_config.json")


class AIKDPAssistant:
    """Intelligent Amazon KDP market research & metadata generation engine."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if not self.api_key and os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.api_key = cfg.get("gemini_api_key", "")
            except Exception:
                pass

    def save_api_key(self, key: str) -> bool:
        """Save Gemini API Key to local studio config."""
        self.api_key = key.strip()
        try:
            cfg = {}
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            cfg["gemini_api_key"] = self.api_key
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save AI config: {e}")
            return False

    def get_api_key(self) -> str:
        return self.api_key

    def _call_gemini(self, prompt: str) -> Optional[str]:
        """Call Gemini API via standard urllib if API key is configured."""
        if not self.api_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048,
            }
        }

        try:
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                candidates = res_data.get("candidates", [])
                if candidates:
                    text_parts = candidates[0].get("content", {}).get("parts", [])
                    if text_parts:
                        return text_parts[0].get("text", "")
        except Exception as e:
            print(f"Gemini API request failed (falling back to smart heuristic): {e}")
            return None
        return None

    def get_trending_niche_ideas(self, target_age: str = "Ages 4-8", book_category: str = "all") -> List[Dict[str, Any]]:
        """Generate high-demand, low-competition Amazon KDP children's book niches."""
        prompt = f"""
        Act as a top 1% Amazon KDP Publishing Strategist and Niche Research Expert.
        Generate 6 highly profitable, trending Amazon KDP children's activity book niches for target age '{target_age}' and book category '{book_category}'.
        Return ONLY valid raw JSON array of objects with the following schema:
        [
          {{
            "niche_name": "Toddler Cute Safari Animals Coloring Book",
            "target_age": "Ages 2-4",
            "book_type": "coloring_book",
            "demand_score": 94,
            "competition_level": "Low - Medium",
            "estimated_monthly_searches": "8,500+",
            "recommended_page_count": 50,
            "recommended_price": "$6.99",
            "hook_selling_point": "Bold lines, simple large animal shapes for tiny toddler hands.",
            "sample_title": "My First Big Animal Coloring Book: 50 Fun & Easy Illustrations for Toddlers Ages 2-4"
          }}
        ]
        """
        gemini_res = self._call_gemini(prompt)
        if gemini_res:
            try:
                # Strip markdown codeblocks if present
                clean_json = re.sub(r"^```json\s*|\s*```$", "", gemini_res.strip(), flags=re.MULTILINE)
                parsed = json.loads(clean_json)
                if isinstance(parsed, list) and len(parsed) > 0:
                    return parsed
            except Exception:
                pass

        # Intelligent Built-in Heuristic Database of Amazon KDP Bestselling Niches
        niches_db = [
            {
                "niche_name": "Toddler Cute Safari & Jungle Animals Coloring",
                "target_age": "Ages 2-4",
                "book_type": "coloring_book",
                "demand_score": 96,
                "competition_level": "Low",
                "estimated_monthly_searches": "12,400+",
                "recommended_page_count": 50,
                "recommended_price": "$6.99",
                "hook_selling_point": "Extra thick black lines, large simple shapes, no bleed-through blank backs.",
                "sample_title": "My First Big Toddler Jungle Coloring Book: 50+ Easy Animals for Ages 2-4"
            },
            {
                "niche_name": "Magical Unicorns & Princesses Scissor Skills Activity",
                "target_age": "Ages 3-5",
                "book_type": "scissor_skills",
                "demand_score": 92,
                "competition_level": "Low",
                "estimated_monthly_searches": "9,800+",
                "recommended_page_count": 48,
                "recommended_price": "$7.99",
                "hook_selling_point": "Progressive cutting exercises from straight lines to cute cut-and-paste craft shapes.",
                "sample_title": "Scissor Skills Activity Book for Kids: Cut & Paste Magical Unicorns & Fairies"
            },
            {
                "niche_name": "Dinosaur & Space Adventures Dot-to-Dot Numbers 1-50",
                "target_age": "Ages 4-8",
                "book_type": "dot_to_dot",
                "demand_score": 90,
                "competition_level": "Low - Medium",
                "estimated_monthly_searches": "8,200+",
                "recommended_page_count": 54,
                "recommended_price": "$7.99",
                "hook_selling_point": "Numbered connect-the-dots that turn into coloring pages with faint guide lines.",
                "sample_title": "Dinosaur Dot to Dot for Kids Ages 4-8: 50+ Challenging Connect the Dots Puzzles"
            },
            {
                "niche_name": "Primary Handwriting & Letter Tracing Workbook",
                "target_age": "Ages 3-6",
                "book_type": "tracing",
                "demand_score": 98,
                "competition_level": "Medium",
                "estimated_monthly_searches": "24,000+",
                "recommended_page_count": 80,
                "recommended_price": "$8.99",
                "hook_selling_point": "3-line penmanship guidelines with directional arrows and sight words tracing.",
                "sample_title": "Letter and Number Tracing Book for Preschoolers: Learn to Write Alphabet A to Z"
            },
            {
                "niche_name": "Animal Kingdom Shadow Matching & Visual Brain Games",
                "target_age": "Ages 3-6",
                "book_type": "shadow_matching",
                "demand_score": 88,
                "competition_level": "Very Low",
                "estimated_monthly_searches": "6,500+",
                "recommended_page_count": 44,
                "recommended_price": "$6.99",
                "hook_selling_point": "Develops visual cognitive recognition by connecting cute animals to their shadows.",
                "sample_title": "Shadow Matching Activity Book for Toddlers: Find and Match Cute Animal Pairs"
            },
            {
                "niche_name": "I-SPY & How Many? Kindergarten Counting Activity",
                "target_age": "Ages 4-7",
                "book_type": "ispy",
                "demand_score": 91,
                "competition_level": "Low",
                "estimated_monthly_searches": "11,000+",
                "recommended_page_count": 50,
                "recommended_price": "$7.99",
                "hook_selling_point": "Engaging visual search puzzles where kids find, count, and color objects.",
                "sample_title": "I Spy With My Little Eye Everything: Fun Search and Find Counting Activity Book"
            }
        ]
        return niches_db

    def generate_kdp_metadata(
        self,
        topic_or_niche: str,
        book_type: str = "coloring_book",
        target_age: str = "Ages 4-8",
        author_name: str = "Creative Kids Studio",
        page_count: int = 50,
        trim_size: str = "8.5x11"
    ) -> Dict[str, Any]:
        """Generate complete Amazon KDP Title, Subtitle, 7 Backend Keywords, Categories, and HTML Description."""
        # Calculate Amazon KDP B&W Printing Cost (US Market)
        if page_count <= 108:
            print_cost = 2.30
        else:
            print_cost = round(1.00 + (page_count * 0.012), 2)
        floor_price = round(print_cost / 0.60, 2)
        launch_profit = round((6.99 * 0.60) - print_cost, 2)
        regular_profit = round((7.99 * 0.60) - print_cost, 2)

        prompt = f"""
        Act as an Amazon KDP Bestseller Publishing Copywriter and SEO Specialist.
        Generate high-converting Amazon metadata for a Children's Activity Book:
        - Topic / Theme: "{topic_or_niche}"
        - Book Type: "{book_type}"
        - Target Age: "{target_age}"
        - Author: "{author_name}"
        - Page Count: {page_count} pages
        - Trim Size: {trim_size}

        CRITICAL AMAZON KDP RULES:
        1. Title: Catchy, memorable, includes primary high-volume keyword (Max 60 chars).
        2. Subtitle: Rich with secondary buyer intent keywords, age group, and number of pages/features (Max 150 chars).
        3. 7 Backend Keywords: Exactly 7 distinct search phrases (<50 chars each). DO NOT repeat words already used in the Title!
        4. Categories: 3 best Amazon KDP BISAC Categories.
        5. HTML Description: Professional Amazon HTML formatted sales copy with <h2>, <b>, <ul>, <li>, emojis, and call-to-action.

        Return ONLY valid raw JSON with this exact structure:
        {{
          "title": "Title Here",
          "subtitle": "Subtitle Here",
          "author": "{author_name}",
          "backend_keywords": [
            "keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5", "keyword 6", "keyword 7"
          ],
          "recommended_categories": [
            "Children's Books > Activities, Crafts & Games > Activity Books",
            "Children's Books > Early Learning > Basic Concepts",
            "Children's Books > Animals"
          ],
          "html_description": "<h3>...</h3><p>...</p><ul><li>...</li></ul>",
          "target_audience": "Toddlers, Preschoolers, Kindergarteners {target_age}",
          "recommended_list_price": "$6.99"
        }}
        """
        gemini_res = self._call_gemini(prompt)
        if gemini_res:
            try:
                clean_json = re.sub(r"^```json\s*|\s*```$", "", gemini_res.strip(), flags=re.MULTILINE)
                parsed = json.loads(clean_json)
                if isinstance(parsed, dict) and "title" in parsed:
                    parsed["pricing_strategy"] = {
                        "page_count": page_count,
                        "trim_size": trim_size,
                        "printing_cost": print_cost,
                        "floor_price": floor_price,
                        "recommended_launch_price": 6.99,
                        "launch_royalty_profit": launch_profit,
                        "recommended_regular_price": 7.99,
                        "regular_royalty_profit": regular_profit,
                        "advice": f"For your {page_count}-page {trim_size} book, launch at $6.99 to capture quick sales & reviews (earning ${launch_profit:.2f}/sale), then raise to $7.99 (earning ${regular_profit:.2f}/sale)."
                    }
                    return parsed
            except Exception:
                pass

        # Smart Heuristic Metadata Generator Engine
        clean_topic = topic_or_niche.strip().title() or "Jungle Animals"
        b_type_title = book_type.replace("_", " ").title()

        title = f"My First {clean_topic} {b_type_title}"
        subtitle = f"{page_count}+ Fun, Easy & Engaging Activity Pages for Kids {target_age} | Learn, Color & Create ({trim_size}\")"

        keywords_map = {
            "coloring_book": [
                "preschool animal coloring pages for boys and girls",
                "easy big simple bold outlines for tiny hands",
                "cute toddler travel quiet time activity gifts",
                "kindergarten fine motor skills practice workbook",
                "relaxing mindful screen free art creative pad",
                "single sided bleed safe illustrations gift idea",
                "birthday holiday stocking stuffer for little kids"
            ],
            "dot_to_dot": [
                "connect the dots numbers 1 to 50 puzzle book",
                "preschool number sequencing counting game",
                "educational visual motor coordination worksheets",
                "screen free travel activity workbook for kids",
                "faint guide numbered drawing puzzle sheets",
                "kindergarten math counting practice brain teaser",
                "fun animal picture reveals connect dots pad"
            ],
            "tracing": [
                "preschool handwriting lines letter practice A to Z",
                "sight words and number tracing 1 to 20 workbook",
                "3 line primary penmanship dotted guides arrows",
                "learn to write alphabet practice for kindergarten",
                "pencil control motor skills exercise workbook",
                "early childhood phonics letter formation sheets",
                "homeschool pre k writing readiness daily drills"
            ],
            "scissor_skills": [
                "preschool cutting practice cut and paste workbook",
                "straight zigzag wavy line safety scissors game",
                "toddler fine motor skill developmental craft book",
                "kindergarten paper cutting shapes puzzle pad",
                "creative arts and crafts gift for preschool kids",
                "hand eye coordination cut glue activity pages",
                "fun scissor practice screen free classroom pad"
            ],
            "shadow_matching": [
                "animal silhouette matching brain teaser puzzle",
                "visual perception cognitive development game",
                "preschool find and connect pairs activity pad",
                "early learning shape recognition visual workout",
                "toddler matching games screen free road trip book",
                "critical thinking logic puzzles for little kids",
                "fun animal shadows pair connection worksheets"
            ],
            "ispy": [
                "search and find hidden objects counting puzzle",
                "can you find and count picture game for kids",
                "look and find kindergarten attention focus game",
                "toddler visual discrimination activity workbook",
                "fun brain quest observation puzzle pages",
                "count color and check off animal game pad",
                "interactive screen free boredom buster book"
            ]
        }

        keywords = keywords_map.get(book_type, [
            f"{clean_topic.lower()} activities for kids {target_age.lower()}",
            "preschool early learning brain teaser workbook",
            "fine motor skills coordination developmental book",
            "screen free quiet time travel activity pad",
            "kindergarten classroom homeschool supplemental",
            "birthday gift holiday stocking stuffer little kids",
            "creative engaging fun daily practice worksheets"
        ])

        html_desc = f"""<h2>🎉 Spark Creativity & Endless Fun with the Ultimate {clean_topic} {b_type_title}! 🌟</h2>

<p>Looking for a fun, engaging, and screen-free way to boost your child's creativity and cognitive skills? <b>{title}</b> is specially designed for little learners ({target_age}) to develop hand-eye coordination, focus, and artistic confidence!</p>

<h3>⭐ What Makes This Book Special:</h3>
<ul>
  <li><b>{page_count}+ Unique & Fun Pages:</b> Carefully crafted with clean, bold lines and charming designs children adore.</li>
  <li><b>Perfect for Little Hands:</b> Generous {trim_size} inch format provides ample drawing and activity space.</li>
  <li><b>Single-Sided Bleed-Safe Pages:</b> Blank back pages prevent bleed-through from markers, pens, and crayons.</li>
  <li><b>Builds Vital Early Skills:</b> Enhances fine motor control, pencil grip, cognitive focus, and creative imagination.</li>
  <li><b>Ideal Screen-Free Gift:</b> Perfect for birthdays, holidays, road trips, rainy days, and homeschool activities!</li>
</ul>

<p><b>✨ Grab your copy today and watch your little one's creativity soar! 🚀</b></p>"""

        return {
            "title": title,
            "subtitle": subtitle,
            "author": author_name,
            "backend_keywords": keywords,
            "recommended_categories": [
                "Children's Books > Activities, Crafts & Games > Activity Books",
                "Children's Books > Early Learning > Basic Concepts",
                "Children's Books > Animals"
            ],
            "html_description": html_desc,
            "target_audience": f"Toddlers & Kids {target_age}",
            "recommended_list_price": "$6.99",
            "pricing_strategy": {
                "page_count": page_count,
                "trim_size": trim_size,
                "printing_cost": print_cost,
                "floor_price": floor_price,
                "recommended_launch_price": 6.99,
                "launch_royalty_profit": launch_profit,
                "recommended_regular_price": 7.99,
                "regular_royalty_profit": regular_profit,
                "advice": f"For your {page_count}-page {trim_size} book, launch at $6.99 to capture quick sales & reviews (earning ${launch_profit:.2f}/sale), then raise to $7.99 (earning ${regular_profit:.2f}/sale)."
            }
        }
