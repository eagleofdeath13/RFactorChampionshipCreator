"""
Utility for generating random talent statistics.

Provides functions to generate realistic and coherent random values
for talent creation and CSV import.
"""

import random
from typing import Dict, Any, Optional

# Import config for bounds (delayed import to avoid circular dependency)
def _get_bounds() -> Dict[str, Any]:
    """Get randomizer bounds from config."""
    try:
        from .config import get_config
        config = get_config()
        return config.get_randomizer_bounds()
    except Exception:
        # Fallback to default bounds if config unavailable
        return {
            "overall_skill": {"min": 40, "max": 95},
            "speed_variance": 8,
            "composure_variance": 10,
            "crash_base": 50,
            "crash_variance": 15,
            "completed_laps_base": 95,
            "completed_laps_variance": 8,
            "completed_laps_min": 75,
            "completed_laps_max": 99,
            "recovery_variance": 12,
            "aggression": {"min": 30, "max": 90},
            "courtesy": {"min": 40, "max": 85},
            "min_racing_skill_variance": 5,
            "reputation_variance": 10,
        }


class TalentRandomizer:
    """Generator for random talent statistics."""

    # Listes de nationalités possibles
    NATIONALITIES = [
        "American", "British", "French", "German", "Italian", "Spanish",
        "Brazilian", "Japanese", "Australian", "Canadian", "Belgian",
        "Dutch", "Swedish", "Finnish", "Austrian", "Swiss", "Portuguese",
        "Mexican", "Argentinian", "Colombian", "Danish", "Norwegian",
    ]

    @staticmethod
    def random_racing_stats() -> Dict[str, float]:
        """
        Generate ONLY random racing statistics (for UI randomizer).

        Does NOT generate personal info (name, nationality, date, career stats).
        Only generates the 9 racing performance stats.

        Returns:
            Dictionary with 9 racing stats
        """
        # Get bounds from config
        bounds = _get_bounds()

        # Génération du niveau général (depuis config)
        overall_min = bounds["overall_skill"]["min"]
        overall_max = bounds["overall_skill"]["max"]
        overall_skill = random.uniform(overall_min, overall_max)

        # Stats principales (corrélées avec overall_skill)
        speed = TalentRandomizer._generate_correlated(
            overall_skill, variance=bounds["speed_variance"]
        )
        composure = TalentRandomizer._generate_correlated(
            overall_skill, variance=bounds["composure_variance"]
        )

        # Crash inversement proportionnel (meilleur pilote = moins de crash)
        crash = TalentRandomizer._generate_inverse(
            overall_skill,
            base=bounds["crash_base"],
            variance=bounds["crash_variance"]
        )

        # CompletedLaps élevé si crash bas
        completed_laps = TalentRandomizer._generate_inverse(
            crash,
            base=bounds["completed_laps_base"],
            variance=bounds["completed_laps_variance"]
        )
        completed_laps = max(
            float(bounds["completed_laps_min"]),
            min(float(bounds["completed_laps_max"]), completed_laps)
        )

        # Recovery aide à gérer les erreurs
        recovery = TalentRandomizer._generate_correlated(
            overall_skill, variance=bounds["recovery_variance"]
        )

        # Aggression et Courtesy sont plus indépendantes (depuis config)
        aggression = random.uniform(
            bounds["aggression"]["min"], bounds["aggression"]["max"]
        )
        courtesy = random.uniform(
            bounds["courtesy"]["min"], bounds["courtesy"]["max"]
        )

        # MinRacingSkill proche de l'overall
        min_racing_skill = TalentRandomizer._generate_correlated(
            overall_skill, variance=bounds["min_racing_skill_variance"]
        )

        # Reputation basée sur le niveau (sans victoires/championnats)
        reputation = TalentRandomizer._generate_correlated(
            overall_skill, variance=bounds["reputation_variance"]
        )

        return {
            "speed": round(speed, 1),
            "crash": round(crash, 1),
            "aggression": round(aggression, 1),
            "reputation": round(reputation, 1),
            "courtesy": round(courtesy, 1),
            "composure": round(composure, 1),
            "recovery": round(recovery, 1),
            "completed_laps": round(completed_laps, 1),
            "min_racing_skill": round(min_racing_skill, 1),
        }

    @staticmethod
    def random_stats() -> Dict[str, Any]:
        """
        Generate random talent statistics with coherent relationships.

        Returns:
            Dictionary with random personal_info and stats

        Rules:
        - Speed et composure sont les stats principales (corrélées)
        - Reputation dépend des victoires et championnats
        - Crash est inversement proportionnel à la compétence
        - CompletedLaps est élevé si crash est bas
        - Recovery aide à compenser les erreurs
        """
        # Génération du niveau général (40-95)
        # Cela définit le "tier" du pilote
        overall_skill = random.uniform(40, 95)

        # Stats principales (corrélées avec overall_skill)
        speed = TalentRandomizer._generate_correlated(overall_skill, variance=8)
        composure = TalentRandomizer._generate_correlated(overall_skill, variance=10)

        # Crash inversement proportionnel (meilleur pilote = moins de crash)
        crash = TalentRandomizer._generate_inverse(overall_skill, base=50, variance=15)

        # CompletedLaps élevé si crash bas
        completed_laps = TalentRandomizer._generate_inverse(crash, base=95, variance=8)
        completed_laps = max(75.0, min(99.0, completed_laps))  # Entre 75-99%

        # Recovery aide à gérer les erreurs
        recovery = TalentRandomizer._generate_correlated(overall_skill, variance=12)

        # Aggression et Courtesy sont plus indépendantes
        aggression = random.uniform(30, 90)
        courtesy = random.uniform(40, 85)

        # MinRacingSkill proche de l'overall
        min_racing_skill = TalentRandomizer._generate_correlated(overall_skill, variance=5)

        # Génération des informations personnelles
        # Victoires, poles, championnats basés sur le niveau
        starts = 0
        poles = 0
        wins = 0
        championships = 0

        # 70% de chances d'avoir de l'expérience
        if random.random() < 0.7:
            # Nombre de départs basé sur le niveau (plus haut = plus d'expérience)
            starts = int(random.uniform(10, 300) * (overall_skill / 80))

            # Poles proportionnels aux départs et à la vitesse
            if starts > 0:
                pole_rate = (speed / 100) * random.uniform(0.05, 0.25)
                poles = int(starts * pole_rate)

            # Victoires proportionnelles aux poles et au niveau général
            if poles > 0:
                win_rate = (overall_skill / 100) * random.uniform(0.3, 0.8)
                wins = int(poles * win_rate)

            # Championnats pour les meilleurs pilotes
            if overall_skill > 85 and wins > 20:
                championships = random.randint(1, 5)
            elif overall_skill > 75 and wins > 10:
                if random.random() < 0.3:
                    championships = random.randint(1, 2)

        # Reputation basée sur les résultats
        reputation = TalentRandomizer._calculate_reputation(
            overall_skill, wins, championships
        )

        # Génération date de naissance (18-45 ans)
        birth_year = random.randint(1979, 2007)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Évite les problèmes de jours invalides

        # Nationalité aléatoire
        nationality = random.choice(TalentRandomizer.NATIONALITIES)

        return {
            "personal_info": {
                "nationality": nationality,
                "date_of_birth": f"{birth_day}-{birth_month}-{birth_year}",
                "starts": starts,
                "poles": poles,
                "wins": wins,
                "drivers_championships": championships,
            },
            "stats": {
                "speed": round(speed, 1),
                "aggression": round(aggression, 1),
                "reputation": round(reputation, 1),
                "courtesy": round(courtesy, 1),
                "composure": round(composure, 1),
                "crash": round(crash, 1),
                "recovery": round(recovery, 1),
                "completed_laps": round(completed_laps, 1),
                "min_racing_skill": round(min_racing_skill, 1),
            },
        }

    @staticmethod
    def _generate_correlated(base: float, variance: float) -> float:
        """
        Generate a value correlated with the base value.

        Args:
            base: Base value (0-100)
            variance: Maximum variance from base

        Returns:
            Float value between 0 and 100
        """
        value = base + random.uniform(-variance, variance)
        return max(0.0, min(100.0, value))

    @staticmethod
    def _generate_inverse(value: float, base: float, variance: float) -> float:
        """
        Generate a value inversely correlated with the input.

        Args:
            value: Input value (0-100)
            base: Base value for the result
            variance: Maximum variance from base

        Returns:
            Float value between 0 and 100
        """
        # Inverse: high value → low result
        # Instead of base - value (which can go negative for high values),
        # use 100 - value to get the inverse, then scale it
        inverse_normalized = 100.0 - value  # 0-100 becomes 100-0

        # Apply base and variance
        # Map inverse_normalized (0-100) to around base with variance
        scaling_factor = base / 50.0  # Scale relative to middle point
        result = (inverse_normalized * scaling_factor) + random.uniform(-variance, variance)

        return max(0.0, min(100.0, result))

    @staticmethod
    def _calculate_reputation(skill: float, wins: int, championships: int) -> float:
        """
        Calculate reputation based on skill and achievements.

        Args:
            skill: Overall skill level (0-100)
            wins: Number of wins
            championships: Number of championships

        Returns:
            Reputation value (0-100)
        """
        # Base sur le skill
        reputation = skill

        # Bonus pour victoires (max +15)
        win_bonus = min(15, wins * 0.5)
        reputation += win_bonus

        # Bonus pour championnats (max +20)
        championship_bonus = min(20, championships * 4)
        reputation += championship_bonus

        # Petit facteur aléatoire
        reputation += random.uniform(-5, 5)

        return max(0.0, min(100.0, reputation))

    @staticmethod
    def random_field(field_name: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Generate a random value for a specific field.

        Used for CSV import to fill missing fields.

        Args:
            field_name: Name of the field to generate
            context: Optional context (e.g., other field values for coherence)

        Returns:
            Random value for the field

        Supported fields:
        - nationality
        - date_of_birth
        - starts, poles, wins, drivers_championships
        - speed, crash, aggression, reputation, courtesy, composure,
          recovery, completed_laps, min_racing_skill
        """
        context = context or {}

        # Nationalité
        if field_name == "nationality":
            return random.choice(TalentRandomizer.NATIONALITIES)

        # Date de naissance (18-45 ans)
        if field_name == "date_of_birth":
            birth_year = random.randint(1979, 2007)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            return f"{birth_day}-{birth_month}-{birth_year}"

        # Stats de carrière (basées sur un niveau estimé)
        if field_name in ["starts", "poles", "wins", "drivers_championships"]:
            # Estimer un niveau depuis le contexte ou générer aléatoirement
            estimated_skill = context.get("speed", random.uniform(40, 95))

            # 70% de chances d'avoir de l'expérience
            if random.random() < 0.7:
                if field_name == "starts":
                    return int(random.uniform(10, 300) * (estimated_skill / 80))
                elif field_name == "poles":
                    starts = context.get("starts", 50)
                    if starts > 0:
                        pole_rate = (estimated_skill / 100) * random.uniform(0.05, 0.25)
                        return int(starts * pole_rate)
                    return 0
                elif field_name == "wins":
                    poles = context.get("poles", 5)
                    if poles > 0:
                        win_rate = (estimated_skill / 100) * random.uniform(0.3, 0.8)
                        return int(poles * win_rate)
                    return 0
                elif field_name == "drivers_championships":
                    wins = context.get("wins", 0)
                    if estimated_skill > 85 and wins > 20:
                        return random.randint(1, 5)
                    elif estimated_skill > 75 and wins > 10:
                        return random.randint(1, 2) if random.random() < 0.3 else 0
                    return 0
            return 0

        # Stats de course
        if field_name in ["speed", "crash", "aggression", "reputation", "courtesy",
                          "composure", "recovery", "completed_laps", "min_racing_skill"]:
            # Générer toutes les stats cohérentes, puis retourner celle demandée
            racing_stats = TalentRandomizer.random_racing_stats()
            return racing_stats.get(field_name, 50.0)

        # Champ non reconnu
        raise ValueError(f"Unknown field: {field_name}")

    @staticmethod
    def fill_missing_fields(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fill missing fields in a talent data dictionary.

        Used for CSV import to complete incomplete rows.

        Args:
            data: Partial talent data (e.g., from CSV row)

        Returns:
            Complete talent data with all missing fields filled

        Expected structure:
        {
            "name": str (required, not generated),
            "nationality": str (optional),
            "date_of_birth": str (optional),
            "starts": int (optional),
            "poles": int (optional),
            "wins": int (optional),
            "drivers_championships": int (optional),
            "speed": float (optional),
            "crash": float (optional),
            ... other racing stats ...
        }
        """
        # Créer une copie pour ne pas modifier l'original
        result = data.copy()

        # Liste des champs à vérifier
        personal_fields = ["nationality", "date_of_birth", "starts", "poles", "wins", "drivers_championships"]
        racing_fields = ["speed", "crash", "aggression", "reputation", "courtesy",
                        "composure", "recovery", "completed_laps", "min_racing_skill"]

        # Context pour cohérence (par exemple, utiliser speed pour calculer starts)
        context = {}

        # Remplir les stats de course d'abord (si manquantes toutes ensemble)
        missing_racing = [f for f in racing_fields if f not in result or result[f] is None or result[f] == ""]
        if len(missing_racing) == len(racing_fields):
            # Toutes les stats manquent, générer un set cohérent
            racing_stats = TalentRandomizer.random_racing_stats()
            for field in racing_fields:
                result[field] = racing_stats[field]
                context[field] = racing_stats[field]
        else:
            # Certaines stats existent, remplir individuellement
            for field in missing_racing:
                result[field] = TalentRandomizer.random_field(field, context)
                context[field] = result[field]

        # Remplir les champs personnels
        for field in personal_fields:
            if field not in result or result[field] is None or result[field] == "":
                result[field] = TalentRandomizer.random_field(field, context)
                context[field] = result[field]

        return result
