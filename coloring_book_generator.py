#!/usr/bin/env python3
"""
Adult Coloring Book Generator for Amazon KDP
Generates intricate line art designs and compiles into print-ready PDFs.
"""

import os
import json
import time
import random
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API Keys (set via environment variable)
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

# KDP Print Dimensions (in pixels at 300 DPI)
KDP_SIZES = {
    "8.5x11": (2550, 3300),      # Standard US Letter
    "8x10": (2400, 3000),         # Popular coloring book size
    "6x9": (1800, 2700),          # Trade paperback
    "8.25x8.25": (2475, 2475),    # Square format
}

# Coloring Book Themes with Prompts
THEMES = {
    "mandalas": {
        "name": "Mystical Mandalas",
        "prompts": [
            "intricate mandala pattern with geometric shapes and floral elements, black line art on white background, adult coloring book page, highly detailed symmetrical design",
            "zen mandala with lotus flowers and sacred geometry, clean black outlines on white, coloring page style, no shading",
            "celestial mandala with sun moon and stars pattern, detailed line drawing, adult coloring book, white background",
            "nature mandala with leaves vines and flowers, circular symmetrical design, black linework coloring page",
            "tribal mandala with ethnic patterns and symbols, intricate black line art, coloring book style",
        ]
    },
    "animals": {
        "name": "Enchanted Animals",
        "prompts": [
            "majestic lion portrait with decorative mane made of intricate patterns and flowers, adult coloring book style, black line art on white",
            "owl with ornate feathers filled with zentangle patterns, detailed coloring page, clean black outlines",
            "elephant decorated with mandala and paisley patterns, adult coloring book page, intricate line art",
            "wolf howling at moon with tribal patterns in fur, detailed line drawing for coloring, white background",
            "butterfly with intricate wing patterns and floral designs, adult coloring page, black linework",
            "peacock with elaborate tail feathers in zentangle style, coloring book art, detailed outlines",
            "fox with decorative fur patterns and nature elements, adult coloring page, clean lines",
            "horse with flowing mane filled with swirls and patterns, line art coloring page, intricate design",
        ]
    },
    "nature": {
        "name": "Botanical Gardens",
        "prompts": [
            "tropical flowers and leaves arrangement, detailed botanical illustration, adult coloring book style, black line art",
            "enchanted forest scene with mushrooms ferns and flowers, intricate line drawing for coloring, white background",
            "underwater coral reef with fish and sea plants, detailed coloring page, clean black outlines",
            "garden scene with roses lilies and vines, botanical coloring book page, intricate linework",
            "tree of life with detailed bark leaves and roots, adult coloring page, ornate line art",
            "succulent garden arrangement, detailed botanical drawing, coloring book style, clean lines",
        ]
    },
    "geometric": {
        "name": "Sacred Geometry",
        "prompts": [
            "complex geometric pattern with interlocking shapes, adult coloring book page, precise black line art on white",
            "optical illusion geometric design, intricate repeating pattern, coloring page style, clean outlines",
            "3D geometric tessellation pattern, adult coloring book, detailed line art, white background",
            "art deco geometric pattern with symmetrical design, coloring page, black linework",
            "islamic geometric tile pattern, intricate arabesque design, adult coloring book style",
        ]
    },
    "fantasy": {
        "name": "Fantasy Realms",
        "prompts": [
            "fairy sitting on mushroom in enchanted forest, intricate details, adult coloring book page, line art",
            "dragon with ornate scales and decorative patterns, detailed coloring page, black outlines on white",
            "mermaid with flowing hair and detailed tail patterns, adult coloring book style, line drawing",
            "unicorn with decorated mane and magical elements, intricate coloring page, clean black lines",
            "castle in clouds with fantasy landscape, detailed line art for coloring, adult coloring book",
            "phoenix rising with elaborate feather patterns, coloring book page, intricate linework",
        ]
    },
    "patterns": {
        "name": "Relaxing Patterns",
        "prompts": [
            "paisley pattern with intricate swirls and details, adult coloring book page, black line art on white",
            "zentangle abstract pattern with various textures, detailed coloring page, clean outlines",
            "damask wallpaper pattern, ornate repeating design, adult coloring book style, line art",
            "moroccan tile pattern with geometric and floral elements, coloring page, intricate lines",
            "art nouveau flowing pattern with organic curves, adult coloring book, detailed linework",
        ]
    },
    "inspirational": {
        "name": "Mindful Words",
        "prompts": [
            "word BREATHE surrounded by decorative swirls flowers and patterns, adult coloring book page, line art",
            "word PEACE with mandala and nature elements around it, coloring page style, intricate outlines",
            "word LOVE decorated with hearts flowers and ornate patterns, adult coloring book, black lines",
            "word DREAM with clouds stars and whimsical designs, coloring page, detailed line art",
            "word CREATE surrounded by artistic elements and patterns, adult coloring book style, clean lines",
        ]
    },
}


