"""
PDF to Markdown Conversion Module

Uses the Marker library to convert PDF documents to Markdown format.
Supports batch processing of PDFs from input folder to output folder.
"""

from .converter import PDFToMarkdownConverter

__all__ = ["PDFToMarkdownConverter"]
