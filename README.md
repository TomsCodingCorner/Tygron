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

Activeer de enviroment:
- conda activate tygrongroep3

Zorg dat je met de terminal in de hoofdpaginafolder zit waar de enviroment.yaml inzit en download de packages uit de yml met:
- conda env update -n tygrongroep3 --file enviroment.yaml

# Hoe moet de code uitgevoerd worden























