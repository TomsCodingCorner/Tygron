![Logo-Tygron](https://github.com/user-attachments/assets/cd238f33-4aa1-4b34-b7c7-a10c54ebae30)

# Tygron
Het team van groep 3 bestaat uit:
- Ties Smid – Scrum Master en contactpersoon voor de Product Owner
- Tom van der Kruijk – Verantwoordelijk voor backlogbeheer
- Elijah Hofman – Leiding Back-endontwikkeling

# Inleiding van het project
Het doel van dit project is het ontwikkelen van een Object Masking AI-model
dat automatisch priveparkeerplaatsen kan herkennen op basis van luchtfoto’s. Die uiteindelijk gebruikt zou worden door overheidsinstanties die momenteel niet beschikken over betrouwbare data over dergelijke parkeerplaatsen, wat beleidsvorming belemmert.

# Benodigdheden:
1. Conda 22.10+ of Miniconda (aanbevolen)
2. Python versie 3.10 of hoger
3. De juiste packages (Zie installeerguide)

# Package installatie
Check of conda geinstalleerd is door het volgende command te doen, dit zou: "conda 25.3.1" (Of een andere versie) moeten teruggeven:
- conda --version

Als dit geintalleerd is, run deze command om een conda enviroment op te zetten:
- conda create --name tygrongroep3 python=3.13

Open een nieuw terminal en activeer de conda enviroment:
- conda activate tygrongroep3

Zorg dat je met de terminal in de hoofdpaginafolder zit waar de enviroment.yaml inzit en download de packages uit de yml met:
- conda env update -n tygrongroep3 --file environment.yaml

# Hoe run ik de proof of concept
1. Zorg dat je in de hoofdfolder bent binnen je python omgeving.
2. Doe: "cd GUI" in de terminal, hiermee wordt gezorgd dat je in de goede folder zit
3. In de terminal, doe: "streamlit run GUI.py", hierna zal in de browser een server starten
4. Selecteer het gewenste model (Het model komt uit de model subfolder)
5. Selecteer de afbeelding waar de parkeerplaats op gedetecteerd moet worden.

# Hoe moet de code uitgevoerd worden
Instructies voor het instellen van de combinatie-overlay in Tygron
Volg onderstaande stappen om de benodigde combinatie-overlay correct in te stellen in het Tygron-platform:

1. Voorbereiding
Installeer het Tygron-platform via de officiële handleiding:
Installatiehandleiding - https://support.tygron.com/wiki/Install

Log in op het platform volgens deze instructies:
Inloghandleiding - https://support.tygron.com/wiki/Log_in

Maak een nieuw project aan met behulp van de wizard:
Nieuwe projectwizard - https://support.tygron.com/wiki/New_Project_Wizard

![file-U1jpjUX3pKGi5Lc4J3USBu](https://github.com/user-attachments/assets/4260fb9a-1b0f-4b59-bc24-10db21bc6990)

2. Toevoegen van overlays
Zodra je project is aangemaakt en je in de 3D-omgeving zit, ga je naar het tabblad "Overlays".

Voeg hier de overlay “Oorspronkelijke Satelliet” toe.

Voeg vervolgens een overlay van het type “Combinatie” toe.

3. Instellingen aanpassen
Voor beide overlays voer je de volgende instellingen door:

Gridgrootte aanpassen:
Zet de grid cell size op 0,25 m per pixel (te vinden onder het tabblad General).

![file-V86ysaPx2Qw8f6vfqz6LrZ](https://github.com/user-attachments/assets/84d5c65e-aeb5-4708-afdc-612c7a0b64d0)

4. Combinatie-overlay configureren
Open de Combinatie-overlay en ga naar het tabblad Input.

Stel onder Grid A de overlay “Oorspronkelijke Satelliet” in.

Klik onderin op “Select more Attributes or Grids” en kies daar het attribuut “Private_Yard” als Attribute A.

![image](https://github.com/user-attachments/assets/bf6cffe8-09b8-4944-a743-96d44d87b624)

5. Formule toevoegen
Ga naar het tabblad General van de combinatie-overlay.

Voeg onder Formula de volgende formule toe:
IF(GT(@A, 0), A, -2147483648)

![file-J5S1EUGwNxRGQjSMcAMFh5](https://github.com/user-attachments/assets/12b38b91-aacb-4886-b4a1-17fea07f6723)

6. Berekening uitvoeren
Klik op “Update Now” om de berekening toe te passen.














