from src.agent_configs import WARDROBE

def check_weather():
    return "Cold, rainy"

def get_wardrobe_items():
    if not WARDROBE:
        return "Your wardrobe is empty."
    items = []
    for item, status in WARDROBE.items():
        items.append(f"Item {item} is {status}")
    return "; ".join(items)

def wash_clothing(item_name):
    if item_name not in WARDROBE:
        return f"Item '{item_name}' not found in wardrobe"
    WARDROBE[item_name] = "clean"
    return f"{item_name} is washed"