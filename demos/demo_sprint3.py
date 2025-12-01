"""
Demo script for Sprint 3 - Championship creation and modification.

This script demonstrates:
- Creating a new championship from scratch
- Modifying championship settings
- Adding/removing opponents
- Saving and loading championships
- Duplicating championships
"""

from src.utils.config import get_config
from src.services.championship_service import ChampionshipService
from src.services.talent_service import TalentService
from src.models.championship import (
    Championship, CareerStats, SeasonSettings,
    Player, Opponent, VehicleEntry
)


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
    print_header("rFactor Championship Creator - Sprint 3 Demo")

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
    champ_service = ChampionshipService(rfactor_path, player_name)
    talent_service = TalentService(rfactor_path)

    # Create a new championship
    print_section("1. Creating a new championship")

    # Career stats
    career = CareerStats(
        experience=0,
        money=500,
    )

    # Season settings
    season = SeasonSettings(
        name="Demo Championship 2025",
        season_status=0,  # Not started
        gameopt_race_laps=10,
        gameopt_opponents=5,
        gameopt_ai_driverstrength=90,
        gameopt_damagemultiplier=75,
    )

    # Player
    player = Player(
        name=player_name,
        veh_file="GAMEDATA\\VEHICLES\\RHEZ\\2005RHEZ\\SRGP\\TEAM RED\\RD_01.VEH",
        rcd_file="",
    )

    # Get some real talents for opponents
    print("Getting talents for opponents...")
    talents = talent_service.list_all()
    opponent_names = talents[:5]  # First 5 talents

    opponents = []
    for i, talent_name in enumerate(opponent_names):
        talent = talent_service.get(talent_name)
        if talent:
            opponent = Opponent(
                opponent_id=i,
                name=talent.name,
                veh_file=f"GAMEDATA\\VEHICLES\\RHEZ\\2005RHEZ\\SRGP\\TEAM_{i}\\CAR_{i}.VEH",
                rcd_file="",  # rFactor will find it automatically
                original_grid_position=i,
                current_grid_position=i,
            )
            opponents.append(opponent)
            print(f"  Added opponent: {talent.name}")

    # Create championship object
    championship = Championship(
        career=career,
        season=season,
        player=player,
        opponents=opponents,
    )

    print(f"\nChampionship created:")
    print(f"  Name: {championship.season.name}")
    print(f"  Player: {championship.player.name}")
    print(f"  Opponents: {len(championship.opponents)}")
    print(f"  Race laps: {championship.season.gameopt_race_laps}")

    # Save the championship
    print_section("2. Saving the championship")

    try:
        champ_service.create(championship, "DemoChampionship")
        print("[OK] Championship saved as 'DemoChampionship.cch'")
    except FileExistsError:
        print("[INFO] Championship already exists, updating instead...")
        champ_service.update(championship, "DemoChampionship")
        print("[OK] Championship updated")

    # Verify by loading it back
    print_section("3. Loading the championship back")

    loaded = champ_service.get("DemoChampionship")
    if loaded:
        print("[OK] Championship loaded successfully")
        print(f"  Name: {loaded.season.name}")
        print(f"  Player: {loaded.player.name}")
        print(f"  Opponents: {len(loaded.opponents)}")
        print(f"  AI Strength: {loaded.season.gameopt_ai_driverstrength}")
    else:
        print("[ERROR] Failed to load championship")
        return

    # Modify the championship
    print_section("4. Modifying championship settings")

    # Change some settings
    loaded.season.gameopt_race_laps = 15
    loaded.season.gameopt_ai_driverstrength = 95
    loaded.season.name = "Demo Championship 2025 - Modified"

    print("Modified:")
    print(f"  Race laps: 10 -> 15")
    print(f"  AI Strength: 90 -> 95")
    print(f"  Name: Updated")

    # Save changes
    champ_service.update(loaded, "DemoChampionship")
    print("\n[OK] Changes saved")

    # Duplicate the championship
    print_section("5. Duplicating the championship")

    try:
        duplicated = champ_service.duplicate("DemoChampionship", "DemoChampionship_Copy")
        print("[OK] Championship duplicated as 'DemoChampionship_Copy.cch'")
        print(f"  Name: {duplicated.season.name}")
        print(f"  Status: {duplicated.season.season_status} (reset to 0)")
        print(f"  Player points: {duplicated.player.season_points} (reset to 0)")
    except FileExistsError:
        print("[INFO] Copy already exists")

    # List all championships
    print_section("6. Listing all championships")

    all_champs = champ_service.list_all_with_info()
    print(f"Total championships: {len(all_champs)}")
    for info in all_champs:
        status_str = ["Not Started", "In Progress", "Completed"][info.get('status', 0)]
        print(f"\n  {info['filename']}")
        print(f"    Name: {info['name']}")
        print(f"    Status: {status_str}")
        print(f"    Opponents: {info['opponents']}")

    # Clean up (optional - comment out to keep the demo championship)
    print_section("7. Cleanup")

    cleanup = input("Delete demo championships? (y/n): ").strip().lower()
    if cleanup == 'y':
        try:
            champ_service.delete("DemoChampionship")
            print("[OK] Deleted 'DemoChampionship.cch'")
        except FileNotFoundError:
            pass

        try:
            champ_service.delete("DemoChampionship_Copy")
            print("[OK] Deleted 'DemoChampionship_Copy.cch'")
        except FileNotFoundError:
            pass

        print("\nCleanup completed!")
    else:
        print("\nDemo championships kept.")

    print_header("Demo completed!")


if __name__ == "__main__":
    main()
