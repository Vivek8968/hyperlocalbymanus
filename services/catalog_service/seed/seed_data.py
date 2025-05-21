import json
import os
from typing import List, Dict, Any

# Electronics categories
CATEGORIES = [
    {"name": "Televisions", "description": "Smart TVs, LED TVs, OLED TVs, and more"},
    {"name": "Air Conditioners", "description": "Split ACs, Window ACs, Inverter ACs"},
    {"name": "Mobile Phones", "description": "Smartphones, feature phones, and accessories"},
    {"name": "Laptops", "description": "Notebooks, ultrabooks, gaming laptops"},
    {"name": "Refrigerators", "description": "Single door, double door, and multi-door refrigerators"},
    {"name": "Washing Machines", "description": "Front load, top load, and semi-automatic washing machines"},
    {"name": "Audio Devices", "description": "Speakers, headphones, earphones, and sound systems"},
    {"name": "Cameras", "description": "DSLR, mirrorless, and point-and-shoot cameras"},
    {"name": "Gaming Consoles", "description": "Video game consoles and accessories"},
    {"name": "Computer Accessories", "description": "Keyboards, mice, monitors, and other peripherals"}
]

# Sample TV brands and models
TV_ITEMS = [
    {
        "name": "Samsung 55-inch 4K Smart TV",
        "description": "55-inch 4K Ultra HD Smart LED TV with HDR",
        "category_id": 1,
        "brand": "Samsung",
        "model": "UA55TU8000",
        "image_url": "https://example.com/images/samsung-55-4k.jpg",
        "specifications": {
            "screen_size": "55 inches",
            "resolution": "3840 x 2160 (4K)",
            "refresh_rate": "60Hz",
            "connectivity": ["Wi-Fi", "Bluetooth", "HDMI", "USB"],
            "smart_features": ["Voice Control", "App Support", "Screen Mirroring"]
        }
    },
    {
        "name": "LG 65-inch OLED TV",
        "description": "65-inch 4K OLED Smart TV with Dolby Vision and Atmos",
        "category_id": 1,
        "brand": "LG",
        "model": "OLED65C1",
        "image_url": "https://example.com/images/lg-65-oled.jpg",
        "specifications": {
            "screen_size": "65 inches",
            "resolution": "3840 x 2160 (4K)",
            "refresh_rate": "120Hz",
            "connectivity": ["Wi-Fi", "Bluetooth", "HDMI 2.1", "USB"],
            "smart_features": ["WebOS", "ThinQ AI", "Magic Remote"]
        }
    },
    {
        "name": "Sony 50-inch LED TV",
        "description": "50-inch Full HD LED TV with X-Reality PRO",
        "category_id": 1,
        "brand": "Sony",
        "model": "KDL-50W660G",
        "image_url": "https://example.com/images/sony-50-led.jpg",
        "specifications": {
            "screen_size": "50 inches",
            "resolution": "1920 x 1080 (Full HD)",
            "refresh_rate": "60Hz",
            "connectivity": ["HDMI", "USB", "Composite"],
            "smart_features": ["X-Reality PRO", "Screen Mirroring"]
        }
    },
    {
        "name": "Mi 43-inch 4K Android TV",
        "description": "43-inch 4K Ultra HD Android LED TV with Dolby Audio",
        "category_id": 1,
        "brand": "Mi",
        "model": "Mi TV 4X 43",
        "image_url": "https://example.com/images/mi-43-4k.jpg",
        "specifications": {
            "screen_size": "43 inches",
            "resolution": "3840 x 2160 (4K)",
            "refresh_rate": "60Hz",
            "connectivity": ["Wi-Fi", "Bluetooth", "HDMI", "USB"],
            "smart_features": ["Android TV", "Google Assistant", "Chromecast"]
        }
    }
]

