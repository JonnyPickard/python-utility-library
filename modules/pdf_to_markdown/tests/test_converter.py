"""
Unit tests for PDF to Markdown converter.
"""

import pytest
import tempfile
import os
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
        assert converter.model_name is None
        assert converter._models is None
        
        converter_with_model = PDFToMarkdownConverter(model_name="test_model")
        assert converter_with_model.model_name == "test_model"
    
    def test_get_supported_extensions(self):
        """Test supported file extensions."""
        extensions = self.converter.get_supported_extensions()
        assert extensions == ['.pdf']
    
    def test_convert_single_file_not_found(self):
        """Test conversion with non-existent file."""
        with pytest.raises(FileNotFoundError):
            self.converter.convert_single_file("non_existent.pdf")
    
    @patch('modules.pdf_to_markdown.converter.convert_single_pdf')
    @patch('modules.pdf_to_markdown.converter.load_all_models')
    def test_convert_single_file_success(self, mock_load_models, mock_convert):
        """Test successful single file conversion."""
        # Setup mocks
        mock_load_models.return_value = MagicMock()
        mock_convert.return_value = ("# Test Markdown", [], {})
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a dummy PDF file
            pdf_path = Path(temp_dir) / "test.pdf"
            pdf_path.write_text("dummy pdf content")
            
            # Convert
            output_path = self.converter.convert_single_file(str(pdf_path))
            
            # Verify
            assert Path(output_path).exists()
            assert Path(output_path).suffix == '.md'
            assert Path(output_path).read_text(encoding='utf-8') == "# Test Markdown"
            mock_convert.assert_called_once()
    
    @patch('modules.pdf_to_markdown.converter.convert_single_pdf')
    @patch('modules.pdf_to_markdown.converter.load_all_models')
    def test_convert_single_file_with_custom_output(self, mock_load_models, mock_convert):
        """Test conversion with custom output path."""
        # Setup mocks
        mock_load_models.return_value = MagicMock()
        mock_convert.return_value = ("# Custom Output", [], {})
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a dummy PDF file
            pdf_path = Path(temp_dir) / "test.pdf"
            pdf_path.write_text("dummy pdf content")
            
            # Custom output path
            output_path = Path(temp_dir) / "custom_output.md"
            
            # Convert
            result_path = self.converter.convert_single_file(str(pdf_path), str(output_path))
            
            # Verify
            assert result_path == str(output_path)
            assert output_path.exists()
            assert output_path.read_text(encoding='utf-8') == "# Custom Output"
    
    def test_convert_folder_not_found(self):
        """Test conversion with non-existent input folder."""
        with pytest.raises(FileNotFoundError):
            self.converter.convert_folder("non_existent_folder", "output_folder")
    
    @patch('modules.pdf_to_markdown.converter.convert_single_pdf')
    @patch('modules.pdf_to_markdown.converter.load_all_models')
    def test_convert_folder_no_pdfs(self, mock_load_models, mock_convert):
        """Test conversion with folder containing no PDFs."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_folder = Path(temp_dir) / "input"
            input_folder.mkdir()
            output_folder = Path(temp_dir) / "output"
            
            # Create a non-PDF file
            (input_folder / "test.txt").write_text("not a pdf")
            
            result = self.converter.convert_folder(str(input_folder), str(output_folder))
            
            assert result == []
            assert output_folder.exists()  # Should still create output folder
    
    @patch('modules.pdf_to_markdown.converter.convert_single_pdf')
    @patch('modules.pdf_to_markdown.converter.load_all_models')
    def test_convert_folder_success(self, mock_load_models, mock_convert):
        """Test successful folder conversion."""
        # Setup mocks
        mock_load_models.return_value = MagicMock()
        mock_convert.return_value = ("# Converted Content", [], {})
        
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
            result = self.converter.convert_folder(str(input_folder), str(output_folder))
            
            # Verify
            assert len(result) == 2
            assert (output_folder / "test1.md").exists()
            assert (output_folder / "test2.md").exists()
            assert mock_convert.call_count == 2
    
    @patch('modules.pdf_to_markdown.converter.convert_single_pdf')
    @patch('modules.pdf_to_markdown.converter.load_all_models')
    def test_convert_folder_skip_existing(self, mock_load_models, mock_convert):
        """Test folder conversion skips existing files when overwrite=False."""
        # Setup mocks
        mock_load_models.return_value = MagicMock()
        mock_convert.return_value = ("# New Content", [], {})
        
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
            result = self.converter.convert_folder(str(input_folder), str(output_folder))
            
            # Verify - should skip conversion
            assert result == []
            assert existing_output.read_text(encoding='utf-8') == "# Existing Content"
            mock_convert.assert_not_called()
    
    @patch('modules.pdf_to_markdown.converter.convert_single_pdf')
    @patch('modules.pdf_to_markdown.converter.load_all_models')
    def test_convert_folder_overwrite_existing(self, mock_load_models, mock_convert):
        """Test folder conversion overwrites existing files when overwrite=True."""
        # Setup mocks  
        mock_load_models.return_value = MagicMock()
        mock_convert.return_value = ("# New Content", [], {})
        
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
            result = self.converter.convert_folder(str(input_folder), str(output_folder), overwrite=True)
            
            # Verify - should overwrite
            assert len(result) == 1
            assert existing_output.read_text(encoding='utf-8') == "# New Content"
            mock_convert.assert_called_once()
    
    @patch('modules.pdf_to_markdown.converter.convert_single_pdf')
    @patch('modules.pdf_to_markdown.converter.load_all_models')  
    def test_model_loading_lazy(self, mock_load_models, mock_convert):
        """Test that models are loaded lazily."""
        mock_models = MagicMock()
        mock_load_models.return_value = mock_models
        mock_convert.return_value = ("# Test", [], {})
        
        converter = PDFToMarkdownConverter()
        assert converter._models is None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create dummy PDF
            pdf_path = Path(temp_dir) / "test.pdf"
            pdf_path.write_text("dummy")
            
            # First conversion should load models
            converter.convert_single_file(str(pdf_path))
            mock_load_models.assert_called_once()
            assert converter._models == mock_models
            
            # Second conversion should reuse models
            converter.convert_single_file(str(pdf_path))
            mock_load_models.assert_called_once()  # Still only called once