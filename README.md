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

# Hoe installeer ik Miniconda:
1. Ga naar de officiele Miniconda downloadpagina: https://www.anaconda.com/download/success
2. Download het installatieprogramma dat overeenkomt met jouw besturingssysteem (Windows, macOS of Linux). 
3. Voer het installatieprogramma uit, Dubbelklik op het gedownloade bestand om het installatieprogramma te starten. 
4. Volg de instructies, Het installatieprogramma zal je door het installatieproces leiden. Je kiest een installatielocatie en voegt de conda paden toe aan je shell. 
5. Test de installatie, Om te controleren of Miniconda correct is geïnstalleerd, open je een nieuw terminalvenster en voer je de opdracht conda list uit. Als de installatie is gelukt, zie je een lijst met geïnstalleerde pakketten. 

# Hoe installeer ik Python: (Versie 3.10 of hoger)
1. Ga naar de Python website: Bezoek de officiële Python downloadpagina: https://www.python.org/downloads/ 
2. Download de installer: Selecteer de juiste installer voor jouw besturingssysteem (Windows, macOS, of Linux) en download deze. 
3. Start de installatie: Open het gedownloade bestand en volg de instructies op het scherm. 
4. Voeg Python toe aan PATH: Zorg ervoor dat je de optie "Add Python to PATH" (of een vergelijkbare optie) aanvinkt tijdens de installatie. Dit maakt het mogelijk om Python vanuit de command line of terminal te gebruiken. 
5. Voltooi de installatie: Klik op "Install" en wacht tot de installatie is voltooid. 
6. Controleer de installatie: Open een command prompt (Windows) of terminal (macOS/Linux) en typ "python --version". Als Python correct is geïnstalleerd, zie je de versie informatie. 

# Package installatie
Check of conda geinstalleerd is door het volgende command te doen, dit zou: "conda 25.3.1" (Of een andere versie) moeten teruggeven:
- conda --version

Als dit geintalleerd is, run deze command om een conda enviroment op te zetten:
- conda create --name tygrongroep3 python=3.13

Open een nieuw terminal en activeer de conda enviroment:
- conda activate tygrongroep3

Zorg dat je met de terminal in de hoofdpaginafolder zit waar de enviroment.yaml inzit en download de packages uit de yml met:
- conda env update -n tygrongroep3 --file environment.yaml

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














