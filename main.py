from organizer import organize


print("📂 Smart File Organizer PRO")
print("==========================")

folder = input("Enter folder name: ")

print("\nChoose Mode:")
print("1. Preview (No changes)")
print("2. Organize Files")

choice = input("Enter choice (1/2): ")


if choice == "1":

    print("\n🔍 Preview Mode ON\n")
    organize(folder, dry_run=True)

elif choice == "2":

    print("\n⚙️ Organizing Files...\n")
    organize(folder, dry_run=False)

    print("\n✅ Finished Successfully")

else:

    print("❌ Invalid choice")