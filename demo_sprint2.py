"""
Demo script for Sprint 2 - Championship management functionality.

This script demonstrates:
- Listing championships
- Loading championship details
- Accessing championship data (players, opponents, settings)
"""

from src.utils.config import get_config
from src.services.championship_service import ChampionshipService


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
    print_header("rFactor Championship Creator - Sprint 2 Demo")

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

    # Initialize championship service
    service = ChampionshipService(rfactor_path, player_name)

    # List all championships
    print_section("1. Listing all championships")
    championships = service.list_all()
    print(f"Found {len(championships)} championship(s):")
    for champ in championships:
        print(f"  - {champ}")

    if not championships:
        print("\nNo championships found.")
        print("Create a championship in rFactor first, then run this demo again.")
        return

    # Get detailed info for all championships
    print_section("2. Championship details")
    champ_infos = service.list_all_with_info()
    for info in champ_infos:
        status_str = ["Not Started", "In Progress", "Completed"][info.get('status', 0)]
        print(f"\nChampionship: {info['name']}")
        print(f"  File: {info['filename']}")
        print(f"  Status: {status_str}")
        print(f"  Player: {info['player']}")
        print(f"  Opponents: {info['opponents']}")
        print(f"  Current Race: {info['current_race']}")
        print(f"  Player Points: {info['player_points']}")
        print(f"  Player Position: {info['player_position']}")

    # Load first championship in detail
    if championships:
        print_section("3. Loading first championship in detail")
        champ_name = championships[0]
        championship = service.get(champ_name)

        if championship:
            print(f"Championship: {championship.season.name}")
            print(f"Status: {championship.season.season_status}")
            print()

            # Career stats
            print("Career Statistics:")
            print(f"  Total Races: {championship.career.total_races}")
            print(f"  Total Wins: {championship.career.total_wins}")
            print(f"  Total Poles: {championship.career.total_poles}")
            print(f"  Money: {championship.career.money}")
            print()

            # Season settings
            print("Season Settings:")
            print(f"  AI Strength: {championship.season.gameopt_ai_driverstrength}")
            print(f"  Race Laps: {championship.season.gameopt_race_laps}")
            print(f"  Number of Opponents: {championship.season.gameopt_opponents}")
            print(f"  Damage Multiplier: {championship.season.gameopt_damagemultiplier}%")
            print()

            # Player info
            if championship.player:
                print("Player:")
                print(f"  Name: {championship.player.name}")
                print(f"  Vehicle: {championship.player.veh_file}")
                print(f"  Points: {championship.player.season_points}")
                print(f"  Position: {championship.player.points_position}")
                print(f"  Poles: {championship.player.poles_taken}")
                print()

            # Opponents (first 5)
            print(f"Opponents (showing first 5 of {len(championship.opponents)}):")
            for i, opp in enumerate(championship.opponents[:5], 1):
                print(f"  {i}. {opp.name}")
                print(f"     Vehicle: {opp.veh_file}")
                print(f"     Points: {opp.season_points}")
                print(f"     Grid Position: {opp.current_grid_position}")
            print()

            # Vehicles
            print(f"Vehicles ({len(championship.vehicles)} owned):")
            for vehicle in championship.vehicles:
                print(f"  - ID {vehicle.vehicle_id}: {vehicle.file}")
                print(f"    Meters driven: {vehicle.meters_driven}")
            print()

            # Track stats
            if championship.track_stats:
                print(f"Track Statistics ({len(championship.track_stats)} track(s)):")
                for track_stat in championship.track_stats:
                    print(f"  - {track_stat.track_name}")
                    print(f"    File: {track_stat.track_file}")

    print_header("Demo completed!")


if __name__ == "__main__":
    main()
