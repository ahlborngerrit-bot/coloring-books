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
HF_TOKEN = os.environ.get("HF_TOKEN")

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

# Removed controversial themes for production use
"""
ARCHIVED_THEMES = {
    "maga_rally": {
        "name": "MAGA Rally Warriors",
        "prompts": [
            # SINGLE CHARACTER - Obese scooter riders (BOLD & EASY style)
            "single morbidly obese man on mobility scooter, huge round belly, red MAGA hat, american flag cape, very thick black outlines, large simple shapes, minimal detail, bold and easy coloring book style, white background, no shading",
            "one very fat woman on electric scooter, massive body overflowing seat, flag shirt stretched tight, oxygen tank attached, extra thick outlines, big simple areas to color, minimalist coloring page",
            "single obese person on decorated scooter with multiple flags, huge belly resting on handlebars, red hat, thick bold black lines, large fill areas, simple shapes only, easy coloring book",

            # SINGLE CHARACTER - Gaunt/meth-head types (BOLD & EASY style)
            "single very skinny gaunt man, hollow cheeks, missing teeth showing, stringy hair, oversized MAGA shirt hanging on bony frame, extra thick outlines, simple shapes, bold easy coloring page, white background",
            "one skeletal thin woman with sunken face, bad teeth visible, cigarette, too-big red hat on small head, flag tank top on bony shoulders, thick black lines, large areas to color, minimal detail",
            "single emaciated man with visible cheekbones, toothless grin, scraggly beard, holding american flag, very thick outlines, simple bold shapes, easy coloring book style",

            # SINGLE CHARACTER - Biker/militia types (BOLD & EASY style)
            "single large biker man with leather vest covered in patches, big beer belly, long beard, bandana, american flag, extra thick black outlines, simple shapes, bold easy coloring page",
            "one man in tactical vest and camo pants, beer gut, red MAGA hat, holding flag, thick bold outlines, large simple areas, minimal detail coloring book style",
            "single bearded man in patriot militia costume, tactical gear on fat body, american flag cape, very thick lines, big simple shapes to color, white background",

            # SINGLE CHARACTER - QAnon Shaman type (BOLD & EASY style)
            "single shirtless man with horned fur hat like viking, face paint, holding flag on pole, round belly, thick black outlines, large simple shapes, bold easy coloring book, minimal detail",
            "one person in homemade patriot superhero costume, cape made of flag, face paint, big body, extra thick outlines, simple bold shapes, easy coloring page style",
            "single man dressed as Uncle Sam but trashy version, tall striped hat, flag suit too tight on fat body, thick lines, large areas to color, minimalist design",

            # TWO CHARACTERS - Contrast pairs (BOLD & EASY style)
            "two trump supporters side by side, one morbidly obese one skeleton thin, both in flag clothing and red hats, very thick outlines, large simple shapes, bold easy coloring book",
            "pair of rally goers, fat man on scooter next to gaunt skinny woman with cane, both toothless smiles, flags, extra thick black lines, simple shapes, minimal detail",
            "two people at rally, obese woman and emaciated man, mismatched couple in matching MAGA hats, thick bold outlines, big areas to color, easy coloring page",

            # RALLY STAGE SCENE - Simple (BOLD & EASY style)
            "simple trump rally stage with podium and big TRUMP sign, two flags on sides, jumbotron screen, very thick outlines, large shapes, minimal detail, bold easy coloring book style",
            "basic rally stage setup, podium center, american flags behind, simple crowd silhouettes below, extra thick black lines, big simple areas to color, minimalist",

            # PICKUP TRUCK SCENE (BOLD & EASY style)
            "single pickup truck covered in trump flags and stickers, obese driver visible, thick black outlines, large simple shapes, minimal detail, bold easy coloring page",
            "one big truck with flags in bed, gaunt skinny person standing in back waving flag, very thick lines, simple shapes only, easy coloring book style",
            "pickup truck tailgate scene, cooler and lawn chair, one fat person sitting one thin person standing, flags everywhere, thick bold outlines, large areas",

            # MERCHANDISE BOOTH - Simple (BOLD & EASY style)
            "simple merchandise table with red hats and flags displayed, one trashy looking vendor, thick black outlines, large shapes, minimal detail coloring book",
            "single booth selling trump merch, obese customer and thin vendor, table with hats, extra thick lines, big simple areas to color, bold easy style",

            # FOOD SCENE - Simple (BOLD & EASY style)
            "single obese person eating giant turkey leg at rally, grease on face, flag shirt, very thick outlines, large simple shapes, minimal detail, easy coloring page",
            "one fat man with huge belly holding corn dog and giant soda, red hat, mustard stains, thick bold black lines, simple shapes, coloring book style",
            "gaunt thin person at concession stand, hollow face, buying hot dog, simple booth behind, extra thick outlines, large areas to color, minimal detail",

            # SCOOTER PARADE - Simple (BOLD & EASY style)
            "three mobility scooters in row, each with obese rider, flags on each scooter, very thick black outlines, large simple shapes, bold easy coloring book, white background",
            "line of scooters with fat people, simple side view, flags waving, thick bold lines, big areas to fill, minimal detail, easy coloring page style",

            # WAITING IN LINE - Simple (BOLD & EASY style)
            "three people waiting in line, one fat one thin one medium, all in flag clothing, lawn chairs, cooler, thick outlines, simple shapes, bold easy coloring book",
            "simple line of rally goers, mix of body types, red hats, porta potty in background, very thick black lines, large areas to color, minimal detail",

            # FAMILY PORTRAIT - Simple (BOLD & EASY style)
            "trump supporter family of three, obese parents thin kid, matching flag shirts, red hats, thick black outlines, large simple shapes, bold easy coloring page",
            "trashy family at rally, grandma on scooter, fat dad, skinny mom, toothless smiles, flags, extra thick lines, simple shapes, minimal detail coloring book",

            # ARENA CROWD - Simplified (BOLD & EASY style)
            "simple arena scene, stage in back with TRUMP sign, rows of red hats as simple circles, few detailed people in front row mix of fat and thin, thick outlines, large shapes",
            "basic rally crowd from behind, sea of simple round heads with red hats, stage with flags in distance, very thick black lines, minimal detail, easy to color",

            # MORE SINGLE CHARACTERS (BOLD & EASY style)
            "single fat shirtless man at rally, huge hairy belly, sunburn, red hat, holding flag, very thick outlines, large simple shapes, bold easy coloring book style",
            "one obese woman in flag bikini top, big belly over shorts, bad teeth smile, holding sign, thick black lines, simple shapes, minimal detail coloring page",
            "single gaunt old man with oxygen tank, flag hospital gown, toothless, holding small flag, extra thick outlines, large areas to color, easy coloring book",
            "one thin unhealthy woman with stringy hair, cigarette, flag dress hanging loose, hollow cheeks, thick bold lines, simple shapes, minimal detail",
            "single large man in too-small flag speedo, big belly, red hat, hairy chest, very thick outlines, large simple shapes, bold easy coloring page style",
            "one skeletal person wrapped in flag like toga, bones showing, toothless grin, thick black lines, big simple areas, minimal detail coloring book",
        ]
    },
}
"""


