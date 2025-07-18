\# Modrinth Mod Downloader



A GUI application to download files from a Modrinth `.mrpack` file, with an option to download only server-side mods.



\## Features

\- Select a `.mrpack` file and an output directory.

\- Option to download only server-side mods (`.jar` files in `mods/`) or all files (including `resourcepacks/` and `shaderpacks/`).

\- Progress bar and log display for tracking downloads.

\- Bilingual interface (French if system language is French, English otherwise).



\## Usage

1\. Install Python 3.x and dependencies:

&nbsp;  ```bash

&nbsp;  pip install -r requirements.txt

&nbsp;  ```

2\. Run the script:

&nbsp;  ```bash

&nbsp;  python src/modrinth\_mod\_downloader.py

&nbsp;  ```

3\. Select a `.mrpack` file and a destination folder.

4\. Check "Download server-side mods only" (or equivalent in French) to download only mods, or uncheck to download all files.

5\. Click "Download files" (or equivalent in French) to start the download.

6\. Monitor the progress bar and log for download status.



\## Language Support

\- The interface automatically displays in French if your system language is set to French (e.g., `fr\_FR`, `fr\_CA`).

\- Otherwise, it displays in English.



\## Prerequisites

\- Python 3.x

\- Install dependencies:

&nbsp; ```bash

&nbsp; pip install -r requirements.txt

&nbsp; ```



\## Project Structure

```

modrinth-mod-downloader/

├── src/

│   ├── modrinth\_mod\_downloader.py

├── requirements.txt

├── .gitignore

├── README.md

```



\## License

MIT License

