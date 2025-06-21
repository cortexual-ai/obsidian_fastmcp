import asyncio
import logging
import os
import re
import requests
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

from config.settings import get_vault_path
from tools.read_note import read_note
from tools.update_note import update_note

logger = logging.getLogger(__name__)

async def add_image_to_note(
    title: str, 
    search_query_or_url: str, 
    image_source: Literal["web_search", "screenshot", "direct_url"], 
    folder: str = ""
) -> dict:
    """
    Add an image to an existing Obsidian note.
    
    Args:
        title: The title of the note to add the image to
        search_query_or_url: Either a search query for web_search, or URL for screenshot/direct_url
        image_source: The method to obtain the image
        folder: The folder containing the note (optional)
        
    Returns:
        dict: Status of the operation and image information
        
    Raises:
        Exception: If the note cannot be found or image cannot be added
    """
    try:
        logger.info(f"Adding image to note: {title}, source: {image_source}")
        
        # Read the existing note
        note = await read_note(title, folder)
        
        # Ensure attachments folder exists
        vault_path = get_vault_path()
        attachments_path = vault_path / "attachments"
        attachments_path.mkdir(exist_ok=True)
        
        # Get image based on source type
        if image_source == "web_search":
            image_path, image_filename = await _search_and_download_image(search_query_or_url, attachments_path)
        elif image_source == "screenshot":
            image_path, image_filename = await _take_screenshot(search_query_or_url, attachments_path)
        elif image_source == "direct_url":
            image_path, image_filename = await _download_image_from_url(search_query_or_url, attachments_path)
        else:
            raise ValueError(f"Invalid image_source: {image_source}")
        
        # Add image markdown to note content
        image_markdown = f"![{search_query_or_url}](attachments/{image_filename})"
        note.content = f"{note.content}\n\n{image_markdown}"
        
        # Update the note
        result = await update_note(note)
        
        logger.info(f"Image added successfully to note: {title}")
        return {
            "message": "Image added to note successfully",
            "note_title": title,
            "image_path": str(image_path),
            "image_filename": image_filename,
            "update_result": result
        }
        
    except Exception as e:
        logger.error(f"Error adding image to note: {str(e)}", exc_info=True)
        raise Exception(f"Failed to add image to note: {str(e)}")

async def _search_and_download_image(query: str, attachments_path: Path) -> tuple[Path, str]:
    """Search for an image and download the first result."""
    try:
        # Simple image search using DuckDuckGo (doesn't require API key)
        search_url = f"https://duckduckgo.com/?q={query}+image&iax=images&ia=images"
        
        # Use selenium to get search results
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            driver.get(search_url)
            
            # Wait for images to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
            )
            
            # Find the first meaningful image (skip icons/logos)
            images = driver.find_elements(By.CSS_SELECTOR, "img")
            image_url = None
            
            for img in images:
                src = img.get_attribute("src")
                if src and ("http" in src) and (img.size["width"] > 100) and (img.size["height"] > 100):
                    image_url = src
                    break
            
            if not image_url:
                raise Exception("No suitable images found in search results")
                
            logger.info(f"Found image URL: {image_url}")
            
        finally:
            driver.quit()
        
        # Download the image
        return await _download_image_from_url(image_url, attachments_path)
        
    except Exception as e:
        logger.error(f"Error searching for image: {str(e)}", exc_info=True)
        raise Exception(f"Failed to search for image: {str(e)}")

async def _take_screenshot(url: str, attachments_path: Path) -> tuple[Path, str]:
    """Take a screenshot of a webpage."""
    try:
        logger.info(f"Taking screenshot of: {url}")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Generate filename from URL
            parsed_url = urlparse(url)
            safe_filename = re.sub(r'[^\w\-_.]', '_', f"{parsed_url.netloc}_{parsed_url.path}")
            filename = f"screenshot_{safe_filename}_{int(asyncio.get_event_loop().time())}.png"
            image_path = attachments_path / filename
            
            # Take screenshot
            driver.save_screenshot(str(image_path))
            
            logger.info(f"Screenshot saved: {image_path}")
            return image_path, filename
            
        finally:
            driver.quit()
            
    except Exception as e:
        logger.error(f"Error taking screenshot: {str(e)}", exc_info=True)
        raise Exception(f"Failed to take screenshot: {str(e)}")

async def _download_image_from_url(url: str, attachments_path: Path) -> tuple[Path, str]:
    """Download an image directly from a URL."""
    try:
        logger.info(f"Downloading image from: {url}")
        
        # Download the image
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Determine file extension from content type or URL
        content_type = response.headers.get('content-type', '')
        if 'jpeg' in content_type or 'jpg' in content_type:
            ext = '.jpg'
        elif 'png' in content_type:
            ext = '.png'
        elif 'gif' in content_type:
            ext = '.gif'
        elif 'webp' in content_type:
            ext = '.webp'
        else:
            # Try to get extension from URL
            parsed_url = urlparse(url)
            path_ext = os.path.splitext(parsed_url.path)[1]
            ext = path_ext if path_ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'] else '.jpg'
        
        # Generate safe filename
        parsed_url = urlparse(url)
        safe_name = re.sub(r'[^\w\-_.]', '_', parsed_url.path.split('/')[-1] or 'image')
        if not safe_name.endswith(ext):
            safe_name = safe_name.split('.')[0]  # Remove existing extension if any
        filename = f"{safe_name}_{int(asyncio.get_event_loop().time())}{ext}"
        image_path = attachments_path / filename
        
        # Save the image
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verify it's a valid image and resize if too large
        try:
            with Image.open(image_path) as img:
                # Resize if image is too large (>2MB or >2000px in any dimension)
                max_size = (2000, 2000)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    img.save(image_path, optimize=True, quality=85)
                    logger.info(f"Resized large image: {image_path}")
        except Exception as img_error:
            logger.warning(f"Could not process image as PIL Image: {img_error}")
            # Keep the original file if PIL processing fails
        
        logger.info(f"Image downloaded successfully: {image_path}")
        return image_path, filename
        
    except Exception as e:
        logger.error(f"Error downloading image: {str(e)}", exc_info=True)
        raise Exception(f"Failed to download image: {str(e)}")