# Sample AC brands and models
AC_ITEMS = [
    {
        "name": "Daikin 1.5 Ton Inverter Split AC",
        "description": "1.5 Ton 5 Star Inverter Split AC with Copper Condenser",
        "category_id": 2,
        "brand": "Daikin",
        "model": "FTKF50TV",
        "image_url": "https://example.com/images/daikin-1.5ton.jpg",
        "specifications": {
            "capacity": "1.5 Ton",
            "energy_rating": "5 Star",
            "type": "Split AC",
            "compressor": "Inverter",
            "cooling_capacity": "5.28 kW",
            "special_features": ["PM 2.5 Filter", "Dehumidifier", "Sleep Mode"]
        }
    },
    {
        "name": "Voltas 1 Ton Window AC",
        "description": "1 Ton 3 Star Window AC with Copper Condenser",
        "category_id": 2,
        "brand": "Voltas",
        "model": "123 LZF",
        "image_url": "https://example.com/images/voltas-1ton.jpg",
        "specifications": {
            "capacity": "1 Ton",
            "energy_rating": "3 Star",
            "type": "Window AC",
            "compressor": "Rotary",
            "cooling_capacity": "3.53 kW",
            "special_features": ["Anti-dust Filter", "Sleep Mode"]
        }
    },
    {
        "name": "LG 2 Ton Dual Inverter Split AC",
        "description": "2 Ton 4 Star Dual Inverter Split AC with Copper Condenser",
        "category_id": 2,
        "brand": "LG",
        "model": "KS-Q24HNZD",
        "image_url": "https://example.com/images/lg-2ton.jpg",
        "specifications": {
            "capacity": "2 Ton",
            "energy_rating": "4 Star",
            "type": "Split AC",
            "compressor": "Dual Inverter",
            "cooling_capacity": "6.21 kW",
            "special_features": ["4-way Swing", "Auto Clean", "Monsoon Comfort"]
        }
    }
]

# Sample Mobile Phone brands and models
MOBILE_ITEMS = [
    {
        "name": "iPhone 13 Pro",
        "description": "Apple iPhone 13 Pro with A15 Bionic chip and Pro camera system",
        "category_id": 3,
        "brand": "Apple",
        "model": "iPhone 13 Pro",
        "image_url": "https://example.com/images/iphone-13-pro.jpg",
        "specifications": {
            "display": "6.1-inch Super Retina XDR",
            "processor": "A15 Bionic",
            "storage": "256GB",
            "camera": "Pro 12MP camera system",
            "battery": "Up to 22 hours video playback",
            "os": "iOS 15"
        }
    },
    {
        "name": "Samsung Galaxy S21",
        "description": "Samsung Galaxy S21 5G with Exynos 2100 and 8K video",
        "category_id": 3,
        "brand": "Samsung",
        "model": "Galaxy S21",
        "image_url": "https://example.com/images/samsung-s21.jpg",
        "specifications": {
            "display": "6.2-inch Dynamic AMOLED 2X",
            "processor": "Exynos 2100",
            "storage": "128GB",
            "camera": "Triple camera with 64MP telephoto",
            "battery": "4000mAh",
            "os": "Android 11"
        }
    },
    {
        "name": "OnePlus 9 Pro",
        "description": "OnePlus 9 Pro 5G with Hasselblad Camera and Snapdragon 888",
        "category_id": 3,
        "brand": "OnePlus",
        "model": "9 Pro",
        "image_url": "https://example.com/images/oneplus-9-pro.jpg",
        "specifications": {
            "display": "6.7-inch Fluid AMOLED with LTPO",
            "processor": "Snapdragon 888",
            "storage": "256GB",
            "camera": "Quad camera with Hasselblad",
            "battery": "4500mAh with Warp Charge 65T",
            "os": "OxygenOS based on Android 11"
        }
    },
    {
        "name": "Xiaomi Redmi Note 10 Pro",
        "description": "Redmi Note 10 Pro with 108MP camera and 120Hz display",
        "category_id": 3,
        "brand": "Xiaomi",
        "model": "Redmi Note 10 Pro",
        "image_url": "https://example.com/images/redmi-note-10-pro.jpg",
        "specifications": {
            "display": "6.67-inch 120Hz AMOLED",
            "processor": "Snapdragon 732G",
            "storage": "128GB",
            "camera": "108MP quad camera",
            "battery": "5020mAh with 33W fast charging",
            "os": "MIUI 12 based on Android 11"
        }
    },
    {
        "name": "Google Pixel 6",
        "description": "Google Pixel 6 with Google Tensor chip and advanced camera",
        "category_id": 3,
        "brand": "Google",
        "model": "Pixel 6",
        "image_url": "https://example.com/images/pixel-6.jpg",
        "specifications": {
            "display": "6.4-inch OLED",
            "processor": "Google Tensor",
            "storage": "128GB",
            "camera": "50MP wide + 12MP ultrawide",
            "battery": "4614mAh",
            "os": "Android 12"
        }
    }
]

