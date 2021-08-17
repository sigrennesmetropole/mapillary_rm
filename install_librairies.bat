@echo off
rem l'ordre est important pour les dépendances

cls

set mode=install
rem set mode=uninstall -y

echo Mode : %mode%
echo Confirmez ?
pause

rem GOTO:EOF

python.exe -m pip %mode% modules_python\argparse-1.4.0-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\urllib3-1.24.3-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\chardet-3.0.4-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\idna-2.7-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\certifi-2020.6.20-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\requests-2.20.0-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\setuptools-44.1.1-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\colorama-0.4.4-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\py-1.9.0-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\pytest-3.2.3-py2.py3-none-any.whl

python.exe -m pip %mode% modules_python\zope.interface-5.1.2-cp27-cp27m-win_amd64.whl
python.exe -m pip %mode% modules_python\six-1.15.0-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\python_dateutil-2.7.3-py2.py3-none-any.whl

python.exe -m pip %mode% modules_python\pytz-2020.1-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\DateTime-4.3-py2.py3-none-any.whl

python.exe -m pip %mode% modules_python\aenum-2.2.4-py2-none-any.whl
python.exe -m pip %mode% modules_python\construct-2.8.8-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\ExifRead-2.1.2-py2-none-any.whl
python.exe -m pip %mode% modules_python\piexif-1.0.13m-py2-none-any.whl
python.exe -m pip %mode% modules_python\gpxpy-0.9.8-py2-none-any.whl
python.exe -m pip %mode% modules_python\pynmea2-1.12.0-py2-none-any.whl
python.exe -m pip %mode% modules_python\Pillow-2.9.0-cp27-none-win_amd64.whl
python.exe -m pip %mode% modules_python\pymp4-1.1.0-py2.py3-none-any.whl
python.exe -m pip %mode% modules_python\tqdm-2.2.4-py2.py3-none-any.whl

python.exe -m pip %mode% modules_python\GDAL-2.2.4-cp27-cp27m-win_amd64.whl

python.exe -m pip %mode% modules_python\mapillary_tools-0.5.3-py2-none-any.whl

pause
