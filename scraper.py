import requests
import os
from datetime import datetime

def download_maps():
    base_url = "https://www.wetterzentrale.de/maps/"
    models = {
        "GFS": {"prefix": "GFSOPEU", "runs": ["00", "12"], "steps": ["0", "24", "48", "72", "120"]},
        "ECMWF": {"prefix": "ECMOPEU", "runs": ["00", "12"], "steps": ["0", "24", "48", "72", "120"]}
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    for model_name, config in models.items():
        for run in config["runs"]:
            folder_path = f"archive/{today}/{model_name}_{run}z"
            os.makedirs(folder_path, exist_ok=True)
            
            for step in config["steps"]:
                filename = f"{config['prefix']}{run}_{step}_1.png"
                url = f"{base_url}{filename}"
                
                try:
                    response = requests.get(url, timeout=15)
                    if response.status_code == 200:
                        with open(os.path.join(folder_path, filename), 'wb') as f:
                            f.write(response.content)
                        print(f"İndirildi: {filename}")
                except Exception as e:
                    print(f"Hata {filename}: {e}")

if __name__ == "__main__":
    download_maps()