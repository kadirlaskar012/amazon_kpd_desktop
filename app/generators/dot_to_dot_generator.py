"""
KDP Book Production Studio - Computer Vision Dot-to-Dot (Connect the Dots) Generator.
Converts any lineart/outline/drawing/photo into sequentially numbered vector dots (1..N) with normal-offset labels.
Also provides rich fallback vector preset shapes (Star, Butterfly, Dinosaur, Rocket, Cat, Heart, Airplane, Fish).
"""

import io
import base64
import math
from typing import List, Dict, Any, Optional, Tuple, Union
from PIL import Image
import numpy as np
try:
    import cv2
except ImportError:
    cv2 = None


class DotToDotGenerator:
    """
    Intelligent Computer Vision and Vector Contour Sampling Engine for Dot-to-Dot Puzzles.
    """

    @classmethod
    def from_image(
        cls,
        image_input: Union[bytes, str],
        dot_count: int = 35,
        canvas_w: int = 420,
        canvas_h: int = 460,
        margin: int = 25,
        faint_guide: bool = True
    ) -> Dict[str, Any]:
        """
        Extracts primary outer silhouette from image and generates N sequentially ordered dots.
        Guarantees 1:1 pixel-perfect overlay with the background image.
        """
        # 1. Decode image to numpy array
        if isinstance(image_input, str) and image_input.startswith("data:image"):
            _, encoded = image_input.split(",", 1)
            raw_bytes = base64.b64decode(encoded)
        elif isinstance(image_input, str):
            raw_bytes = base64.b64decode(image_input)
        else:
            raw_bytes = image_input

        pil_img = Image.open(io.BytesIO(raw_bytes))
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")

        np_img = np.array(pil_img)
        img_h, img_w = np_img.shape[:2]
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)

        # 2. Binary thresholding to isolate artwork foreground
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 235, 255, cv2.THRESH_BINARY_INV)

        # 3. Morphological Closing to seal sketches & FloodFill Solid Silhouette
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        closed_lines = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        flood_mask = np.zeros((img_h + 2, img_w + 2), np.uint8)
        filled = closed_lines.copy()
        cv2.floodFill(filled, flood_mask, (0, 0), 255)
        
        # Silhouette: Invert filled background and merge with lines
        silhouette = cv2.bitwise_not(filled)
        silhouette = cv2.bitwise_or(silhouette, closed_lines)
        silhouette = cv2.morphologyEx(silhouette, cv2.MORPH_CLOSE, kernel)

        # 4. Find the Single Main Outer Continuous Contour
        contours, _ = cv2.findContours(silhouette, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours:
            contours, _ = cv2.findContours(closed_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if not contours:
            return cls.generate_preset("star", dot_count=dot_count, canvas_w=canvas_w, canvas_h=canvas_h)

        primary_contour = max(contours, key=lambda cnt: cv2.contourArea(cnt), default=None)
        if primary_contour is None or len(primary_contour) < 5:
            return cls.generate_preset("star", dot_count=dot_count, canvas_w=canvas_w, canvas_h=canvas_h)

        # Smooth polygon slightly to avoid pixel staircase noise
        peri = cv2.arcLength(primary_contour, True)
        approx = cv2.approxPolyDP(primary_contour, epsilon=0.003 * peri, closed=True)
        pts = approx.reshape(-1, 2).astype(np.float32)

        # 5. Enforce Clockwise Progression & Top-Start (min_y)
        # Check orientation via shoelace / contour area
        if cv2.contourArea(pts, oriented=True) > 0:
            pts = pts[::-1] # Reverse to clockwise

        # Find top-most point to start (min_y)
        min_y_idx = int(np.argmin(pts[:, 1]))
        if min_y_idx != 0:
            pts = np.roll(pts, -min_y_idx, axis=0)

        # 6. Parametric Arc-Length Equidistant Sampling
        dists = [0.0]
        for i in range(1, len(pts)):
            d = np.linalg.norm(pts[i] - pts[i - 1])
            dists.append(dists[-1] + d)
        
        # Closing segment distance
        dists.append(dists[-1] + np.linalg.norm(pts[0] - pts[-1]))
        pts_closed = np.vstack([pts, pts[0]])

        sampled_pts = []
        step = dists[-1] / max(dot_count, 3)

        for k in range(dot_count):
            target_d = k * step
            idx = np.searchsorted(dists, target_d)
            idx = min(idx, len(pts_closed) - 1)
            
            if idx == 0:
                pt = pts_closed[0]
            else:
                d0 = dists[idx - 1]
                d1 = dists[idx]
                seg_len = d1 - d0
                ratio = (target_d - d0) / seg_len if seg_len > 1e-5 else 0.0
                pt = pts_closed[idx - 1] + ratio * (pts_closed[idx] - pts_closed[idx - 1])
            
            sampled_pts.append(pt)

        sampled_pts = np.array(sampled_pts, dtype=np.float32)

        # 7. 1:1 Pixel-Perfect Canvas Coordinate Scaling
        avail_w = canvas_w - (margin * 2)
        avail_h = canvas_h - (margin * 2)
        scale = min(avail_w / img_w, avail_h / img_h)

        scaled_img_w = round(img_w * scale, 1)
        scaled_img_h = round(img_h * scale, 1)
        img_x = round(margin + (avail_w - scaled_img_w) / 2.0, 1)
        img_y = round(margin + (avail_h - scaled_img_h) / 2.0, 1)

        # Centroid for normal vector label offsets
        center_x = img_x + (scaled_img_w / 2.0)
        center_y = img_y + (scaled_img_h / 2.0)

        dots = []
        for i, p in enumerate(sampled_pts):
            dot_num = i + 1
            sx = round(img_x + (p[0] * scale), 1)
            sy = round(img_y + (p[1] * scale), 1)

            # Normal vector from center to point
            vx = sx - center_x
            vy = sy - center_y
            norm = math.hypot(vx, vy)
            if norm < 1e-4:
                nx, ny = 0.0, -1.0
            else:
                nx = vx / norm
                ny = vy / norm

            # Label offset 13px outward
            label_x = round(sx + (nx * 13.0), 1)
            label_y = round(sy + (ny * 13.0), 1)

            dots.append({
                "num": dot_num,
                "x": sx,
                "y": sy,
                "label_x": label_x,
                "label_y": label_y,
                "is_start": (dot_num == 1)
            })

        return {
            "type": "dot_to_dot",
            "dot_count": len(dots),
            "dots": dots,
            "canvas_w": canvas_w,
            "canvas_h": canvas_h,
            "image_bounds": {
                "x": img_x,
                "y": img_y,
                "width": scaled_img_w,
                "height": scaled_img_h
            },
            "faint_guide": faint_guide,
            "show_lines": False,
            "has_reference": True
        }

    @classmethod
    def generate_preset(
        cls,
        preset_name: str = "star",
        dot_count: int = 30,
        canvas_w: int = 420,
        canvas_h: int = 460,
        margin: int = 35
    ) -> Dict[str, Any]:
        """
        Generates standard high-quality geometric/vector shapes for kids dot-to-dot books.
        """
        preset_key = preset_name.lower().strip()
        cx = canvas_w / 2.0
        cy = canvas_h / 2.0
        rx = (canvas_w - (margin * 2)) / 2.0
        ry = (canvas_h - (margin * 2)) / 2.0

        raw_points: List[Tuple[float, float]] = []

        if preset_key == "star":
            points_count = max(dot_count, 10)
            star_points = 5
            for i in range(points_count):
                angle = (i / points_count) * (2 * math.pi) - (math.pi / 2)
                # Alternate between outer and inner radius
                sub_step = (i * star_points * 2) / points_count
                r_scale = 0.45 + 0.55 * (0.5 + 0.5 * math.cos(sub_step * math.pi))
                px = cx + rx * r_scale * math.cos(angle)
                py = cy + ry * r_scale * math.sin(angle)
                raw_points.append((px, py))

        elif preset_key == "heart":
            points_count = max(dot_count, 20)
            for i in range(points_count):
                t = (i / points_count) * (2 * math.pi)
                # Parametric heart equation
                hx = 16 * (math.sin(t) ** 3)
                hy = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
                px = cx + (hx / 18.0) * rx
                py = (cy - 15) + (hy / 18.0) * ry
                raw_points.append((px, py))

        elif preset_key == "rocket":
            # Polygonal rocket profile
            base_poly = [
                (0, -1.0), (0.25, -0.7), (0.35, -0.2), (0.35, 0.4),
                (0.65, 0.7), (0.45, 0.7), (0.35, 0.55), (0.2, 0.65),
                (0.0, 0.55), (-0.2, 0.65), (-0.35, 0.55), (-0.45, 0.7),
                (-0.65, 0.7), (-0.35, 0.4), (-0.35, -0.2), (-0.25, -0.7)
            ]
            raw_points = cls._resample_polygon(base_poly, dot_count, cx, cy, rx, ry)

        elif preset_key == "butterfly":
            # Parametric butterfly curve
            points_count = max(dot_count, 24)
            for i in range(points_count):
                t = (i / points_count) * (2 * math.pi)
                r = (math.exp(math.cos(t)) - 2 * math.cos(4*t) + (math.sin(t / 12) ** 5))
                bx = math.sin(t) * r
                by = -math.cos(t) * r
                px = cx + (bx / 3.2) * rx
                py = cy + (by / 3.2) * ry
                raw_points.append((px, py))

        elif preset_key == "dinosaur":
            # Cute cartoon dino outline
            dino_poly = [
                (0.2, -0.9), (0.5, -0.8), (0.6, -0.5), (0.35, -0.4),
                (0.3, -0.1), (0.6, 0.2), (0.7, 0.4), (0.5, 0.5),
                (0.4, 0.8), (0.25, 0.8), (0.2, 0.5), (0.0, 0.5),
                (-0.05, 0.8), (-0.2, 0.8), (-0.25, 0.4), (-0.6, 0.5),
                (-0.8, 0.3), (-0.6, 0.1), (-0.3, 0.0), (-0.1, -0.4),
                (-0.05, -0.7), (0.1, -0.85)
            ]
            raw_points = cls._resample_polygon(dino_poly, dot_count, cx, cy, rx, ry)

        elif preset_key == "cat":
            # Cute cat head with ears
            cat_poly = [
                (0.0, -0.4), (0.3, -0.5), (0.7, -0.9), (0.75, -0.3),
                (0.85, 0.1), (0.6, 0.6), (0.3, 0.75), (0.0, 0.78),
                (-0.3, 0.75), (-0.6, 0.6), (-0.85, 0.1), (-0.75, -0.3),
                (-0.7, -0.9), (-0.3, -0.5)
            ]
            raw_points = cls._resample_polygon(cat_poly, dot_count, cx, cy, rx, ry)

        elif preset_key == "airplane":
            air_poly = [
                (0.0, -0.95), (0.15, -0.5), (0.15, -0.1), (0.9, 0.2),
                (0.85, 0.35), (0.15, 0.25), (0.12, 0.6), (0.35, 0.8),
                (0.3, 0.9), (0.0, 0.8), (-0.3, 0.9), (-0.35, 0.8),
                (-0.12, 0.6), (-0.15, 0.25), (-0.85, 0.35), (-0.9, 0.2),
                (-0.15, -0.1), (-0.15, -0.5)
            ]
            raw_points = cls._resample_polygon(air_poly, dot_count, cx, cy, rx, ry)

        else: # Fish default
            fish_poly = [
                (0.5, 0.0), (0.25, -0.4), (-0.2, -0.5), (-0.5, -0.2),
                (-0.8, -0.5), (-0.7, 0.0), (-0.8, 0.5), (-0.5, 0.2),
                (-0.2, 0.5), (0.25, 0.4)
            ]
            raw_points = cls._resample_polygon(fish_poly, dot_count, cx, cy, rx, ry)

        # Build dots list
        dots = []
        for i, (px, py) in enumerate(raw_points[:dot_count]):
            dot_num = i + 1
            vx = px - cx
            vy = py - cy
            norm = math.hypot(vx, vy)
            nx = (vx / norm) if norm > 1e-4 else 0.0
            ny = (vy / norm) if norm > 1e-4 else -1.0

            dots.append({
                "num": dot_num,
                "x": round(px, 1),
                "y": round(py, 1),
                "label_x": round(px + nx * 14.0, 1),
                "label_y": round(py + ny * 14.0, 1),
                "is_start": (dot_num == 1)
            })

        return {
            "type": "dot_to_dot",
            "preset": preset_key,
            "title": preset_key.replace("_", " ").title(),
            "dot_count": len(dots),
            "dots": dots,
            "canvas_w": canvas_w,
            "canvas_h": canvas_h,
            "faint_guide": True,
            "has_reference": True
        }

    @staticmethod
    def _resample_polygon(
        poly: List[Tuple[float, float]],
        target_count: int,
        cx: float,
        cy: float,
        rx: float,
        ry: float
    ) -> List[Tuple[float, float]]:
        """
        Interpolates polygon vertices into target_count equidistant points.
        """
        world_pts = [(cx + p[0] * rx, cy + p[1] * ry) for p in poly]
        world_pts.append(world_pts[0])

        dists = [0.0]
        for i in range(1, len(world_pts)):
            dx = world_pts[i][0] - world_pts[i-1][0]
            dy = world_pts[i][1] - world_pts[i-1][1]
            dists.append(dists[-1] + math.hypot(dx, dy))

        total_d = dists[-1]
        step = total_d / target_count
        resampled = []

        for k in range(target_count):
            td = k * step
            idx = 1
            while idx < len(dists) and dists[idx] < td:
                idx += 1
            if idx >= len(dists):
                idx = len(dists) - 1
            
            d0, d1 = dists[idx-1], dists[idx]
            seg_len = d1 - d0
            ratio = (td - d0) / seg_len if seg_len > 1e-4 else 0.0
            p0 = world_pts[idx-1]
            p1 = world_pts[idx]
            x = p0[0] + ratio * (p1[0] - p0[0])
            y = p0[1] + ratio * (p1[1] - p0[1])
            resampled.append((x, y))

        return resampled
