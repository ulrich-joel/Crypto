@echo off 
REM Sauvegarder le répertoire actuel 
set current_dir=%cd% 
REM Vérifier si un argument a été passé 
if "%~1"=="" ( 
 echo Aucun chemin fourni. Veuillez fournir un chemin. 
 exit /b 
) 
set path=%~1 
cd "C:\Users\ulrich.atchiengang\Desktop\IA" 
call .\venv\Scripts\activate 
REM Vérifier si Python est accessible 
where py >nul 2>nul 
if errorlevel 1 ( 
 echo 'py' n’est pas reconnu. Vérifiez votre installation de Python. 
 exit /b 
) 
py "crl.py" %* 
call deactivate 
REM Définir le répertoire de destination (où vous souhaitez déplacer les 
fichiers .CRL) 
set destination_dir="%current_dir%\directory" 
REM Créer le répertoire de destination s'il n'existe pas déjà 
if not exist %destination_dir% ( 
 mkdir %destination_dir% 
) 
REM Déplacer tous les fichiers .CRL du répertoire source vers le répertoire 
de destination 
move %path%\*.CRL %destination_dir% /Y 
echo Tous les fichiers .CRL ont été déplacés vers %destination_dir%. 
rem Revenir au répertoire d'origine 
cd %current_dir% 