# Sample Laptop brands and models
LAPTOP_ITEMS = [
    {
        "name": "MacBook Pro 14-inch",
        "description": "14-inch MacBook Pro with M1 Pro chip and Liquid Retina XDR display",
        "category_id": 4,
        "brand": "Apple",
        "model": "MacBook Pro 14",
        "image_url": "https://example.com/images/macbook-pro-14.jpg",
        "specifications": {
            "processor": "Apple M1 Pro",
            "memory": "16GB unified memory",
            "storage": "512GB SSD",
            "display": "14.2-inch Liquid Retina XDR",
            "graphics": "16-core GPU",
            "battery": "Up to 17 hours"
        }
    },
    {
        "name": "Dell XPS 13",
        "description": "Dell XPS 13 with 11th Gen Intel Core and InfinityEdge display",
        "category_id": 4,
        "brand": "Dell",
        "model": "XPS 13 9310",
        "image_url": "https://example.com/images/dell-xps-13.jpg",
        "specifications": {
            "processor": "11th Gen Intel Core i7",
            "memory": "16GB LPDDR4x",
            "storage": "512GB SSD",
            "display": "13.4-inch FHD+ InfinityEdge",
            "graphics": "Intel Iris Xe",
            "battery": "Up to 14 hours"
        }
    },
    {
        "name": "HP Spectre x360",
        "description": "HP Spectre x360 convertible laptop with 11th Gen Intel Core",
        "category_id": 4,
        "brand": "HP",
        "model": "Spectre x360 14",
        "image_url": "https://example.com/images/hp-spectre-x360.jpg",
        "specifications": {
            "processor": "11th Gen Intel Core i7",
            "memory": "16GB LPDDR4x",
            "storage": "1TB SSD",
            "display": "13.5-inch 3K2K OLED",
            "graphics": "Intel Iris Xe",
            "battery": "Up to 17 hours"
        }
    },
    {
        "name": "Lenovo ThinkPad X1 Carbon",
        "description": "Lenovo ThinkPad X1 Carbon Gen 9 business laptop",
        "category_id": 4,
        "brand": "Lenovo",
        "model": "ThinkPad X1 Carbon Gen 9",
        "image_url": "https://example.com/images/thinkpad-x1-carbon.jpg",
        "specifications": {
            "processor": "11th Gen Intel Core i7",
            "memory": "16GB LPDDR4x",
            "storage": "512GB SSD",
            "display": "14-inch WUXGA",
            "graphics": "Intel Iris Xe",
            "battery": "Up to 16 hours"
        }
    }
]

# Sample Refrigerator brands and models
REFRIGERATOR_ITEMS = [
    {
        "name": "Samsung 253L Double Door Refrigerator",
        "description": "253L 3 Star Frost Free Double Door Refrigerator",
        "category_id": 5,
        "brand": "Samsung",
        "model": "RT28T3122S8",
        "image_url": "https://example.com/images/samsung-253l.jpg",
        "specifications": {
            "capacity": "253 Liters",
            "energy_rating": "3 Star",
            "type": "Double Door",
            "cooling_technology": "Digital Inverter",
            "defrost_system": "Frost Free",
            "special_features": ["Convertible", "Stabilizer Free Operation"]
        }
    },
    {
        "name": "LG 190L Single Door Refrigerator",
        "description": "190L 4 Star Direct Cool Single Door Refrigerator",
        "category_id": 5,
        "brand": "LG",
        "model": "GL-B201ASPY",
        "image_url": "https://example.com/images/lg-190l.jpg",
        "specifications": {
            "capacity": "190 Liters",
            "energy_rating": "4 Star",
            "type": "Single Door",
            "cooling_technology": "Smart Inverter",
            "defrost_system": "Direct Cool",
            "special_features": ["Smart Connect", "Anti-bacterial Gasket"]
        }
    },
    {
        "name": "Whirlpool 292L Frost Free Refrigerator",
        "description": "292L 3 Star Frost Free Multi-Door Refrigerator",
        "category_id": 5,
        "brand": "Whirlpool",
        "model": "FP 313D",
        "image_url": "https://example.com/images/whirlpool-292l.jpg",
        "specifications": {
            "capacity": "292 Liters",
            "energy_rating": "3 Star",
            "type": "Multi-Door",
            "cooling_technology": "6th Sense IntelliSense Inverter",
            "defrost_system": "Frost Free",
            "special_features": ["Zeolite Technology", "Moisture Retention"]
        }
    }
]

