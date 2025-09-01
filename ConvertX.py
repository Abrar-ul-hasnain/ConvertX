import os
import json
from datetime import datetime
from tqdm import tqdm
from rich.console import Console

console = Console()

def convert_files(input_folder, old_ext, new_ext, output_folder, delete_originals=False):
    os.makedirs(output_folder, exist_ok=True)

    # Collect matching files
    matching_files = [
        f for f in os.listdir(input_folder) if f.lower().endswith(old_ext.lower())
    ]

    if not matching_files:
        console.print(f"[red]No files with extension {old_ext} found in {input_folder}.[/red]")
        return

    # Show preview
    console.print("\n[bold cyan]Matching files:[/bold cyan]")
    for f in matching_files:
        console.print(" -", f)
    proceed = input(f"\nProceed with converting {len(matching_files)} files? (y/n): ").strip().lower()
    if proceed != "y":
        console.print("[yellow]Conversion cancelled.[/yellow]")
        return

    # Log files
    log_file = os.path.join(output_folder, "conversion_log.txt")
    error_log_file = os.path.join(output_folder, "error_log.txt")

    with open(log_file, "a", encoding="utf-8") as log, open(error_log_file, "a", encoding="utf-8") as err_log:
        log.write(f"\n--- Conversion run {datetime.now()} ---\n")
        err_log.write(f"\n--- Conversion run {datetime.now()} ---\n")

        # Progress bar
        for filename in tqdm(matching_files, desc="Converting", unit="file"):
            old_file_path = os.path.join(input_folder, filename)
            new_file_name = filename[: -len(old_ext)] + new_ext
            new_file_path = os.path.join(output_folder, new_file_name)

            try:
                # Duplicate check
                if os.path.exists(new_file_path):
                    console.print(f"[yellow]SKIPPED: {new_file_name} already exists.[/yellow]")
                    log.write(f"SKIPPED: {filename} -> {new_file_name} (already exists)\n")
                    continue

                if old_ext == ".ipynb" and new_ext == ".py":
                    # Special handling: extract code cells
                    with open(old_file_path, "r", encoding="utf-8") as f:
                        notebook = json.load(f)

                    code_lines = []
                    for cell in notebook.get("cells", []):
                        if cell.get("cell_type") == "code":
                            code_lines.extend(cell.get("source", []))
                            code_lines.append("\n")

                    with open(new_file_path, "w", encoding="utf-8") as f:
                        f.writelines(code_lines)

                else:
                    # General case: copy file content
                    with open(old_file_path, "r", encoding="utf-8", errors="ignore") as src:
                        data = src.read()

                    with open(new_file_path, "w", encoding="utf-8", errors="ignore") as dst:
                        dst.write(data)

                if delete_originals:
                    os.remove(old_file_path)

                log.write(f"SUCCESS: {filename} -> {new_file_name}\n")

            except Exception as e:
                console.print(f"[red]ERROR: {filename} - {e}[/red]")
                err_log.write(f"ERROR: {filename} - {e}\n")
                continue

    console.print(f"\n[green]Conversion complete.[/green] Log saved at: {log_file}")
    console.print(f"[yellow]Errors (if any) saved at: {error_log_file}[/yellow]")


def main():
    console.print("[bold green]=== File Extension Converter ===[/bold green]")
    input_folder = input("Enter the folder containing files to convert: ").strip()
    old_ext = input("Enter the current file extension (include dot, e.g. .ipynb): ").strip()
    new_ext = input("Enter the new file extension (include dot, e.g. .py): ").strip()
    output_folder = input("Enter the folder where converted files should be saved: ").strip()

    delete_choice = input("Delete originals after conversion? (y/n): ").strip().lower()
    delete_originals = (delete_choice == "y")

    convert_files(input_folder, old_ext, new_ext, output_folder, delete_originals)


if __name__ == "__main__":
    main()
