# Chaîne de traitement pour traiter et téléverser des photos 360° vers Mapillary

Ce projet rassemble les ressources qui permettent de traiter les images 360° dérivées de l'acquisition *mobile mapping* pour le RMTR surface. Ces images sont en effet un produit dérivé des acquisitions LIDAR faite avec du matériel [Ladybug](https://www.flir.fr/products/ladybug5plus/).

Mais les images récupérées ne sont pas bien crées et ne sont pas, dans leur état natif, des images 360°.


## Principe

Le script :
1. lit le fichier IML d'une campagne d'acquisition
2. en dérive un fichier CSV avec les attributs utiles : image, time, x, y, z, h
3. modifie les métadonnées EXIF des images pour injecter les données de localisation afn de les rendre 360°
4. appelle les *mapillary tools* pour prétraiter les images (supression des images trop proches, par exemple)
5. téléverse vers l'API de Mapillary


## Prérequis

- terminal MINTTY (installé via git pour Windows) OU ms-dos
- Python 3.6.8
- les modules python dans le répertoire `modules_python`


Librairies :
- aenum 2.2.4
- argparse 1.4.0
- certifi 2020.6.20
- chardet 3.0.4
- colorama 0.4.4
- construct 2.8.8
- DateTime 4.3
- ExifRead 2.1.2
- gpxpy 0.9.8
- idna 2.7
- mapillary_tools 0.5.3
- piexif 1.0.13m
- Pillow 2.9.0
- py 1.9.0
- pymp4 1.1.0
- pynmea2 1.12.0
- pyproj 2.2.2
- pytest 3.2.3
- python_dateutil 2.7.3
- pytz 2020.1
- requests 2.20.0
- setuptools 44.1.1
- six 1.15.0
- tqdm 2.2.4
- urllib3 1.24.3
- zope.interface 5.1.2


## Activer une session virtuelle Python

Pour toute opération (installation ou utilisation) on va se mettre dans une session virtuelle Python. Voir [la procédure](python_venv.md) pour mettre en place une session virtuelle Python.

`source ./venv/Scripts/activate`


## installation des librairies Python

Ouvrir un terminal MS-DOS
Aller dans le répertoire de traitement

	cd C:\Users\acces.sig\Documents\mapillary\traitement

On installe les librairies, via un script car il y a un ordre à cause des dépendances

	install_librairies.bat

Vérifier qu'il n'y a pas d'erreurs (en rouge)
Ignorer les alertes de non vérification SSL (car on ne sort pas à cause du proxy)


Créer une variable d'environment GDAL_DATA qui pointe vers C:\python\2.7.18\Lib\site-packages\osgeo\data\gdal


## Utilisation

Pour info : ctrl + maj + V pour coller des commandes ms-dos


Comme on a un problème avec les chemins Windows : on va dans le répertoire à traiter
Ainsi on appellera le répertoire courant.

Ouvrir un terminal MS-DOS.

	g:
	cd "3_Photos\StreetMapper Aout2016 - 2018-02-16 - ACIGNE_1602"
	
	
--------
Afficher l'aide

	python.exe C:\Users\acces.sig\Documents\mapillary\traitement\process_sequence.py -h
	
	usage: process_sequence.py [-h] [--skip-preprocess] [--skip-exif]
							   [--skip-upload]
							   DATE PATH MAPILLARY_USER

	Processing Geofit files for geolocating pictures and upload to Mapillary

	positional arguments:
	  DATE               pictures shooting date in YYYY-MM-DD format
	  PATH               path to access one sequence files (IML + JPG)
	  MAPILLARY_USER     Mapillary user name

	optional arguments:
	  -h, --help         show this help message and exit
	  --skip-preprocess  don't run preprocessing of pictures
	  --skip-exif        don't write updated EXIF metadata in pictures
	  --skip-upload      don't run upload of pictures

	  

Juste analyser et traiter le fichier IML

	python.exe C:\Users\acces.sig\Documents\mapillary\traitement\process_sequence.py --skip-exif --skip-upload 2018-02-16 .\ sig_rm
	


Juste patcher les métadonnées EXIF des photos : pas de preprocess ni d'upload

	python.exe C:\Users\acces.sig\Documents\mapillary\traitement\process_sequence.py --skip-preprocess --skip-upload 2018-02-16 .\ sig_rm
	
	

Juste l'upload

	python.exe C:\Users\acces.sig\Documents\mapillary\traitement\process_sequence.py --skip-preprocess --skip-exif 2018-02-16 .\ sig_rm



La totale

	python.exe C:\Users\acces.sig\Documents\mapillary\traitement\process_sequence.py 2018-02-16 .\ sig_rm


A chaque lancement, le script va vérifier les dates dans le fichier IML et demander de valider ou corriger date et heure de début des prises de vues.
Exemple :


	G:\3_Photos\StreetMapper Aout2016 - 2018-02-16 - ACIGNE_1602>python.exe C:\Users\acces.sig\Documents\mapillary\traitement\process_sequence.py --skip-upload 2018-02-16 .\ sig_rm
	Checking picture validity 16225/16226 (99%)
	Found 1 IML files
	Found 16226 JPG files
	Reading IML file line 3/438103 (0%)
	Start date read from IML : 2024-07-16T11:03:11.356000
	Do you want to use your date instead (2018-02-16) ? (y/n) y
	Set the capture start time (in HH:MM format) : 09:00   



Pour vérifier que les coordonnées sont bonnes on peut ouvrir une image dans XnView

menu Edition > métadonnées > Ouvrir la position GPS dans geohack



## Notes

Pour la partie GDAL on utilise le .whl de ce site 
https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

