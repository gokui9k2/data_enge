import concurrent.futures
import subprocess
import sys
import os

def install_dependencies():
    requirements_path = "requirements.txt"
    if os.path.exists(requirements_path):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
    else:
        print("Le fichier requirements.txt est introuvable.")

def run_spider(spider_script, is_scrapy_project=False):
    if is_scrapy_project:
        # Pour le projet Scrapy, utiliser 'scrapy crawl'
        os.chdir(spider_script)  # Changer le répertoire de travail
        subprocess.run(["scrapy", "crawl", "ufc_spider"])
        os.chdir("..")  
    else:
        # Pour un script Python standard
        subprocess.run(["python", spider_script])

def run_nettoyage():
    subprocess.run(["python", "nettoyage.py"])
    

def launch_dash_app():
    os.chdir('/app/MultipageDash')
    
    # Lancer Gunicorn comme processus principal dans le thread actuel
    try:
        subprocess.run(["gunicorn", "-b", "0.0.0.0:8050", "--timeout", "120", "app:server"])
    except Exception as e:
        print(f"Erreur lors du lancement de Gunicorn: {e}")



if __name__ == "__main__":
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Lancer les spiders en simultané
        futures = [
            executor.submit(run_spider, "dc_spider.py"),
            executor.submit(run_spider, "scrapy_data_enge_1", is_scrapy_project=True)
        ]

        # Attendre que tous les spiders aient terminé
        for future in concurrent.futures.as_completed(futures):
            future.result()

    # Exécuter le nettoyage après la fin des spiders
    run_nettoyage()
    launch_dash_app()
