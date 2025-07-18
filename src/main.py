#Made by Xerty


import json
import os
import requests
import zipfile
import customtkinter as ctk
from tkinter import filedialog, messagebox
from urllib.parse import unquote
import tempfile
import locale

class ModDownloaderApp:
    def __init__(self, root):
        self.root = root
        
        # Détecter la langue du système
        system_locale = locale.getlocale()[0]
        self.language = "fr" if system_locale and system_locale.startswith("fr") else "en"

        # Dictionnaire de traductions
        self.translations = {
            "fr": {
                "title": "Téléchargeur de Mods Modrinth",
                "mrpack_label": "Fichier .mrpack :",
                "choose_mrpack": "Choisir .mrpack",
                "output_label": "Dossier de destination :",
                "choose_output": "Choisir dossier",
                "server_only": "Télécharger uniquement les mods côté serveur",
                "download_button": "Télécharger les fichiers",
                "log_label": "Journal :",
                "mrpack_selected": "Fichier .mrpack sélectionné : {path}",
                "output_selected": "Dossier de destination sélectionné : {path}",
                "no_mrpack_error": "Veuillez sélectionner un fichier .mrpack",
                "no_output_error": "Veuillez sélectionner un dossier de destination",
                "no_files_info": "Aucun fichier trouvé dans le fichier .mrpack",
                "download_start": "Téléchargement de {file}...",
                "download_success": "{file} téléchargé avec succès.",
                "download_fail": "Échec du téléchargement de {file} (code {code}).",
                "download_error": "Erreur lors du téléchargement de {file} : {error}",
                "download_complete": "Téléchargement terminé !",
                "processing_error": "Erreur lors du traitement : {error}",
                "success_message": "Téléchargement des fichiers terminé !"
            },
            "en": {
                "title": "Modrinth Mod Downloader",
                "mrpack_label": "Modrinth .mrpack file:",
                "choose_mrpack": "Choose .mrpack",
                "output_label": "Destination folder:",
                "choose_output": "Choose folder",
                "server_only": "Download server-side mods only",
                "download_button": "Download files",
                "log_label": "Log:",
                "mrpack_selected": "Selected .mrpack file: {path}",
                "output_selected": "Selected destination folder: {path}",
                "no_mrpack_error": "Please select a .mrpack file",
                "no_output_error": "Please select a destination folder",
                "no_files_info": "No files found in the .mrpack file",
                "download_start": "Downloading {file}...",
                "download_success": "{file} downloaded successfully.",
                "download_fail": "Failed to download {file} (code {code}).",
                "download_error": "Error downloading {file}: {error}",
                "download_complete": "Download completed!",
                "processing_error": "Error during processing: {error}",
                "success_message": "File download completed!"
            }
        }

        # Configurer la fenêtre
        self.root.title(self.translations[self.language]["title"])
        self.root.geometry("600x500")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variables
        self.mrpack_path = ctk.StringVar()
        self.output_dir = ctk.StringVar()
        self.progress = ctk.DoubleVar()
        self.server_only = ctk.BooleanVar(value=True)  # Par défaut, ne télécharger que les mods serveur

        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Titre
        ctk.CTkLabel(self.root, text=self.translations[self.language]["title"], font=("Arial", 16, "bold")).pack(pady=10)

        # Sélection du fichier .mrpack
        ctk.CTkLabel(self.root, text=self.translations[self.language]["mrpack_label"]).pack(pady=5)
        ctk.CTkEntry(self.root, textvariable=self.mrpack_path, width=400, state="readonly").pack(pady=5)
        ctk.CTkButton(self.root, text=self.translations[self.language]["choose_mrpack"], command=self.select_mrpack).pack(pady=5)

        # Sélection du dossier de destination
        ctk.CTkLabel(self.root, text=self.translations[self.language]["output_label"]).pack(pady=5)
        ctk.CTkEntry(self.root, textvariable=self.output_dir, width=400, state="readonly").pack(pady=5)
        ctk.CTkButton(self.root, text=self.translations[self.language]["choose_output"], command=self.select_output_dir).pack(pady=5)

        # Case à cocher pour les mods serveur uniquement
        ctk.CTkCheckBox(self.root, text=self.translations[self.language]["server_only"], variable=self.server_only).pack(pady=10)

        # Bouton de téléchargement
        ctk.CTkButton(self.root, text=self.translations[self.language]["download_button"], command=self.download_mods).pack(pady=20)

        # Barre de progression
        ctk.CTkProgressBar(self.root, variable=self.progress, width=400).pack(pady=10)

        # Journal
        ctk.CTkLabel(self.root, text=self.translations[self.language]["log_label"]).pack(pady=5)
        self.log_text = ctk.CTkTextbox(self.root, width=500, height=150)
        self.log_text.pack(pady=5)

    def select_mrpack(self):
        file_path = filedialog.askopenfilename(filetypes=[("Modrinth Pack", "*.mrpack")])
        if file_path:
            self.mrpack_path.set(file_path)
            self.log_text.insert("end", self.translations[self.language]["mrpack_selected"].format(path=file_path) + "\n")

    def select_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir.set(dir_path)
            self.log_text.insert("end", self.translations[self.language]["output_selected"].format(path=dir_path) + "\n")

    def download_mods(self):
        if not self.mrpack_path.get():
            messagebox.showerror("Error", self.translations[self.language]["no_mrpack_error"])
            return
        if not self.output_dir.get():
            messagebox.showerror("Error", self.translations[self.language]["no_output_error"])
            return

        # Créer le dossier de destination s'il n'existe pas
        os.makedirs(self.output_dir.get(), exist_ok=True)

        try:
            # Extraire modrinth.index.json du fichier .mrpack
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(self.mrpack_path.get(), 'r') as zip_ref:
                    zip_ref.extract("modrinth.index.json", temp_dir)
                
                json_path = os.path.join(temp_dir, "modrinth.index.json")
                with open(json_path, "r") as file:
                    data = json.load(file)

                # Filtrer les fichiers selon la case à cocher
                if self.server_only.get():
                    files = [f for f in data["files"] if f["path"].startswith("mods/")]
                else:
                    files = data["files"]

                total_files = len(files)
                if total_files == 0:
                    messagebox.showinfo("Info", self.translations[self.language]["no_files_info"])
                    return

                self.progress.set(0)
                for i, file_entry in enumerate(files, 1):
                    file_path = file_entry["path"]
                    download_url = file_entry["downloads"][0]
                    file_name = unquote(os.path.basename(download_url))
                    destination_path = os.path.join(self.output_dir.get(), file_name)

                    self.log_text.insert("end", self.translations[self.language]["download_start"].format(file=file_name) + "\n")
                    self.log_text.see("end")
                    self.root.update()

                    try:
                        response = requests.get(download_url, stream=True)
                        if response.status_code == 200:
                            with open(destination_path, "wb") as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                            self.log_text.insert("end", self.translations[self.language]["download_success"].format(file=file_name) + "\n")
                        else:
                            self.log_text.insert("end", self.translations[self.language]["download_fail"].format(file=file_name, code=response.status_code) + "\n")
                    except Exception as e:
                        self.log_text.insert("end", self.translations[self.language]["download_error"].format(file=file_name, error=str(e)) + "\n")

                    # Mettre à jour la barre de progression
                    self.progress.set(i / total_files)
                    self.root.update()

                self.log_text.insert("end", self.translations[self.language]["download_complete"] + "\n")
                self.log_text.see("end")
                messagebox.showinfo("Success", self.translations[self.language]["success_message"])

        except Exception as e:
            messagebox.showerror("Error", self.translations[self.language]["processing_error"].format(error=str(e)))

if __name__ == "__main__":
    root = ctk.CTk()
    app = ModDownloaderApp(root)
    root.mainloop()