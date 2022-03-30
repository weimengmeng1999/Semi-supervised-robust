
#ls .
#mkdir robustmis
#mount -t cifs -o user=mwei,password=WMwm199910156@ //10.246.201.201/laparoscopy/robustmis robustmis
#scp mwei@10.246.201.201:/laparoscopy/robustmislite robustmis
#ls robustmis

cd Fixmatch_seg
pip install --upgrade pip
pip install -r requirements.txt
python train.py --config configs/config_robust.json
