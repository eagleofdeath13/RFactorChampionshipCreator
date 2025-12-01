"""
Demo script for Sprint 4 - CSV Import/Export functionality.

This script demonstrates:
- Generating a CSV template
- Importing talents from CSV
- Handling import errors
- Exporting talents to CSV
- Validating CSV without importing
"""

from pathlib import Path
from src.utils.config import get_config
from src.services.talent_service import TalentService
from src.services.import_service import ImportService


def print_header(text: str):
    """Print a formatted header."""
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)
    print()


def print_section(text: str):
    """Print a formatted section header."""
    print()
    print("-" * 40)
    print(text)
    print("-" * 40)


def main():
    print_header("rFactor Championship Creator - Sprint 4 Demo")

    # Load configuration
    config = get_config()

    if not config.is_configured():
        print("[ERROR] Application not configured!")
        print("Please run 'python setup_config.py' first.")
        return

    # Get configured paths
    rfactor_path = config.get_rfactor_path()
    player_name = config.get_current_player()

    print(f"rFactor path: {rfactor_path}")
    print(f"Player: {player_name}")

    # Initialize services
    talent_service = TalentService(rfactor_path)
    import_service = ImportService(talent_service)

    # Count existing talents
    existing_count = len(talent_service.list_all())
    print(f"Existing talents: {existing_count}")

    # 1. Generate CSV template
    print_section("1. Generating CSV template")

    template_file = "talents_template.csv"
    ImportService.generate_csv_template(template_file)
    print(f"[OK] Template generated: {template_file}")
    print("\nThe template includes 2 example drivers with all available fields:")
    print("  - name (required)")
    print("  - nationality (required)")
    print("  - date_of_birth (required)")
    print("  - starts, poles, wins, drivers_championships")
    print("  - aggression, reputation, courtesy, composure, speed")
    print("  - crash, recovery, completed_laps, min_racing_skill")

    # 2. Validate CSV without importing
    print_section("2. Validating CSV (dry run)")

    result = import_service.import_from_csv(template_file, validate_only=True)
    print(f"Validation result:")
    print(f"  Valid rows: {result.success_count}")
    print(f"  Invalid rows: {result.error_count}")

    if result.error_count > 0:
        print("\nErrors found:")
        for row_num, name, error in result.errors:
            print(f"  Row {row_num} ({name}): {error}")

    # 3. Import from CSV
    print_section("3. Importing talents from CSV")

    print("Importing with skip_existing=True...")
    result = import_service.import_from_csv(template_file, skip_existing=True)

    print(f"\nImport result:")
    print(f"  Successfully imported: {result.success_count}")
    print(f"  Errors/Skipped: {result.error_count}")
    print(f"  Total processed: {result.total}")

    if result.error_count > 0:
        print("\nErrors/Warnings:")
        for row_num, name, error in result.errors:
            print(f"  Row {row_num} ({name}): {error}")

    # Show created talents
    if result.success_count > 0:
        print("\nNewly created talents:")
        for i in range(1, 3):  # We know template has 2 examples
            talent_name = f"Example Driver {i}"
            talent = talent_service.get(talent_name)
            if talent:
                print(f"  - {talent.name}")
                print(f"    Nationality: {talent.personal_info.nationality}")
                print(f"    Speed: {talent.stats.speed:.1f}")
                print(f"    Aggression: {talent.stats.aggression:.1f}")

    # 4. Create a custom CSV with intentional errors
    print_section("4. Importing CSV with errors")

    # Create a test CSV with some errors
    test_csv = "talents_test.csv"
    with open(test_csv, 'w', encoding='utf-8', newline='') as f:
        f.write("name,nationality,date_of_birth,speed\n")
        f.write("Good Driver 1,France,15-03-1990,85.0\n")
        f.write(",Italy,20-05-1988,80.0\n")  # Missing name (error)
        f.write("Good Driver 2,Germany,10-10-1992,75.0\n")
        f.write("Bad Speed,Spain,05-12-1985,999.0\n")  # Invalid speed (error)
        f.write("Good Driver 3,UK,22-08-1991,78.0\n")

    print(f"Created test CSV with intentional errors: {test_csv}")
    print("  - Row 2: Missing name")
    print("  - Row 4: Invalid speed (999.0 > 100.0)")

    result = import_service.import_from_csv(test_csv, skip_existing=True)

    print(f"\nImport result:")
    print(f"  Successfully imported: {result.success_count}")
    print(f"  Errors: {result.error_count}")

    if result.error_count > 0:
        print("\nError details:")
        for row_num, name, error in result.errors:
            print(f"  Row {row_num} ({name}): {error}")

    # 5. Export talents to CSV
    print_section("5. Exporting talents to CSV")

    # Export all talents
    export_all_file = "talents_export_all.csv"
    count = import_service.export_to_csv(export_all_file)
    print(f"[OK] Exported {count} talents to {export_all_file}")

    # Export specific talents
    export_specific_file = "talents_export_specific.csv"
    specific_talents = ['Example Driver 1', 'Good Driver 1', 'Good Driver 2']

    # Check which talents exist
    existing_talents = [t for t in specific_talents if talent_service.get(t)]

    if existing_talents:
        count = import_service.export_to_csv(export_specific_file, talent_names=existing_talents)
        print(f"[OK] Exported {count} specific talents to {export_specific_file}")
        print(f"Exported: {', '.join(existing_talents)}")

    # 6. Show summary
    print_section("6. Summary")

    new_count = len(talent_service.list_all())
    print(f"Total talents before demo: {existing_count}")
    print(f"Total talents after demo: {new_count}")
    print(f"Talents added: {new_count - existing_count}")

    print("\nGenerated files:")
    for filename in [template_file, test_csv, export_all_file, export_specific_file]:
        if Path(filename).exists():
            size = Path(filename).stat().st_size
            print(f"  - {filename} ({size} bytes)")

    # Cleanup option
    print_section("7. Cleanup")

    cleanup = input("Delete demo files and talents? (y/n): ").strip().lower()
    if cleanup == 'y':
        # Delete CSV files
        for filename in [template_file, test_csv, export_all_file, export_specific_file]:
            path = Path(filename)
            if path.exists():
                path.unlink()
                print(f"[OK] Deleted {filename}")

        # Delete created talents
        demo_talents = [
            'Example Driver 1',
            'Example Driver 2',
            'Good Driver 1',
            'Good Driver 2',
            'Good Driver 3',
        ]

        deleted_count = 0
        for name in demo_talents:
            if talent_service.exists(name):
                try:
                    talent_service.delete(name)
                    deleted_count += 1
                except Exception:
                    pass

        print(f"[OK] Deleted {deleted_count} demo talents")
        print("\nCleanup completed!")
    else:
        print("\nDemo files and talents kept.")

    print_header("Demo completed!")
    print("\nKey features demonstrated:")
    print("  - CSV template generation")
    print("  - Validation before import")
    print("  - Batch import with error handling")
    print("  - Export all or specific talents")
    print("  - Error reporting and recovery")


if __name__ == "__main__":
    main()
