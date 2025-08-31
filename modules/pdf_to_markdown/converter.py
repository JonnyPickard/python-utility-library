"""
PDF to Markdown converter using the Marker library.
"""

from pathlib import Path
from typing import Optional
import logging

try:
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered
except ImportError:
    raise ImportError(
        "marker-pdf library is required. Install with: pip install marker-pdf"
    )

class PDFToMarkdownConverter:
    """
    Converts PDF files to Markdown using the Marker library.

    Supports single file conversion and batch processing from input to output folders.
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the converter.

        Args:
            config: Optional configuration dict for Marker. If None, uses default.
        """
        self.config = config
        self._converter = None
        self.logger = logging.getLogger(__name__)

    def _get_converter(self):
        """Lazy load the PDF converter."""
        if self._converter is None:
            self.logger.info("Loading Marker PDF converter...")
            try:
                # Set up GPU acceleration if available
                import os
                try:
                    import torch
                    if torch.cuda.is_available():
                        os.environ["TORCH_DEVICE"] = "cuda"
                        device_name = torch.cuda.get_device_name()
                        vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                        self.logger.info(f"Using GPU acceleration: {device_name} ({vram:.1f}GB VRAM)")
                    else:
                        self.logger.info("CUDA not available, using CPU")
                except ImportError:
                    self.logger.info("PyTorch not available, using CPU")

                # Create model artifacts dict
                artifact_dict = create_model_dict()
                self._converter = PdfConverter(
                    artifact_dict=artifact_dict, config=self.config
                )
                self.logger.info("Converter loaded successfully")
            except Exception as e:
                self.logger.error(f"Failed to load converter: {str(e)}")
                raise
        return self._converter

    def convert_single_file(
        self, pdf_path: str, output_path: Optional[str] = None
    ) -> str:
        """
        Convert a single PDF file to Markdown.

        Args:
            pdf_path: Path to the input PDF file
            output_path: Path for the output Markdown file.
                If None, uses same name with .md extension

        Returns:
            Path to the output Markdown file

        Raises:
            FileNotFoundError: If the input PDF file doesn't exist
            Exception: If conversion fails
        """
        pdf_path_obj = Path(pdf_path)
        if not pdf_path_obj.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path_obj}")

        if output_path is None:
            output_path_obj = pdf_path_obj.with_suffix(".md")
        else:
            output_path_obj = Path(output_path)

        self.logger.info(f"Converting {pdf_path_obj} to {output_path_obj}")

        try:
            converter = self._get_converter()
            # Convert PDF to document
            rendered = converter(str(pdf_path_obj))
            # Extract markdown text from rendered output
            markdown_text, _, _ = text_from_rendered(rendered)

            # Write the markdown content to file
            output_path_obj.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path_obj, "w", encoding="utf-8") as f:
                f.write(markdown_text)

            self.logger.info(f"Successfully converted to {output_path_obj}")
            return str(output_path_obj)

        except Exception as e:
            self.logger.error(f"Failed to convert {pdf_path_obj}: {str(e)}")
            raise

    def convert_folder(
        self, input_folder: str, output_folder: str, overwrite: bool = False
    ) -> list[str]:
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
        input_folder_obj = Path(input_folder)
        output_folder_obj = Path(output_folder)

        if not input_folder_obj.exists():
            raise FileNotFoundError(f"Input folder not found: {input_folder_obj}")

        # Create output folder if it doesn't exist
        output_folder_obj.mkdir(parents=True, exist_ok=True)

        # Find all PDF files
        pdf_files = list(input_folder_obj.glob("*.pdf"))
        if not pdf_files:
            self.logger.warning(f"No PDF files found in {input_folder_obj}")
            return []

        self.logger.info(f"Found {len(pdf_files)} PDF files to convert")

        converted_files = []
        for pdf_file in pdf_files:
            output_file = output_folder_obj / f"{pdf_file.stem}.md"

            # Skip if file exists and overwrite is False
            if output_file.exists() and not overwrite:
                self.logger.info(f"Skipping {pdf_file.name} (output exists)")
                continue

            try:
                converted_path = self.convert_single_file(str(pdf_file), str(output_file))
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
        return [".pdf"]