class ColoringBookGenerator:
    """Generate adult coloring book pages using AI."""

    def __init__(self, output_dir: str = "output", backend: str = "huggingface", force_lineart: bool = False, lineart_method: str = "enhanced"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.api_token = REPLICATE_API_TOKEN
        self.hf_token = HF_TOKEN
        self.backend = backend  # "huggingface", "pollinations", or "replicate"
        self.force_lineart = force_lineart  # Post-process to pure B&W line art
        self.lineart_method = lineart_method  # "enhanced", "standard", or "detailed"

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

    def generate_image_pollinations(self, prompt: str, size: tuple = (1024, 1024)) -> Optional[bytes]:
        """Generate a coloring page using Pollinations.ai (completely free, no API key)."""
        import urllib.parse

        # IMPROVED: Generate high-contrast images that convert well to line art
        # Instead of trying to force the AI to make line art, we generate clear images
        # and convert them with our enhanced edge detection
        if self.force_lineart:
            # Optimized for edge detection conversion: high contrast, clear shapes
            full_prompt = f"{prompt}, high contrast illustration, clear defined edges, bold shapes, simple clean design, flat colors, cartoon style, clear outlines, no gradients, no blur, sharp edges, simple composition"
        else:
            # Traditional approach for direct line art generation
            full_prompt = f"{prompt}, BOLD AND EASY coloring book style, EXTRA THICK black outlines, LARGE simple shapes, MINIMAL detail, pure black lines on white background, NO shading NO gradients NO gray tones, simple chunky shapes easy to color, thick bold lineart, cartoon style simplicity, big areas to fill with color, no intricate patterns, no fine details"

        # URL-encode the prompt
        encoded_prompt = urllib.parse.quote(full_prompt)

        # Pollinations.ai API - completely free, no auth needed
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={size[0]}&height={size[1]}&nologo=true&model=flux"

        try:
            logger.info(f"  Requesting from Pollinations.ai...")
            response = requests.get(url, timeout=120)

            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'image' in content_type or len(response.content) > 10000:
                    logger.info(f"  Success! Got {len(response.content)} bytes")
                    return response.content
                else:
                    logger.warning(f"  Unexpected response: {content_type}")
            else:
                logger.warning(f"  Pollinations error: {response.status_code}")

        except requests.exceptions.Timeout:
            logger.warning("  Pollinations timed out, retrying...")
            try:
                response = requests.get(url, timeout=180)
                if response.status_code == 200:
                    return response.content
            except Exception as e:
                logger.warning(f"  Retry failed: {e}")
        except Exception as e:
            logger.warning(f"  Pollinations error: {e}")

        return None

    def generate_image_huggingface(self, prompt: str, size: tuple = (1024, 1024)) -> Optional[bytes]:
        """Generate a coloring page using HuggingFace free inference API."""

        # Enhanced prompt for line art - STRONG enforcement
        full_prompt = f"{prompt}, pure black ink lines on pure white paper, adult coloring book page, clean vector line art, no fills, no shading, no gradients, no gray, no halftones, only black outlines on white, high contrast linework, professional coloring book illustration, thick clean outlines ready for coloring"

        negative_prompt = "color, colored, red, blue, green, yellow, orange, purple, pink, shading, gradient, gray, grayscale, shadows, blur, photograph, realistic, 3d render, painted, watercolor, text, words, letters, writing, caption, label, signature, logo"

        # Try the new router API with different models
        models = [
            "black-forest-labs/FLUX.1-schnell",
            "stabilityai/stable-diffusion-xl-base-1.0",
            "stabilityai/stable-diffusion-2-1",
        ]

        for model in models:
            try:
                logger.info(f"  Trying model: {model}")

                # Use new router.huggingface.co endpoint
                response = requests.post(
                    f"https://router.huggingface.co/hf-inference/models/{model}",
                    headers={
                        "Authorization": f"Bearer {self.hf_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "inputs": full_prompt,
                        "parameters": {
                            "negative_prompt": negative_prompt,
                            "num_inference_steps": 25,
                            "guidance_scale": 7.5,
                        }
                    },
                    timeout=180
                )

                if response.status_code == 200:
                    # Response is the image bytes directly
                    content_type = response.headers.get('content-type', '')
                    if 'image' in content_type:
                        logger.info(f"  Success with {model}")
                        return response.content
                    else:
                        logger.warning(f"  Unexpected response type: {content_type}")
                elif response.status_code == 503:
                    # Model loading, wait and retry
                    logger.info(f"  Model loading, waiting...")
                    time.sleep(30)
                    # Retry same model
                    response = requests.post(
                        f"https://router.huggingface.co/hf-inference/models/{model}",
                        headers={
                            "Authorization": f"Bearer {self.hf_token}",
                            "Content-Type": "application/json"
                        },
                        json={"inputs": full_prompt},
                        timeout=180
                    )
                    if response.status_code == 200 and 'image' in response.headers.get('content-type', ''):
                        return response.content
                else:
                    logger.warning(f"  Model {model} failed: {response.status_code} - {response.text[:300]}")

            except requests.exceptions.Timeout:
                logger.warning(f"  Model {model} timed out")
            except Exception as e:
                logger.warning(f"  Model {model} error: {e}")

        return None

    def convert_to_coloring_page(self, image_bytes: bytes, method: str = "enhanced") -> bytes:
        """Post-process image to enforce pure black & white line art.

        Args:
            image_bytes: Input image as bytes
            method: 'enhanced' (thick bold lines), 'standard' (normal), or 'detailed' (fine lines)
        """
        try:
            import cv2
            import numpy as np
            from io import BytesIO
            from PIL import Image

            # Load image from bytes
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                logger.warning("Failed to decode image")
                return image_bytes

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            if method == "enhanced":
                # ENHANCED METHOD: Thick bold lines perfect for coloring
                # 1. Bilateral filter: smooth while preserving edges
                bilateral = cv2.bilateralFilter(gray, 9, 75, 75)

                # 2. Adaptive thresholding to find dark areas
                thresh = cv2.adaptiveThreshold(
                    bilateral, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY, 11, 2
                )

                # 3. Canny edge detection
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                edges = cv2.Canny(blurred, 30, 100)

                # 4. Combine edges with thresholded image
                combined = cv2.bitwise_and(edges, cv2.bitwise_not(thresh))

                # 5. Dilate for THICK outlines (perfect for coloring)
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
                thick_edges = cv2.dilate(combined, kernel, iterations=2)

                # 6. Clean up small noise
                kernel_clean = np.ones((2, 2), np.uint8)
                cleaned = cv2.morphologyEx(thick_edges, cv2.MORPH_CLOSE, kernel_clean)

                # 7. Invert: black lines on white background
                result = cv2.bitwise_not(cleaned)

            elif method == "detailed":
                # DETAILED METHOD: Fine lines for intricate designs
                # Apply Gaussian blur
                blurred = cv2.GaussianBlur(gray, (3, 3), 0)

                # Sensitive edge detection for details
                edges = cv2.Canny(blurred, 20, 60)

                # Minimal dilation
                kernel = np.ones((1, 1), np.uint8)
                edges = cv2.dilate(edges, kernel, iterations=1)

                # Invert
                result = cv2.bitwise_not(edges)

            else:  # standard
                # STANDARD METHOD: Balanced approach
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                edges = cv2.Canny(blurred, 30, 100)

                # Medium thickness
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
                edges = cv2.dilate(edges, kernel, iterations=1)

                result = cv2.bitwise_not(edges)

            # Final cleanup: ensure pure white background
            # Anything not pure black becomes white
            _, result = cv2.threshold(result, 250, 255, cv2.THRESH_BINARY)

            # Encode back to PNG bytes at high quality
            encode_params = [cv2.IMWRITE_PNG_COMPRESSION, 3]
            _, buffer = cv2.imencode('.png', result, encode_params)

            return buffer.tobytes()

        except ImportError:
            logger.warning("OpenCV not installed, skipping line art conversion")
            return image_bytes
        except Exception as e:
            logger.warning(f"Line art conversion failed: {e}")
            return image_bytes

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

            image_path = images_dir / f"page_{i+1:03d}.png"
            success = False

            if self.backend == "pollinations":
                # Pollinations.ai - completely free, no API key
                image_bytes = self.generate_image_pollinations(prompt)
                if image_bytes:
                    if self.force_lineart:
                        image_bytes = self.convert_to_coloring_page(image_bytes, method=self.lineart_method)
                    image_path.write_bytes(image_bytes)
                    success = True
            elif self.backend == "huggingface":
                # HuggingFace returns image bytes directly
                image_bytes = self.generate_image_huggingface(prompt)
                if image_bytes:
                    # Apply line art conversion if enabled
                    if self.force_lineart:
                        image_bytes = self.convert_to_coloring_page(image_bytes, method=self.lineart_method)
                    image_path.write_bytes(image_bytes)
                    success = True
            else:
                # Replicate returns a URL
                image_url = self.generate_image_replicate(prompt)
                if image_url:
                    success = self.download_image(image_url, image_path)
                    # Apply line art conversion if enabled
                    if success and self.force_lineart:
                        img_bytes = image_path.read_bytes()
                        converted = self.convert_to_coloring_page(img_bytes, method=self.lineart_method)
                        image_path.write_bytes(converted)

            if success:
                generated.append({
                    "page": i + 1,
                    "prompt": prompt,
                    "file": str(image_path.name)
                })
                logger.info(f"  Saved: {image_path.name}")
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
    parser.add_argument("--backend", choices=["pollinations", "huggingface", "replicate"], default="pollinations",
                       help="Image generation backend (default: pollinations - free, unlimited)")
    parser.add_argument("--force-lineart", action="store_true",
                       help="Post-process images to pure black & white line art using edge detection")
    parser.add_argument("--lineart-method", choices=["enhanced", "standard", "detailed"], default="enhanced",
                       help="Line art extraction method: enhanced (thick bold lines), standard (balanced), detailed (fine lines)")

    args = parser.parse_args()

    if args.list_themes:
        print("\nAvailable Themes:")
        print("-" * 40)
        for key, data in THEMES.items():
            print(f"  {key}: {data['name']}")
            print(f"    Prompts: {len(data['prompts'])}")
        return

    generator = ColoringBookGenerator(
        output_dir=args.output,
        backend=args.backend,
        force_lineart=args.force_lineart,
        lineart_method=args.lineart_method
    )

    book_dir = generator.generate_book(
        theme=args.theme,
        num_pages=args.pages,
        book_title=args.title
    )

    if args.pdf and book_dir:
        generator.create_pdf(book_dir)


if __name__ == "__main__":
    main()
