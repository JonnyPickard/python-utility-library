"""
PDF to Markdown converter using the Marker library.
"""

import os
from pathlib import Path
from typing import Optional
import logging

try:
    from marker.convert import convert_single_pdf
    from marker.models import load_all_models
except ImportError:
    raise ImportError("marker-pdf library is required. Install with: pip install marker-pdf")


class PDFToMarkdownConverter:
    """
    Converts PDF files to Markdown using the Marker library.
    
    Supports single file conversion and batch processing from input to output folders.
    """
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the converter.
        
        Args:
            model_name: Optional model name for Marker. If None, uses default.
        """
        self.model_name = model_name
        self._models = None
        self.logger = logging.getLogger(__name__)
    
    def _load_models(self):
        """Lazy load the Marker models."""
        if self._models is None:
            self.logger.info("Loading Marker models...")
            self._models = load_all_models()
            self.logger.info("Models loaded successfully")
        return self._models
    
    def convert_single_file(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        Convert a single PDF file to Markdown.
        
        Args:
            pdf_path: Path to the input PDF file
            output_path: Path for the output Markdown file. If None, uses same name with .md extension
            
        Returns:
            Path to the output Markdown file
            
        Raises:
            FileNotFoundError: If the input PDF file doesn't exist
            Exception: If conversion fails
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if output_path is None:
            output_path = pdf_path.with_suffix('.md')
        else:
            output_path = Path(output_path)
        
        self.logger.info(f"Converting {pdf_path} to {output_path}")
        
        try:
            models = self._load_models()
            full_text, images, out_meta = convert_single_pdf(str(pdf_path), models)
            
            # Write the markdown content to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            
            self.logger.info(f"Successfully converted to {output_path}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Failed to convert {pdf_path}: {str(e)}")
            raise
    
    def convert_folder(self, input_folder: str, output_folder: str, 
                      overwrite: bool = False) -> list[str]:
        """
        Convert all PDF files in a folder to Markdown.
        
        Args:
            input_folder: Path to folder containing PDF files
            output_folder: Path to folder for output Markdown files
            overwrite: Whether to overwrite existing Markdown files
            
        Returns:
            List of paths to created Markdown files
            
        Raises:
            FileNotFoundError: If input folder doesn't exist
        """
        input_folder = Path(input_folder)
        output_folder = Path(output_folder)
        
        if not input_folder.exists():
            raise FileNotFoundError(f"Input folder not found: {input_folder}")
        
        # Create output folder if it doesn't exist
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Find all PDF files
        pdf_files = list(input_folder.glob("*.pdf"))
        if not pdf_files:
            self.logger.warning(f"No PDF files found in {input_folder}")
            return []
        
        self.logger.info(f"Found {len(pdf_files)} PDF files to convert")
        
        converted_files = []
        for pdf_file in pdf_files:
            output_file = output_folder / f"{pdf_file.stem}.md"
            
            # Skip if file exists and overwrite is False
            if output_file.exists() and not overwrite:
                self.logger.info(f"Skipping {pdf_file.name} (output exists)")
                continue
            
            try:
                converted_path = self.convert_single_file(pdf_file, output_file)
                converted_files.append(converted_path)
            except Exception as e:
                self.logger.error(f"Failed to convert {pdf_file.name}: {str(e)}")
                # Continue with other files even if one fails
                continue
        
        self.logger.info(f"Successfully converted {len(converted_files)} files")
        return converted_files
    
    def get_supported_extensions(self) -> list[str]:
        """
        Get list of supported file extensions.
        
        Returns:
            List of supported extensions
        """
        return ['.pdf']