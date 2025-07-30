#### PATHING ISSUES FIX ####
import os, sys

print("Aantal paden in sys.path:", len(sys.path))
# Bepaal de parent-werkmap
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

#Loop door alle submappen en voeg ze toe aan sys.path
for dirpath, dirnames, filenames in os.walk(parent_dir):
    if dirpath not in sys.path:
        sys.path.insert(0, dirpath)

print("Aantal paden in sys.path:", len(sys.path))
###########

import streamlit as st
from PIL import Image
import os
import sys
import torch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tempfile
import io
from torchvision.io import read_image, ImageReadMode
from torchvision.utils import draw_bounding_boxes, draw_segmentation_masks
from torchvision import tv_tensors
from torchvision.transforms import v2

from Libraries.inference_training import createModelInstance, createTransforms

# Voeg het Libraries pad toe aan sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
libraries_dir = os.path.join(script_dir, '..', 'Libraries')
sys.path.append(libraries_dir)


# Configuration class (vereenvoudigde versie)
class Configuration:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.numClasses = 3  # Achtergrond + 1 klasse
        self.bboxPerImage = 250
        self.maskThreshold = 0.5
        self.inputWidth = 250
        self.inputHeight = 250

# Path handelen
logo_path = os.path.join(script_dir, 'TygronLogo.png')
models_dir = os.path.join(script_dir, '..', 'Models')

# Configureren van de streamlit
img = Image.open(logo_path)
st.set_page_config(layout="wide", page_title="Tygron AI - Object Detectie", page_icon=img)
st.image(logo_path, width=175)

st.title("Tygron AI - Object Detectie en Segmentatie")

st.sidebar.markdown("""**Welkom bij de Tygron AI Object Detectie Tool**   
                     
*Gebruiksaanwijzing:*  
1. Selecteer een getraind model uit de dropdown
2. Upload een afbeelding
3. Klik op 'Analyseer Afbeelding' om de detectie uit te voeren
""")

left, right = st.columns(2)
with left:
    # Model selectie
    st.subheader("Model Selectie")
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.pt')]
    if model_files:
        selected_model = st.selectbox("Kies een model:", model_files)
        model_path = os.path.join(models_dir, selected_model)
    else:
        st.error("Geen .pt modellen gevonden in de Models directory")
        st.stop()
with right:
    # Afbeelding upload
    st.subheader("Afbeelding Upload")
    uploaded_file = st.file_uploader("Kies een afbeelding", type=['png', 'jpg', 'jpeg'])


st.markdown("---")


if uploaded_file is not None:
    # Toon de originele afbeelding
    original_image = Image.open(uploaded_file)
    
   # st.subheader("Originele Afbeelding")
    #st.image(original_image, caption="Originele afbeelding", use_column_width=True)
    
    # Analyseer knop
    if st.button("Analyseer Afbeelding", type="primary"):
        with st.spinner("Model wordt geladen..."):
            try:
                # Laad de configuratie
                config = Configuration()
                
                # Laad het model
                model = createModelInstance(config)
                model.load_state_dict(torch.load(model_path, map_location=config.device, weights_only=True))
                model.to(config.device)
                model.eval()
                
                st.success("Model succesvol geladen!")
                
            except Exception as e:
                st.error(f"Fout bij het laden van het model: {str(e)}")
                st.stop()
        
        with st.spinner("Afbeelding wordt geanalyseerd..."):
            try:
                # Sla de geüploade afbeelding tijdelijk op
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                    original_image.save(tmp_file.name)
                    
                    # Laad de afbeelding met torchvision
                    image = read_image(tmp_file.name, mode=ImageReadMode.RGB)
                    image = v2.functional.convert_image_dtype(image, dtype=torch.float)
                    image = tv_tensors.Image(image)
                    
                    # Maak transformaties
                    eval_transform = createTransforms(train=False)
                    
                    # Voer inferentie uit
                    with torch.no_grad():
                        x = eval_transform(image)
                        x = x.to(config.device)
                        predictions = model([x])
                        pred = predictions[0]
                    
                    # Bereid de afbeelding voor visualisatie voor
                    display_image = image[:3, ...]  # Neem alleen RGB kanalen
                    display_image = (255.0 * (display_image - display_image.min()) / 
                                   (display_image.max() - display_image.min())).to(torch.uint8)
                    
                    # Maak labels voor detecties
                    pred_labels = [f"Score: {score:.3f}" for score in pred["scores"]]
                    pred_boxes = pred["boxes"].long()
                    
                    # Teken bounding boxes
                    output_image = draw_bounding_boxes(display_image, pred_boxes, pred_labels, colors="red")
                    
                    # Teken segmentatie maskers
                    if "masks" in pred and len(pred["masks"]) > 0:
                        masks = (pred["masks"] > config.maskThreshold).squeeze(1)
                        output_image = draw_segmentation_masks(output_image, masks, alpha=0.5, colors="blue")
                    
                    # Converteer naar PIL Image voor weergave
                    output_image_pil = Image.fromarray(output_image.permute(1, 2, 0).numpy())
                    
                    # Toon resultaten
                    st.subheader("Analyse Resultaten")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Originele Afbeelding**")
                        st.image(original_image, use_column_width=True)
                    
                    with col2:
                        st.write("**Geanalyseerde Afbeelding**")
                        st.image(output_image_pil, use_column_width=True)
                    
                    # Toon detectie statistieken
                    st.subheader("Detectie Statistieken")
                    num_detections = len(pred["boxes"])
                    st.write(f"**Aantal detecties:** {num_detections}")
                    
                    if num_detections > 0:
                        scores = pred["scores"].cpu().numpy()
                        st.write(f"**Hoogste betrouwbaarheid:** {scores.max():.3f}")
                        st.write(f"**Gemiddelde betrouwbaarheid:** {scores.mean():.3f}")
                        
                        # Toon top detecties in een tabel
                        if num_detections > 0:
                            st.write("**Top Detecties:**")
                            detection_data = []
                            for i, (box, score) in enumerate(zip(pred["boxes"][:5], pred["scores"][:5])):
                                detection_data.append({
                                    "Detectie": i+1,
                                    "Betrouwbaarheid": f"{score:.3f}",
                                    "Bounding Box": f"({box[0]:.0f}, {box[1]:.0f}, {box[2]:.0f}, {box[3]:.0f})"
                                })
                            
                            df = pd.DataFrame(detection_data)
                            st.table(df)
                    
                    # Opruimen
                    os.unlink(tmp_file.name)
                    
                    st.success("Analyse voltooid!")
                    
            except Exception as e:
                st.error(f"Fout tijdens analyse: {str(e)}")
                import traceback
                st.error(traceback.format_exc())

else:
    st.info("Upload een afbeelding om te beginnen met de analyse.")

# Footer
st.markdown("---")
st.markdown("*Ontwikkeld door het Tygron AI team*")
