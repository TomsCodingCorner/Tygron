# Tygron
Groep 3 Tygron DLP door Ties, Joel, Tom en Elijah

# GitHub Workflow – Tygron Team

## Branch Structuur
- `main` → stabiele productiecode (nooit direct aan werken)
- `dev` → gezamenlijke ontwikkelbranch 
- `feature/...` → voor nieuwe functionaliteiten (elke feature heeft zijn eigen branc)
- `bugfix/...` → voor specifieke fouten.

## Nieuwe branch maken (iedereen MOET dit volgen)
git fetch origin (Pakt alle branches)
git checkout dev (Verlaat de main branch en ga naar de dev branch)
git pull origin dev (Pak de meest recente versie)
git checkout -b feature/NAAM_HIER (Maak nu je eigen branch aan IN de dev branch voor de specifieke feature die je gaat bouwen.)

## Commit regels
❌ Niet doen: 
update, nieuwe versie, shit gefixt

✅ Wel doen:

feat: voegt login toe

fix: repareert fout bij dataload

docs: beschrijft workflow in README

## Werkwijze
Maak een branch vanaf dev

Codeer op je eigen branch

Commit & push

Maak een Pull Request naar dev

Laat je code reviewen

Merge na goedkeuringWerkwijze

## Voorbeeld pushen

git status                      # Check of je op je eigen branch werkt, er moet staan feature/(jouw feature naam) NIET MAIN of DEV. 
git add README.md               # Voeg toe wat je wil opslaan
git commit -m "docs: beschrijft git workflow in README"
git push -u origin feature/update-readme
