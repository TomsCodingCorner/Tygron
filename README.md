# Tygron
Groep 3 Tygron DLP door Ties, Tom en Elijah

# GitHub Workflow – Tygron Team

## Branch Structuur
- `main` → stabiele productiecode (nooit direct aan werken)
- `dev` → gezamenlijke ontwikkelbranch 
- `feature/...` → voor nieuwe functionaliteiten (elke feature heeft zijn eigen branc)
- `bugfix/...` → voor specifieke fouten.

## Nieuwe branch maken (iedereen MOET dit volgen)
1. git fetch origin (Pakt alle branches)
2. git checkout dev (Verlaat de main branch en ga naar de dev branch)
3. git pull origin dev (Pak de meest recente versie)
4. git checkout -b feature/NAAM_HIER (Maak nu je eigen branch aan IN de dev branch voor de specifieke feature die je gaat bouwen.)

## Commit regels
✅ Wel doen:
- Commit tekst: Geef een duidelijke beknopte uitleg weat je hebt gedaan binnen die commit
- Commit met regelmaat!
- feat: voegt login toe
- fix: repareert fout bij dataload
- docs: beschrijft workflow in README

## Werkwijze
- Maak een branch vanaf dev
- Codeer op je eigen branch als er conflicts kunnen komen door op dezelfde branche te werken
- Commit & push
- Maak een Pull Request naar dev
- Laat je code reviewen
- Merge na goedkeuring Werkwijze

## Voorbeeld pushen
git status                      # Check of je op je eigen branch werkt, er moet staan feature/(jouw feature naam) NIET MAIN of DEV. 
git add README.md               # Voeg toe wat je wil opslaan
git commit -m "docs: beschrijft git workflow in README"
git push -u origin feature/update-readme
