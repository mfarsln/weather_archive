import requests
import os
from datetime import datetime

def download_weather_data():
    base_url = "https://www.wetterzentrale.de/maps/"
    pic_url = "https://www.wetterzentrale.de/pics/"
    
    # Ayarlar
    today = datetime.now().strftime('%Y-%m-%d')
    CITY_COORD = "410290" # İstanbul örneği (41.0N, 29.0E)
    
    # 1. HARİTALAR (Önceki mantık)
    map_models = {
        "GFS": {"prefix": "GFSOPEU", "runs": ["00", "12"]},
        "ECMWF": {"prefix": "ECMOPEU", "runs": ["00", "12"]}
    }
    map_params = {"1": "500hPa", "2": "850hPa"}
    steps = ["0", "24", "48", "72", "96", "120", "144", "168", "192", "216", "240"]

    # 2. DİYAGRAMLAR (Yeni Bölüm)
    diag_models = {
        "GEFS": "gefs", # GFS Ensemble
        "ECMWF_ENS": "ecm" # ECMWF Ensemble
    }

    # --- Haritaları İndir ---
    for model_name, config in map_models.items():
        for run in config["runs"]:
            for p_id, p_name in map_params.items():
                folder = f"archive/{today}/{model_name}_{run}z_{p_name}"
                os.makedirs(folder, exist_ok=True)
                for step in steps:
                    filename = f"{config['prefix']}{run}_{step}_{p_id}.png"
                    url = f"{base_url}{filename}"
                    save_image(url, folder, filename)

    # --- Diyagramları İndir ---
    for diag_label, model_code in diag_models.items():
        for run in ["00", "12"]:
            folder = f"archive/{today}/Diagrams_{run}z"
            os.makedirs(folder, exist_ok=True)
            # Örn: MS_410290_gefs_ens.png (Not: Bazı modellerde run bilgisi dosya adında farklı işleyebilir)
            # Wetterzentrale diyagramlarda genellikle en son run'ı 'ens' adıyla tutar. 
            # Ancak arşiv için run bazlı linkleri kontrol etmek gerekebilir.
            filename = f"MS_{CITY_COORD}_{model_code}_ens.png"
            url = f"{pic_url}{filename}"
            # Arşivde karışmaması için isimlendirmeyi değiştiriyoruz
            save_name = f"{diag_label}_{run}z_diagram.png"
            save_image(url, folder, save_name)

def save_image(url, folder, filename):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            with open(os.path.join(folder, filename), 'wb') as f:
                f.write(r.content)
            print(f"Başarılı: {filename}")
    except:
        pass

if __name__ == "__main__":
    download_weather_data()
