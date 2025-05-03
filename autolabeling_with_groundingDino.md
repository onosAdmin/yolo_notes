## How to use Grounding DINO

```


git clone https://github.com/IDEA-Research/GroundingDINO.git
cp GroundingDINO_download_weights.py GroundingDINO/
cp  groundingDino.py GroundingDINO/
cd GroundingDINO/

python3 -m pip install -e .

python3 -m pip install autodistill-grounding-dino
python3 -m pip install scikit-learn

mkdir weights
python3  GroundingDINO_download_weights.py

edit the path in groundingDino.py and then run it
python3  groundingDino.py





then to make the preelabelling:
edit the path in autolabeling_using_GroundingDINO.py and then run it

pythyon3 autolabeling_using_GroundingDINO.py
```
