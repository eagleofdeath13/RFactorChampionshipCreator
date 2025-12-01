"""
Demo script for Sprint 1 - Talent management functionality.

This script demonstrates:
- Listing talents
- Getting talent details
- Creating a new talent
- Searching talents
"""

from src.services.talent_service import TalentService
from src.models.talent import Talent, TalentPersonalInfo, TalentStats


def main():
    # Initialize the service
    rfactor_path = "RFactorFiles"
    service = TalentService(rfactor_path)

    print("=" * 60)
    print("rFactor Championship Creator - Sprint 1 Demo")
    print("=" * 60)
    print()

    # List all talents (first 10)
    print("1. Listing all talents (first 10):")
    print("-" * 40)
    all_talents = service.list_all()
    print(f"Total talents: {len(all_talents)}")
    for name in all_talents[:10]:
        print(f"  - {name}")
    print()

    # Get details for Brandon Lang
    print("2. Getting details for 'Brandon Lang':")
    print("-" * 40)
    brandon = service.get("Brandon Lang")
    if brandon:
        print(f"Name: {brandon.name}")
        print(f"Nationality: {brandon.personal_info.nationality}")
        print(f"Date of Birth: {brandon.personal_info.date_of_birth}")
        print(f"Starts: {brandon.personal_info.starts}")
        print(f"Wins: {brandon.personal_info.wins}")
        print(f"Speed: {brandon.stats.speed:.2f}")
        print(f"Aggression: {brandon.stats.aggression:.2f}")
    print()

    # Create a new talent
    print("3. Creating a new talent 'Lewis Hamilton':")
    print("-" * 40)

    personal_info = TalentPersonalInfo(
        nationality="British",
        date_of_birth="07-01-1985",
        starts=300,
        poles=100,
        wins=95,
        drivers_championships=7,
    )

    stats = TalentStats(
        aggression=85.0,
        reputation=98.5,
        courtesy=80.0,
        composure=95.0,
        speed=98.5,
        crash=5.0,
        recovery=90.0,
        completed_laps=98.0,
        min_racing_skill=95.0,
    )

    lewis = Talent(
        name="Lewis Hamilton",
        personal_info=personal_info,
        stats=stats,
    )

    try:
        service.create(lewis)
        print(f"[OK] Talent '{lewis.name}' created successfully!")
        print(f"  Filename: {lewis.filename}")
    except FileExistsError:
        print(f"[ERROR] Talent '{lewis.name}' already exists")
    print()

    # Verify creation by reading it back
    print("4. Verifying creation:")
    print("-" * 40)
    lewis_retrieved = service.get("Lewis Hamilton")
    if lewis_retrieved:
        print(f"[OK] Successfully retrieved '{lewis_retrieved.name}'")
        print(f"  Speed: {lewis_retrieved.stats.speed:.2f}")
        print(f"  Championships: {lewis_retrieved.personal_info.drivers_championships}")
    else:
        print("[ERROR] Failed to retrieve talent")
    print()

    # Search for talents
    print("5. Searching for talents with 'Lewis' in the name:")
    print("-" * 40)
    search_results = service.search("Lewis")
    print(f"Found {len(search_results)} talent(s):")
    for talent in search_results:
        print(f"  - {talent.name} ({talent.personal_info.nationality})")
    print()

    # Get American talents
    print("6. Getting all American talents (first 5):")
    print("-" * 40)
    american_talents = service.get_by_nationality("American")
    print(f"Found {len(american_talents)} American talent(s)")
    for talent in american_talents[:5]:
        print(f"  - {talent.name} (Speed: {talent.stats.speed:.2f})")
    print()

    # Clean up (delete the created talent)
    print("7. Cleaning up (deleting created talent):")
    print("-" * 40)
    try:
        service.delete("Lewis Hamilton")
        print(f"[OK] Talent 'Lewis Hamilton' deleted successfully")
    except FileNotFoundError:
        print(f"[ERROR] Talent 'Lewis Hamilton' not found")
    print()

    print("=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
