#! /bin/bash
mkdir ~/Documents/localization
mkdir ~/Documents/localization_merged
cp ~/Downloads/localization.zip ~/Documents/localization
unzip ~/Documents/localization/localization.zip -d  ~/Documents/localization/
./mergeLoc.py
rm ~/Downloads/localization.zip
cd ~/Documents/localization_merged
zip -r localization.zip Saury* localization_merged
cd ~/scripts/XMLTrans
cp ~/Documents/localization_merged/localization.zip ~/Downloads
rm -r ~/Documents/localization_merged
rm -r ~/Documents/localization
mkdir ~/Documents/localization
cp ~/Downloads/localization.zip ~/Documents/localization
unzip ~/Documents/localization/localization.zip -d  ~/Documents/localization/
./xmltrans.py
rm -r ~/Documents/localization
rm ~/Downloads/localization.zip
