Modrinth Mod Downloader

A GUI application to download files from a Modrinth .mrpack file, with an option to download only server-side mods.

Features



Select a .mrpack file and an output directory.

Option to download only server-side mods (.jar files in mods/) or all files (including resourcepacks/ and shaderpacks/).

Progress bar and log display for tracking downloads.

Bilingual interface (French if system language is French, English otherwise).



Usage



Install Python 3.x and dependencies:pip install -r requirements.txt





Run the script:python src/modrinth\_mod\_downloader.py





Select a .mrpack file and a destination folder.

Check "Download server-side mods only" (or equivalent in French) to download only mods, or uncheck to download all files.

Click "Download files" (or equivalent in French) to start the download.

Monitor the progress bar and log for download status.



Language Support



The interface automatically displays in French if your system language is set to French (e.g., fr\_FR, fr\_CA).

Otherwise, it displays in English.



Prerequisites



Python 3.x

Install dependencies:pip install -r requirements.txt







Project Structure

modrinth-mod-downloader/

├── src/

│   ├── modrinth\_mod\_downloader.py

├── requirements.txt

├── .gitignore

├── README.md



License

MIT License