# Sample Washing Machine brands and models
WASHING_MACHINE_ITEMS = [
    {
        "name": "LG 7 Kg Front Load Washing Machine",
        "description": "7 Kg 5 Star Fully Automatic Front Load Washing Machine",
        "category_id": 6,
        "brand": "LG",
        "model": "FHM1207SDW",
        "image_url": "https://example.com/images/lg-7kg.jpg",
        "specifications": {
            "capacity": "7 Kg",
            "energy_rating": "5 Star",
            "type": "Front Load",
            "motor": "Direct Drive",
            "wash_programs": 10,
            "special_features": ["Steam Wash", "Allergy Care", "Child Lock"]
        }
    },
    {
        "name": "Samsung 8.5 Kg Top Load Washing Machine",
        "description": "8.5 Kg Fully Automatic Top Load Washing Machine",
        "category_id": 6,
        "brand": "Samsung",
        "model": "WA85T4560NS",
        "image_url": "https://example.com/images/samsung-8.5kg.jpg",
        "specifications": {
            "capacity": "8.5 Kg",
            "energy_rating": "4 Star",
            "type": "Top Load",
            "motor": "Digital Inverter",
            "wash_programs": 8,
            "special_features": ["Magic Filter", "Wobble Technology", "Soft Closing Door"]
        }
    },
    {
        "name": "Bosch 7.5 Kg Front Load Washing Machine",
        "description": "7.5 Kg Fully Automatic Front Load Washing Machine",
        "category_id": 6,
        "brand": "Bosch",
        "model": "WAJ2846IIN",
        "image_url": "https://example.com/images/bosch-7.5kg.jpg",
        "specifications": {
            "capacity": "7.5 Kg",
            "energy_rating": "5 Star",
            "type": "Front Load",
            "motor": "EcoSilence Drive",
            "wash_programs": 15,
            "special_features": ["Anti-Vibration Design", "SpeedPerfect", "AllergyPlus"]
        }
    }
]

# Sample Audio Device brands and models
AUDIO_ITEMS = [
    {
        "name": "Sony WH-1000XM4 Wireless Headphones",
        "description": "Sony WH-1000XM4 Wireless Noise Cancelling Headphones",
        "category_id": 7,
        "brand": "Sony",
        "model": "WH-1000XM4",
        "image_url": "https://example.com/images/sony-wh1000xm4.jpg",
        "specifications": {
            "type": "Over-ear Headphones",
            "connectivity": "Bluetooth 5.0",
            "battery_life": "Up to 30 hours",
            "noise_cancellation": "Active Noise Cancellation",
            "special_features": ["Speak-to-chat", "Multipoint connection", "Touch controls"]
        }
    },
    {
        "name": "JBL Flip 5 Portable Speaker",
        "description": "JBL Flip 5 Waterproof Portable Bluetooth Speaker",
        "category_id": 7,
        "brand": "JBL",
        "model": "Flip 5",
        "image_url": "https://example.com/images/jbl-flip5.jpg",
        "specifications": {
            "type": "Portable Speaker",
            "connectivity": "Bluetooth 4.2",
            "battery_life": "Up to 12 hours",
            "waterproof": "IPX7",
            "special_features": ["PartyBoost", "USB-C charging", "Racetrack-shaped driver"]
        }
    },
    {
        "name": "Bose SoundLink Revolve+ II",
        "description": "Bose SoundLink Revolve+ II Portable Bluetooth Speaker",
        "category_id": 7,
        "brand": "Bose",
        "model": "SoundLink Revolve+ II",
        "image_url": "https://example.com/images/bose-revolve-plus.jpg",
        "specifications": {
            "type": "Portable Speaker",
            "connectivity": "Bluetooth",
            "battery_life": "Up to 17 hours",
            "waterproof": "IP55",
            "special_features": ["360° sound", "Built-in microphone", "Carrying handle"]
        }
    },
    {
        "name": "Apple AirPods Pro",
        "description": "Apple AirPods Pro with Active Noise Cancellation",
        "category_id": 7,
        "brand": "Apple",
        "model": "AirPods Pro",
        "image_url": "https://example.com/images/airpods-pro.jpg",
        "specifications": {
            "type": "In-ear Earbuds",
            "connectivity": "Bluetooth 5.0",
            "battery_life": "Up to 4.5 hours (24 hours with case)",
            "noise_cancellation": "Active Noise Cancellation",
            "special_features": ["Transparency mode", "Adaptive EQ", "Water resistant"]
        }
    }
]

