# Tygron AI Object Detectie GUI

Deze Streamlit applicatie gebruikt getrainde PyTorch modellen (.pt) om objecten te detecteren en segmenteren in afbeeldingen.

## Functionaliteiten

- **Model Selectie**: Kies uit beschikbare .pt modellen in de Models directory
- **Afbeelding Upload**: Upload afbeeldingen in PNG, JPG of JPEG formaat
- **Object Detectie**: Detecteert objecten en toont bounding boxes
- **Segmentatie**: Toont segmentatie maskers over gedetecteerde objecten
- **Resultaat Visualisatie**: Toont originele en geanalyseerde afbeelding naast elkaar
- **Detectie Statistieken**: Toont aantal detecties, betrouwbaarheidsscores en details

## Installatie

1. Installeer de vereiste packages:
```bash
pip install -r requirements.txt
```

2. Zorg ervoor dat er .pt modellen aanwezig zijn in de `../Models/` directory

## Gebruik

1. Start de applicatie:
```bash
streamlit run GUI.py
```

2. Selecteer een model uit de dropdown
3. Upload een afbeelding
4. Klik op "Analyseer Afbeelding" om de detectie uit te voeren

## Vereisten

- Python 3.8+
- PyTorch 2.0+
- Streamlit 1.29+
- Getrainde .pt modellen in de Models directory

## Model Ondersteuning

De applicatie ondersteunt PyTorch modellen die zijn getraind met de Tygron AI training pipeline. Het model moet de volgende output structuur hebben:
- `boxes`: Bounding box coördinaten
- `scores`: Betrouwbaarheidsscores
- `masks`: Segmentatie maskers (optioneel)
- `labels`: Klasse labels

## Technische Details

- Gebruikt torchvision voor image preprocessing
- Ondersteunt CUDA acceleratie indien beschikbaar
- Automatische model configuratie
- Real-time inferentie visualisatie
