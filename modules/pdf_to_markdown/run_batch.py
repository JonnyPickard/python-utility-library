"""
Script to run batch PDF to Markdown conversion.
This script is used by VSCode launch configuration.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Module imports after path setup
from modules.pdf_to_markdown import PDFToMarkdownConverter  # noqa: E402


def main():
    """Run batch folder conversion."""
    converter = PDFToMarkdownConverter()

    # Get module paths (we're already in the module directory)
    module_path = Path(__file__).parent
    inputs_path = module_path / "inputs"
    outputs_path = module_path / "outputs"

    print("=== PDF to Markdown Batch Conversion ===\n")

    # Check for PDF files
    pdf_files = list(inputs_path.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {inputs_path}")
        print("Please add PDF files to the inputs folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s):")
    for pdf_file in pdf_files:
        print(f"  - {pdf_file.name}")

    # Check for existing output files
    existing_outputs = []
    for pdf_file in pdf_files:
        output_file = outputs_path / f"{pdf_file.stem}.md"
        if output_file.exists():
            existing_outputs.append(output_file.name)

    if existing_outputs:
        print("\nExisting output files found:")
        for output_file_name in existing_outputs:
            print(f"  - {output_file_name}")

        try:
            overwrite = input("\nOverwrite existing files? (y/n): ").lower().strip()
            if overwrite not in ["y", "yes"]:
                print("Skipping files that already exist...")
                overwrite_flag = False
            else:
                overwrite_flag = True
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    else:
        overwrite_flag = False

    print("\nStarting batch conversion...")
    print(f"Input folder: {inputs_path}")
    print(f"Output folder: {outputs_path}")
    print("Please wait...\n")

    try:
        converted_files = converter.convert_folder(
            str(inputs_path), str(outputs_path), overwrite=overwrite_flag
        )

        print("✅ Batch conversion completed!")
        print(f"Successfully converted {len(converted_files)} file(s):")

        for converted_file in converted_files:
            filename = Path(converted_file).name
            print(f"  - {filename}")

        if len(converted_files) < len(pdf_files):
            skipped = len(pdf_files) - len(converted_files)
            print(f"\nSkipped {skipped} file(s) (already existed or failed)")

    except Exception as e:
        print(f"❌ Batch conversion failed: {str(e)}")
        return

    print("\n" + "=" * 50)
    print("Batch conversion complete!")


if __name__ == "__main__":
    main()