# Sample Camera brands and models
CAMERA_ITEMS = [
    {
        "name": "Canon EOS R6",
        "description": "Canon EOS R6 Full-Frame Mirrorless Camera",
        "category_id": 8,
        "brand": "Canon",
        "model": "EOS R6",
        "image_url": "https://example.com/images/canon-eos-r6.jpg",
        "specifications": {
            "type": "Mirrorless",
            "sensor": "20.1MP Full-Frame CMOS",
            "processor": "DIGIC X",
            "video": "4K 60p, Full HD 120p",
            "autofocus": "Dual Pixel CMOS AF II",
            "special_features": ["In-body stabilization", "Eye Detection AF", "Wi-Fi connectivity"]
        }
    },
    {
        "name": "Nikon Z6 II",
        "description": "Nikon Z6 II Full-Frame Mirrorless Camera",
        "category_id": 8,
        "brand": "Nikon",
        "model": "Z6 II",
        "image_url": "https://example.com/images/nikon-z6-ii.jpg",
        "specifications": {
            "type": "Mirrorless",
            "sensor": "24.5MP BSI CMOS",
            "processor": "Dual EXPEED 6",
            "video": "4K 60p, Full HD 120p",
            "autofocus": "273-point Hybrid AF",
            "special_features": ["5-axis VR", "Dual card slots", "Eye-Detection AF"]
        }
    },
    {
        "name": "Sony Alpha A7 III",
        "description": "Sony Alpha A7 III Full-Frame Mirrorless Camera",
        "category_id": 8,
        "brand": "Sony",
        "model": "Alpha A7 III",
        "image_url": "https://example.com/images/sony-a7iii.jpg",
        "specifications": {
            "type": "Mirrorless",
            "sensor": "24.2MP Exmor R CMOS",
            "processor": "BIONZ X",
            "video": "4K 30p, Full HD 120p",
            "autofocus": "693-point phase-detection AF",
            "special_features": ["5-axis stabilization", "Eye AF", "15-stop dynamic range"]
        }
    }
]

# Sample Gaming Console brands and models
GAMING_ITEMS = [
    {
        "name": "Sony PlayStation 5",
        "description": "Sony PlayStation 5 Console with Ultra HD Blu-ray",
        "category_id": 9,
        "brand": "Sony",
        "model": "PlayStation 5",
        "image_url": "https://example.com/images/ps5.jpg",
        "specifications": {
            "processor": "AMD Zen 2 (8 cores, 16 threads)",
            "graphics": "AMD RDNA 2 (10.28 TFLOPS)",
            "storage": "825GB SSD",
            "resolution": "Up to 8K",
            "special_features": ["Ray Tracing", "3D Audio", "Haptic Feedback"]
        }
    },
    {
        "name": "Microsoft Xbox Series X",
        "description": "Microsoft Xbox Series X Console",
        "category_id": 9,
        "brand": "Microsoft",
        "model": "Xbox Series X",
        "image_url": "https://example.com/images/xbox-series-x.jpg",
        "specifications": {
            "processor": "AMD Zen 2 (8 cores, 16 threads)",
            "graphics": "AMD RDNA 2 (12 TFLOPS)",
            "storage": "1TB SSD",
            "resolution": "Up to 8K",
            "special_features": ["Quick Resume", "Auto HDR", "Smart Delivery"]
        }
    },
    {
        "name": "Nintendo Switch OLED Model",
        "description": "Nintendo Switch OLED Model with enhanced audio",
        "category_id": 9,
        "brand": "Nintendo",
        "model": "Switch OLED",
        "image_url": "https://example.com/images/switch-oled.jpg",
        "specifications": {
            "processor": "NVIDIA Custom Tegra",
            "display": "7-inch OLED",
            "storage": "64GB",
            "battery_life": "4.5-9 hours",
            "special_features": ["Tabletop mode", "TV mode", "Handheld mode"]
        }
    }
]

