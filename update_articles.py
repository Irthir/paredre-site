import os
import pdfplumber

# Dossiers
PDF_DIR = "pdfs"
CONTENT_DIR = ""

def find_md_file(article_name):
    """Recherche récursivement un fichier Markdown correspondant au nom de l'article"""
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md") and os.path.splitext(file)[0] == article_name:
                return os.path.join(root, file)  # Retourne le chemin complet
    return None

# Liste des PDF
for pdf_file in os.listdir(PDF_DIR):
    if pdf_file.endswith(".pdf"):
        article_name = os.path.splitext(pdf_file)[0]  # Nom sans extension
        pdf_path = os.path.join(PDF_DIR, pdf_file)

        # Cherche le fichier .md correspondant
        md_path = find_md_file(article_name)
        
        if md_path:
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n\n".join([page.extract_text() or "" for page in pdf.pages])

            # Lire le fichier Markdown et conserver le front matter
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Vérifie si le texte est déjà ajouté (évite les doublons)
            if "---\n" in content:
                frontmatter, old_text = content.split("---\n", 1)
            else:
                frontmatter = content
                old_text = ""

            # Remplace l'ancien texte par le nouveau
            new_content = f"{frontmatter}---\n\n{text}"

            # Écriture du fichier Markdown mis à jour
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"✅ Contenu mis à jour pour : {md_path}")

        else:
            print(f"⚠️ Aucun fichier Markdown trouvé pour : {article_name}")