class ColoringBookGenerator:
    """Generate adult coloring book pages using AI."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.api_token = REPLICATE_API_TOKEN

    def generate_image_replicate(self, prompt: str, size: tuple = (2550, 3300)) -> Optional[str]:
        """Generate a coloring page using Replicate API."""

        # Enhanced prompt for line art
        full_prompt = f"{prompt}, black and white line art, no shading, no gradients, no gray tones, pure black lines on pure white background, high contrast, suitable for coloring, clean crisp lines, 300 DPI print quality"

        negative_prompt = "color, colored, shading, gradient, gray, grayscale, shadows, blur, low quality, photograph, realistic, 3d render"

        try:
            # Using SDXL for high quality line art
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers={
                    "Authorization": f"Token {self.api_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "version": "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",  # SDXL
                    "input": {
                        "prompt": full_prompt,
                        "negative_prompt": negative_prompt,
                        "width": min(size[0], 1024),  # SDXL max
                        "height": min(size[1], 1024),
                        "num_inference_steps": 30,
                        "guidance_scale": 7.5,
                    }
                },
                timeout=30
            )

            if response.status_code != 201:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return None

            prediction = response.json()
            prediction_id = prediction["id"]

            # Poll for completion
            for _ in range(60):  # 5 minute timeout
                time.sleep(5)

                status_response = requests.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}",
                    headers={"Authorization": f"Token {self.api_token}"},
                    timeout=30
                )

                if status_response.status_code == 200:
                    result = status_response.json()
                    if result["status"] == "succeeded":
                        output = result.get("output")
                        if output:
                            return output[0] if isinstance(output, list) else output
                    elif result["status"] == "failed":
                        logger.error(f"Generation failed: {result.get('error')}")
                        return None

            logger.error("Generation timed out")
            return None

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return None

    def download_image(self, url: str, filepath: Path) -> bool:
        """Download image from URL."""
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                filepath.write_bytes(response.content)
                return True
        except Exception as e:
            logger.error(f"Error downloading image: {e}")
        return False

    def generate_book(self, theme: str, num_pages: int = 30, book_title: str = None) -> Path:
        """Generate a complete coloring book."""

        if theme not in THEMES:
            raise ValueError(f"Unknown theme: {theme}. Available: {list(THEMES.keys())}")

        theme_data = THEMES[theme]
        title = book_title or theme_data["name"]
        safe_title = title.replace(" ", "_").replace(":", "")

        # Create book directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        book_dir = self.output_dir / f"{safe_title}_{timestamp}"
        book_dir.mkdir(parents=True, exist_ok=True)
        images_dir = book_dir / "images"
        images_dir.mkdir(exist_ok=True)

        logger.info(f"Generating coloring book: {title}")
        logger.info(f"Theme: {theme}, Pages: {num_pages}")
        logger.info(f"Output: {book_dir}")

        # Generate pages
        prompts = theme_data["prompts"]
        generated = []

        for i in range(num_pages):
            prompt = prompts[i % len(prompts)]

            # Add variety
            variations = [
                "",
                ", with extra fine details",
                ", with bold thick lines",
                ", with intricate background patterns",
                ", centered composition",
                ", full page design",
            ]
            prompt += random.choice(variations)

            logger.info(f"Generating page {i+1}/{num_pages}...")

            image_url = self.generate_image_replicate(prompt)

            if image_url:
                image_path = images_dir / f"page_{i+1:03d}.png"
                if self.download_image(image_url, image_path):
                    generated.append({
                        "page": i + 1,
                        "prompt": prompt,
                        "file": str(image_path.name)
                    })
                    logger.info(f"  Saved: {image_path.name}")
                else:
                    logger.warning(f"  Failed to download page {i+1}")
            else:
                logger.warning(f"  Failed to generate page {i+1}")

            # Rate limiting
            time.sleep(2)

        # Save metadata
        metadata = {
            "title": title,
            "theme": theme,
            "pages": num_pages,
            "generated": len(generated),
            "timestamp": timestamp,
            "pages_data": generated
        }

        metadata_file = book_dir / "metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))

        logger.info(f"Generated {len(generated)}/{num_pages} pages")
        logger.info(f"Book saved to: {book_dir}")

        return book_dir

    def create_pdf(self, book_dir: Path, size: str = "8.5x11") -> Optional[Path]:
        """Compile images into a print-ready PDF."""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import inch
            from PIL import Image
        except ImportError:
            logger.error("Install reportlab and Pillow: pip install reportlab Pillow")
            return None

        images_dir = book_dir / "images"
        if not images_dir.exists():
            logger.error(f"Images directory not found: {images_dir}")
            return None

        # Get all images
        images = sorted(images_dir.glob("*.png"))
        if not images:
            logger.error("No images found")
            return None

        # Load metadata
        metadata_file = book_dir / "metadata.json"
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            title = metadata.get("title", "Coloring Book")
        else:
            title = "Coloring Book"

        # Create PDF
        pdf_path = book_dir / f"{title.replace(' ', '_')}.pdf"

        # Use letter size for KDP
        page_width, page_height = letter

        c = canvas.Canvas(str(pdf_path), pagesize=letter)

        # Add title page
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(page_width/2, page_height/2 + 50, title)
        c.setFont("Helvetica", 18)
        c.drawCentredString(page_width/2, page_height/2 - 20, "Adult Coloring Book")
        c.showPage()

        # Add coloring pages
        margin = 0.5 * inch
        content_width = page_width - 2 * margin
        content_height = page_height - 2 * margin

        for img_path in images:
            try:
                img = Image.open(img_path)
                img_width, img_height = img.size

                # Calculate scaling to fit page
                scale = min(content_width / img_width, content_height / img_height)
                new_width = img_width * scale
                new_height = img_height * scale

                # Center on page
                x = (page_width - new_width) / 2
                y = (page_height - new_height) / 2

                c.drawImage(str(img_path), x, y, new_width, new_height)
                c.showPage()

            except Exception as e:
                logger.error(f"Error adding {img_path}: {e}")

        c.save()
        logger.info(f"PDF created: {pdf_path}")

        return pdf_path


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate Adult Coloring Books for KDP")
    parser.add_argument("--theme", choices=list(THEMES.keys()), default="mandalas",
                       help="Coloring book theme")
    parser.add_argument("--pages", type=int, default=30,
                       help="Number of pages (default: 30)")
    parser.add_argument("--title", type=str, default=None,
                       help="Custom book title")
    parser.add_argument("--output", type=str, default="output",
                       help="Output directory")
    parser.add_argument("--pdf", action="store_true",
                       help="Also create PDF")
    parser.add_argument("--list-themes", action="store_true",
                       help="List available themes")

    args = parser.parse_args()

    if args.list_themes:
        print("\nAvailable Themes:")
        print("-" * 40)
        for key, data in THEMES.items():
            print(f"  {key}: {data['name']}")
            print(f"    Prompts: {len(data['prompts'])}")
        return

    generator = ColoringBookGenerator(output_dir=args.output)

    book_dir = generator.generate_book(
        theme=args.theme,
        num_pages=args.pages,
        book_title=args.title
    )

    if args.pdf and book_dir:
        generator.create_pdf(book_dir)


if __name__ == "__main__":
    main()