# Sample Computer Accessories brands and models
COMPUTER_ACCESSORIES_ITEMS = [
    {
        "name": "Logitech MX Master 3",
        "description": "Logitech MX Master 3 Advanced Wireless Mouse",
        "category_id": 10,
        "brand": "Logitech",
        "model": "MX Master 3",
        "image_url": "https://example.com/images/mx-master-3.jpg",
        "specifications": {
            "type": "Wireless Mouse",
            "connectivity": "Bluetooth, USB Receiver",
            "battery_life": "Up to 70 days",
            "dpi": "4000 DPI",
            "special_features": ["Electromagnetic scrolling", "App-specific customization", "Flow cross-computer control"]
        }
    },
    {
        "name": "Keychron K2 Mechanical Keyboard",
        "description": "Keychron K2 Wireless Mechanical Keyboard with Gateron Brown Switches",
        "category_id": 10,
        "brand": "Keychron",
        "model": "K2",
        "image_url": "https://example.com/images/keychron-k2.jpg",
        "specifications": {
            "type": "Mechanical Keyboard",
            "connectivity": "Bluetooth, USB-C",
            "switches": "Gateron Brown",
            "layout": "75% layout with 84 keys",
            "special_features": ["RGB backlight", "Mac/Windows compatible", "Hot-swappable"]
        }
    },
    {
        "name": "Dell UltraSharp U2720Q",
        "description": "Dell UltraSharp U2720Q 27-inch 4K USB-C Monitor",
        "category_id": 10,
        "brand": "Dell",
        "model": "U2720Q",
        "image_url": "https://example.com/images/dell-u2720q.jpg",
        "specifications": {
            "type": "Monitor",
            "display": "27-inch IPS",
            "resolution": "3840 x 2160 (4K)",
            "refresh_rate": "60Hz",
            "connectivity": ["HDMI", "DisplayPort", "USB-C"],
            "special_features": ["USB-C power delivery", "99% sRGB color coverage", "VESA mount compatible"]
        }
    },
    {
        "name": "Anker PowerExpand+ 7-in-1 USB-C Hub",
        "description": "Anker PowerExpand+ 7-in-1 USB-C Hub Adapter",
        "category_id": 10,
        "brand": "Anker",
        "model": "PowerExpand+ 7-in-1",
        "image_url": "https://example.com/images/anker-hub.jpg",
        "specifications": {
            "type": "USB-C Hub",
            "ports": ["HDMI", "USB-C", "USB-A", "SD card", "microSD card"],
            "power_delivery": "Up to 85W",
            "video_output": "4K@30Hz",
            "special_features": ["Compact design", "Travel-friendly", "Aluminum casing"]
        }
    }
]

# Combine all items
ALL_ITEMS = (
    TV_ITEMS + 
    AC_ITEMS + 
    MOBILE_ITEMS + 
    LAPTOP_ITEMS + 
    REFRIGERATOR_ITEMS + 
    WASHING_MACHINE_ITEMS + 
    AUDIO_ITEMS + 
    CAMERA_ITEMS + 
    GAMING_ITEMS + 
    COMPUTER_ACCESSORIES_ITEMS
)

def generate_seed_data():
    """
    Generate seed data for categories and catalog items
    """
    return {
        "categories": CATEGORIES,
        "catalog_items": ALL_ITEMS
    }

if __name__ == "__main__":
    # Generate seed data
    seed_data = generate_seed_data()
    
    # Save to JSON file
    with open("seed_data.json", "w") as f:
        json.dump(seed_data, f, indent=2)
    
    print(f"Generated seed data with {len(seed_data['categories'])} categories and {len(seed_data['catalog_items'])} catalog items")
