import os
import shutil
from pathlib import Path

def organize_directory(target_dir="."):
    print("=" * 60)
    print("      AUTOMATED FILE ORGANIZER & CLEANUP UTILITY      ")
    print("=" * 60)
    
    path = Path(target_dir).resolve()
    print(f"\n📂 Scanning directory: {path}\n")
    
    if not path.exists():
        print(f"❌ Error: The directory '{path}' does not exist.")
        return

    # Extension mapping dictionary as specified in requirements
    extension_mapping = {
        # Documents
        '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
        '.txt': 'Documents', '.xlsx': 'Documents', '.xls': 'Documents',
        '.csv': 'Documents', '.pptx': 'Documents', '.ppt': 'Documents',
        
        # Images
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
        '.gif': 'Images', '.svg': 'Images', '.webp': 'Images',
        
        # Videos & Audio
        '.mp4': 'Videos', '.mkv': 'Videos', '.avi': 'Videos',
        '.mov': 'Videos', '.mp3': 'Videos', '.wav': 'Videos',
        
        # Archives
        '.zip': 'Archives', '.rar': 'Archives', '.tar': 'Archives',
        '.gz': 'Archives', '.7z': 'Archives',
        
        # Code & Scripts
        '.py': 'Code', '.js': 'Code', '.html': 'Code',
        '.css': 'Code', '.cpp': 'Code', '.java': 'Code', '.json': 'Code'
    }
    
    moved_files_count = 0
    skipped_files_count = 0
    
    # Use os.scandir for efficient iteration
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                # Skip directories and hidden files (starting with '.')
                if entry.is_dir() or entry.name.startswith('.'):
                    continue
                
                file_path = Path(entry.path)
                file_ext = file_path.suffix.lower()
                
                # Determine target category folder
                category = extension_mapping.get(file_ext, 'Others')
                target_folder = path / category
                
                try:
                    # Create category subfolder if it doesn't exist
                    target_folder.mkdir(exist_ok=True)
                    
                    destination_path = target_folder / file_path.name
                    
                    # Handle naming collisions safely
                    if destination_path.exists():
                        base_name = file_path.stem
                        counter = 1
                        while destination_path.exists():
                            new_filename = f"{base_name}_{counter}{file_ext}"
                            destination_path = target_folder / new_filename
                            counter += 1
                    
                    # Move the file using shutil.move
                    shutil.move(str(file_path), str(destination_path))
                    print(f"✅ Moved: {file_path.name} ➡️ /{category}/")
                    moved_files_count += 1
                    
                except PermissionError:
                    print(f"⚠️ Permission Denied: Could not move '{file_path.name}'. File might be in use.")
                    skipped_files_count += 1
                except Exception as e:
                    print(f"❌ Error moving '{file_path.name}': {e}")
                    skipped_files_count += 1
                    
    except Exception as e:
        print(f"❌ Error scanning directory: {e}")
        return

    # Execution Summary
    print("\n" + "=" * 60)
    print("                  EXECUTION SUMMARY                   ")
    print("-" * 60)
    print(f"📁 Target Directory   : {path}")
    print(f"✨ Total Files Relocated: {moved_files_count}")
    print(f"⚠️ Files Skipped/Errors : {skipped_files_count}")
    print("=" * 60)

if __name__ == "__main__":
    # You can specify a path here, e.g., "C:/Users/ASUS/Downloads" or leave "." for current directory
    target = input("Enter directory path to organize (Press Enter for current folder): ").strip()
    if not target:
        target = "."
    organize_directory(target)