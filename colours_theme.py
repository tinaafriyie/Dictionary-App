from enum import Enum

class AppColors(Enum):
    PRIMARY = "#6750A4"  # Primary color (Purple)
    SECONDARY = "#E8DEF8"  # Secondary color (Light Purple)
    SURFACE = "#FFFBFE"  # Surface color (Almost White)
    ERROR = "#B3261E"  # Error color (Red)
    ACCENT = "#D0BCFF"  # Accent color (Light Purple)
    TEXT = "#1C1B1F"  # Primary text color (Dark Grey)
    TEXT_SECONDARY = "#49454F"  # Secondary text color (Grey)
    SUCCESS = "#CDEAC0"  # Success color (Light Green)

    def get_colors(theme_name):
        if theme_name == "default":
            return {
                "primary": "#6750A4",  # Purple
                "secondary": "#E8DEF8",  # Light Purple
                "surface": "#FFFBFE",  # Almost White
                "error": "#B3261E",  # Red
                "accent": "#D0BCFF",  # Light Purple
                "text": "#1C1B1F",  # Dark Grey
                "text_secondary": "#49454F",  # Grey
                "success": "#CDEAC0",  # Light Green
                "gradient_end": "#9A82DB"  # Light Purple
            }
        elif theme_name == "blue":
            return {
                "primary": "#1565C0",  # Blue
                "secondary": "#BBDEFB",  # Light Blue
                "surface": "#E3F2FD",  # Very Light Blue
                "error": "#B71C1C",  # Dark Red
                "accent": "#64B5F6",  # Light Blue
                "text": "#0D47A1",  # Dark Blue
                "text_secondary": "#1976D2",  # Blue
                "success": "#A5D6A7",  # Light Green
                "gradient_end": "#4F83CC"  # Blue
            }
        elif theme_name == "cream":
            return {
                "primary": "#E4B363",  # Cream
                "secondary": "#F7F4D4",  # Light Cream
                "surface": "#FFFDF6",  # Very Light Cream
                "error": "#C53B27",  # Dark Red
                "accent": "#F4D35E",  # Yellow
                "text": "#43341B",  # Brown
                "text_secondary": "#7D6C38",  # Dark Yellow
                "success": "#C2D6A4",  # Light Green
                "gradient_end": "#EAC779"  # Cream
            }
        elif theme_name == "green":
            return {
                "primary": "#388E3C",  # Green
                "secondary": "#C8E6C9",  # Light Green
                "surface": "#F1F8E9",  # Very Light Green
                "error": "#D32F2F",  # Dark Red
                "accent": "#81C784",  # Light Green
                "text": "#1B5E20",  # Dark Green
                "text_secondary": "#2E7D32",  # Green
                "success": "#A5D6A7",  # Light Green
                "gradient_end": "#4CAF50"  # Green
            }
        elif theme_name == "red":
            return {
                "primary": "#C62828",  # Red
                "secondary": "#FFCDD2",  # Light Red
                "surface": "#FFEBEE",  # Very Light Red
                "error": "#7B1FA2",  # Purple
                "accent": "#EF5350",  # Light Red
                "text": "#B71C1C",  # Dark Red
                "text_secondary": "#C62828",  # Red
                "success": "#C8E6C9",  # Light Green
                "gradient_end": "#EF5350"  # Red
            }
        elif theme_name == "ocean":
            return {
                "primary": "#006064",  # Teal
                "secondary": "#B2EBF2",  # Light Teal
                "surface": "#E0F7FA",  # Very Light Teal
                "error": "#BF360C",  # Dark Red
                "accent": "#4DD0E1",  # Light Teal
                "text": "#00363A",  # Dark Teal
                "text_secondary": "#00838F",  # Teal
                "success": "#80CBC4",  # Light Green
                "gradient_end": "#0097A7"  # Teal
            }
        elif theme_name == "sunset":
            return {
                "primary": "#FF6F00",  # Orange
                "secondary": "#FFE0B2",  # Light Orange
                "surface": "#FFF8E1",  # Very Light Orange
                "error": "#C2185B",  # Dark Pink
                "accent": "#FFB74D",  # Light Orange
                "text": "#BF360C",  # Dark Orange
                "text_secondary": "#E65100",  # Orange
                "success": "#DCEDC8",  # Light Green
                "gradient_end": "#F57C00"  # Orange
            }
        elif theme_name == "brown":
            return {
                "primary": "#432818",  # Dark Brown
                "secondary": "#6F4E37",  # Brown
                "surface": "#A0522D",  # Light Brown
                "error": "#8B4513",  # Saddle Brown
                "accent": "#D2691E",  # Chocolate
                "text": "#5C4033",  # Dark Brown
                "text_secondary": "#7B3F00",  # Brown
                "success": "#8B5A2B",  # Light Brown
                "gradient_end": "#A0522D"  # Light Brown
            }
        else:
            # Default to original theme if the specified theme doesn't exist
            return AppColors.get_colors("default")
        
