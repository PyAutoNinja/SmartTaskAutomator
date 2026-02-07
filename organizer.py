import os
import shutil
from datetime import datetime


FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv"],
    "Music": [".mp3"],
    "Archives": [".zip", ".rar"],
    "Apps": [".apk"]
}


LOG_FILE = "log.txt"
BACKUP_FOLDER = "Backup"


def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def get_category(filename):

    name = filename.lower()

    for category, exts in FILE_TYPES.items():

        for ext in exts:
            if name.endswith(ext):
                return category

    return "Others"


def organize(folder, dry_run=False):

    if not os.path.exists(folder):
        print("❌ Folder not found!")
        return

    files = os.listdir(folder)

    backup = os.path.join(folder, BACKUP_FOLDER)

    if not os.path.exists(backup):
        os.mkdir(backup)

    count = 0

    log("\n===== New Run: " + str(datetime.now()) + " =====")

    for file in files:

        src = os.path.join(folder, file)

        if not os.path.isfile(src):
            continue

        category = get_category(file)

        dest_folder = os.path.join(folder, category)

        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)

        dest = os.path.join(dest_folder, file)

        backup_file = os.path.join(backup, file)

        if dry_run:

            print(f"🔍 Preview: {file} → {category}")
            continue

        # Backup
        shutil.copy2(src, backup_file)

        # Move
        shutil.move(src, dest)

        print(f"✅ Moved: {file} → {category}")

        log(f"{file} → {category}")

        count += 1

    print(f"\n🔥 Total files organized: {count}")
    log(f"Total: {count} files\n")