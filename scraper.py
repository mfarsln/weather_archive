import requests
import os
from datetime import datetime

def download_maps():
    base_url = "https://www.wetterzentrale.de/maps/"
    models = {
        "GFS": {"prefix": "GFSOPEU", "runs": ["00", "12"]},
        "ECMWF": {"prefix": "ECMOPEU", "runs": ["00", "12"]}
    }
    # 1 = 500hPa & MSLP, 2 = 850hPa Temp
    parameters = {"1": "500hPa", "2": "850hPa"}
    steps = ["0", "24", "48", "72", "96", "120", "144", "168", "192", "216", "240"]
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    for model_name, config in models.items():
        for run in config["runs"]:
            for p_id, p_name in parameters.items():
                # Klasör yapısına parametre adını ekliyoruz (Örn: GFS_00z_850hPa)
                folder_path = f"archive/{today}/{model_name}_{run}z_{p_name}"
                os.makedirs(folder_path, exist_ok=True)
                
                for step in steps:
                    filename = f"{config['prefix']}{run}_{step}_{p_id}.png"
                    url = f"{base_url}{filename}"
                    
                    try:
                        response = requests.get(url, timeout=15)
                        if response.status_code == 200:
                            file_path = os.path.join(folder_path, filename)
                            with open(file_path, 'wb') as f:
                                f.write(response.content)
                            print(f"İndirildi: {p_name} - {filename}")
                    except Exception as e:
                        print(f"Hata {filename}: {e}")

if __name__ == "__main__":
    download_maps()

