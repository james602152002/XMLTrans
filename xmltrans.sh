#! /bin/bash
mkdir ~/Documents/localization
cp ~/Downloads/localization.zip ~/Documents/localization
unzip ~/Documents/localization/localization.zip -d  ~/Documents/localization/
rm ~/Documents/localization/localization.zip
./xmltrans.py
rm -r ~/Documents/localization
