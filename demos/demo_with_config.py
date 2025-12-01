"""
Demo script using configuration system.

This script demonstrates using the Config system to automatically
detect and use the configured rFactor installation.
"""

from src.utils.config import get_config
from src.services.talent_service import TalentService
from src.models.talent import Talent, TalentPersonalInfo, TalentStats


def main():
    print("=" * 60)
    print("rFactor Championship Creator - Config Demo")
    print("=" * 60)
    print()

    # Load configuration
    config = get_config()

    if not config.is_configured():
        print("[ERROR] Application not configured!")
        print("Please run 'python setup_config.py' first.")
        return

    # Show config summary
    print("Configuration:")
    print("-" * 40)
    summary = config.get_config_summary()
    print(f"rFactor path: {summary['rfactor_path']}")
    print(f"Current player: {summary['current_player']}")
    print(f"Talents available: {summary.get('talent_count', 0)}")
    print()

    # Initialize service using configured path
    rfactor_path = config.get_rfactor_path()
    service = TalentService(rfactor_path)

    # List first 5 talents
    print("First 5 talents:")
    print("-" * 40)
    talents = service.list_all()
    for name in talents[:5]:
        print(f"  - {name}")
    print()

    # Get details for a specific talent
    print("Details for 'Brandon Lang':")
    print("-" * 40)
    brandon = service.get("Brandon Lang")
    if brandon:
        print(f"Name: {brandon.name}")
        print(f"Nationality: {brandon.personal_info.nationality}")
        print(f"Speed: {brandon.stats.speed:.2f}")
    else:
        print("Talent not found")
    print()

    # Show player profile location
    current_player = config.get_current_player()
    if current_player:
        print(f"Current player profile: {current_player}")
        print(f"Championships will be saved to: UserData/{current_player}/")
        print()

    print("=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
