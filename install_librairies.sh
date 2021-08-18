#! /bin/bash

# notes
# DateTime requiert zope.interface
# tqdm requiert colorama
# mapillary_tools requiert tzwhere qui requiert Shapely

clear

mode=install
#mode=uninstall -y

echo "mode = $mode"

read -p "  Si ces infos sont exactes : appuyer sur la touche [Entrée] sinon faire ctrl + C pour arrêter."

python -m pip $mode --trusted-host pypi.org modules_python/argparse-1.4.0-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/urllib3-1.24.3-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/chardet-3.0.4-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/idna-2.7-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/certifi-2021.5.30-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/requests-2.20.0-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/zope.interface-5.1.2-cp36-cp36m-win_amd64.whl
python -m pip $mode --trusted-host pypi.org modules_python/six-1.16.0-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/python_dateutil-2.7.3-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/pytz-2021.1-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/DateTime-4.3-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/construct-2.8.8-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/ExifRead-2.1.2-py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/piexif-1.1.3-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/gpxpy-0.9.8-py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/pynmea2-1.12.0-py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/Pillow-8.3.1-cp36-cp36m-win_amd64.whl
python -m pip $mode --trusted-host pypi.org modules_python/pymp4-1.1.0-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/colorama-0.4.4-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/tqdm-4.62.1-py2.py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/GDAL-3.1.4-cp36-cp36m-win_amd64.whl
python -m pip $mode --trusted-host pypi.org modules_python/Shapely-1.7.1-cp36-cp36m-win_amd64.whl
python -m pip $mode --trusted-host pypi.org modules_python/tzwhere-3.0.3-py3-none-any.whl
python -m pip $mode --trusted-host pypi.org modules_python/mapillary_tools-0.7.4-py3-none-any.whl
