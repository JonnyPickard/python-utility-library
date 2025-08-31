"""
Unit tests for PDF to Markdown converter.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from modules.pdf_to_markdown.converter import PDFToMarkdownConverter


class TestPDFToMarkdownConverter:
    """Test cases for PDFToMarkdownConverter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = PDFToMarkdownConverter()

    def test_initialization(self):
        """Test converter initialization."""
        converter = PDFToMarkdownConverter()
        assert converter.config is None
        assert converter._converter is None

        converter_with_config = PDFToMarkdownConverter(config={"test": "config"})
        assert converter_with_config.config == {"test": "config"}

    def test_get_supported_extensions(self):
        """Test supported file extensions."""
        extensions = self.converter.get_supported_extensions()
        assert extensions == [".pdf"]

    def test_convert_single_file_not_found(self):
        """Test conversion with non-existent file."""
        with pytest.raises(FileNotFoundError):
            self.converter.convert_single_file("non_existent.pdf")

    @patch("modules.pdf_to_markdown.converter.text_from_rendered")
    @patch("modules.pdf_to_markdown.converter.PdfConverter")
    @patch("modules.pdf_to_markdown.converter.create_model_dict")
    def test_convert_single_file_success(
        self, mock_create_model_dict, mock_pdf_converter, mock_text_from_rendered
    ):
        """Test successful single file conversion."""
        # Setup mocks
        mock_create_model_dict.return_value = {"models": "dict"}
        mock_converter_instance = MagicMock()
        mock_rendered = MagicMock()
        mock_converter_instance.return_value = mock_rendered
        mock_pdf_converter.return_value = mock_converter_instance
        mock_text_from_rendered.return_value = ("# Test Markdown", None, None)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a dummy PDF file
            pdf_path = Path(temp_dir) / "test.pdf"
            pdf_path.write_text("dummy pdf content")

            # Convert
            output_path = self.converter.convert_single_file(str(pdf_path))

            # Verify
            assert Path(output_path).exists()
            assert Path(output_path).suffix == ".md"
            assert Path(output_path).read_text(encoding="utf-8") == "# Test Markdown"
            mock_converter_instance.assert_called_once()
            mock_text_from_rendered.assert_called_once_with(mock_rendered)

    @patch("modules.pdf_to_markdown.converter.text_from_rendered")
    @patch("modules.pdf_to_markdown.converter.PdfConverter")
    @patch("modules.pdf_to_markdown.converter.create_model_dict")
    def test_convert_single_file_with_custom_output(
        self, mock_create_model_dict, mock_pdf_converter, mock_text_from_rendered
    ):
        """Test conversion with custom output path."""
        # Setup mocks
        mock_create_model_dict.return_value = {"models": "dict"}
        mock_converter_instance = MagicMock()
        mock_rendered = MagicMock()
        mock_converter_instance.return_value = mock_rendered
        mock_pdf_converter.return_value = mock_converter_instance
        mock_text_from_rendered.return_value = ("# Custom Output", None, None)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a dummy PDF file
            pdf_path = Path(temp_dir) / "test.pdf"
            pdf_path.write_text("dummy pdf content")

            # Custom output path
            output_path = Path(temp_dir) / "custom_output.md"

            # Convert
            result_path = self.converter.convert_single_file(
                str(pdf_path), str(output_path)
            )

            # Verify
            assert result_path == str(output_path)
            assert output_path.exists()
            assert output_path.read_text(encoding="utf-8") == "# Custom Output"

    def test_convert_folder_not_found(self):
        """Test conversion with non-existent input folder."""
        with pytest.raises(FileNotFoundError):
            self.converter.convert_folder("non_existent_folder", "output_folder")

    @patch("modules.pdf_to_markdown.converter.PdfConverter")
    @patch("modules.pdf_to_markdown.converter.create_model_dict")
    def test_convert_folder_no_pdfs(self, mock_create_model_dict, mock_pdf_converter):
        """Test conversion with folder containing no PDFs."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_folder = Path(temp_dir) / "input"
            input_folder.mkdir()
            output_folder = Path(temp_dir) / "output"

            # Create a non-PDF file
            (input_folder / "test.txt").write_text("not a pdf")

            result = self.converter.convert_folder(
                str(input_folder), str(output_folder)
            )

            assert result == []
            assert output_folder.exists()  # Should still create output folder

    @patch("modules.pdf_to_markdown.converter.text_from_rendered")
    @patch("modules.pdf_to_markdown.converter.PdfConverter")
    @patch("modules.pdf_to_markdown.converter.create_model_dict")
    def test_convert_folder_success(
        self, mock_create_model_dict, mock_pdf_converter, mock_text_from_rendered
    ):
        """Test successful folder conversion."""
        # Setup mocks
        mock_create_model_dict.return_value = {"models": "dict"}
        mock_converter_instance = MagicMock()
        mock_rendered = MagicMock()
        mock_converter_instance.return_value = mock_rendered
        mock_pdf_converter.return_value = mock_converter_instance
        mock_text_from_rendered.return_value = ("# Converted Content", None, None)

        with tempfile.TemporaryDirectory() as temp_dir:
            input_folder = Path(temp_dir) / "input"
            input_folder.mkdir()
            output_folder = Path(temp_dir) / "output"

            # Create dummy PDF files
            pdf1 = input_folder / "test1.pdf"
            pdf2 = input_folder / "test2.pdf"
            pdf1.write_text("dummy pdf 1")
            pdf2.write_text("dummy pdf 2")

            # Convert
            result = self.converter.convert_folder(
                str(input_folder), str(output_folder)
            )

            # Verify
            assert len(result) == 2
            assert (output_folder / "test1.md").exists()
            assert (output_folder / "test2.md").exists()
            assert mock_converter_instance.call_count == 2

    @patch("modules.pdf_to_markdown.converter.PdfConverter")
    @patch("modules.pdf_to_markdown.converter.create_model_dict")
    def test_convert_folder_skip_existing(
        self, mock_create_model_dict, mock_pdf_converter
    ):
        """Test folder conversion skips existing files when overwrite=False."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_folder = Path(temp_dir) / "input"
            input_folder.mkdir()
            output_folder = Path(temp_dir) / "output"
            output_folder.mkdir()

            # Create dummy PDF file
            pdf1 = input_folder / "test1.pdf"
            pdf1.write_text("dummy pdf")

            # Create existing output file
            existing_output = output_folder / "test1.md"
            existing_output.write_text("# Existing Content")

            # Convert with overwrite=False (default)
            result = self.converter.convert_folder(
                str(input_folder), str(output_folder)
            )

            # Verify - should skip conversion
            assert result == []
            assert existing_output.read_text(encoding="utf-8") == "# Existing Content"
            mock_pdf_converter.assert_not_called()

    @patch("modules.pdf_to_markdown.converter.text_from_rendered")
    @patch("modules.pdf_to_markdown.converter.PdfConverter")
    @patch("modules.pdf_to_markdown.converter.create_model_dict")
    def test_convert_folder_overwrite_existing(
        self, mock_create_model_dict, mock_pdf_converter, mock_text_from_rendered
    ):
        """Test folder conversion overwrites existing files when overwrite=True."""
        # Setup mocks
        mock_create_model_dict.return_value = {"models": "dict"}
        mock_converter_instance = MagicMock()
        mock_rendered = MagicMock()
        mock_converter_instance.return_value = mock_rendered
        mock_pdf_converter.return_value = mock_converter_instance
        mock_text_from_rendered.return_value = ("# New Content", None, None)

        with tempfile.TemporaryDirectory() as temp_dir:
            input_folder = Path(temp_dir) / "input"
            input_folder.mkdir()
            output_folder = Path(temp_dir) / "output"
            output_folder.mkdir()

            # Create dummy PDF file
            pdf1 = input_folder / "test1.pdf"
            pdf1.write_text("dummy pdf")

            # Create existing output file
            existing_output = output_folder / "test1.md"
            existing_output.write_text("# Existing Content")

            # Convert with overwrite=True
            result = self.converter.convert_folder(
                str(input_folder), str(output_folder), overwrite=True
            )

            # Verify - should overwrite
            assert len(result) == 1
            assert existing_output.read_text(encoding="utf-8") == "# New Content"
            mock_converter_instance.assert_called_once()

    @patch("modules.pdf_to_markdown.converter.text_from_rendered")
    @patch("modules.pdf_to_markdown.converter.PdfConverter")
    @patch("modules.pdf_to_markdown.converter.create_model_dict")
    def test_converter_loading_lazy(
        self, mock_create_model_dict, mock_pdf_converter, mock_text_from_rendered
    ):
        """Test that converter is loaded lazily."""
        mock_create_model_dict.return_value = {"models": "dict"}
        mock_converter_instance = MagicMock()
        mock_pdf_converter.return_value = mock_converter_instance
        mock_rendered = MagicMock()
        mock_converter_instance.return_value = mock_rendered
        mock_text_from_rendered.return_value = ("# Test", None, None)

        converter = PDFToMarkdownConverter()
        assert converter._converter is None

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create dummy PDF
            pdf_path = Path(temp_dir) / "test.pdf"
            pdf_path.write_text("dummy")

            # First conversion should load converter
            converter.convert_single_file(str(pdf_path))
            mock_create_model_dict.assert_called_once()
            assert converter._converter == mock_converter_instance

            # Second conversion should reuse converter
            converter.convert_single_file(str(pdf_path))
            mock_create_model_dict.assert_called_once()  # Still only called once
