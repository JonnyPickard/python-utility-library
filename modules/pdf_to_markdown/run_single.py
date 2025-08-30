"""
Script to run single PDF to Markdown conversion.
This script is used by VSCode launch configuration.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.pdf_to_markdown import PDFToMarkdownConverter


def main():
    """Run single file conversion with user input."""
    converter = PDFToMarkdownConverter()
    
    # Get module paths (we're already in the module directory)
    module_path = Path(__file__).parent
    inputs_path = module_path / "inputs"
    outputs_path = module_path / "outputs"
    
    print("=== PDF to Markdown Single File Conversion ===\n")
    
    # List available PDFs
    pdf_files = list(inputs_path.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {inputs_path}")
        print("Please add PDF files to the inputs folder.")
        return
    
    print("Available PDF files:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf_file.name}")
    
    # Get user selection
    try:
        while True:
            choice = input(f"\nSelect file to convert (1-{len(pdf_files)}): ")
            if choice.isdigit() and 1 <= int(choice) <= len(pdf_files):
                selected_pdf = pdf_files[int(choice) - 1]
                break
            print("Invalid selection. Please try again.")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return
    
    # Convert the file
    output_file = outputs_path / f"{selected_pdf.stem}.md"
    
    print(f"\nConverting: {selected_pdf.name}")
    print(f"Output: {output_file.name}")
    print("Please wait...\n")
    
    try:
        result_path = converter.convert_single_file(str(selected_pdf), str(output_file))
        print(f"✅ Conversion successful!")
        print(f"Output saved to: {result_path}")
    except Exception as e:
        print(f"❌ Conversion failed: {str(e)}")
        return
    
    print("\n" + "="*50)
    print("Conversion complete!")


if __name__ == "__main__":
    main()