import os
import pdfplumber

# Dossiers
PDF_DIR = "static/pdfs"
POSTS_DIR = "content/posts"

# Liste tous les fichiers Markdown
for md_file in os.listdir(POSTS_DIR):
    if md_file.endswith(".md"):
        article_name = os.path.splitext(md_file)[0]  # Nom sans extension
        pdf_path = os.path.join(PDF_DIR, f"{article_name}.pdf")
        md_path = os.path.join(POSTS_DIR, md_file)

        # Vérifie si le fichier PDF correspondant existe
        if os.path.exists(pdf_path):
            with pdfplumber.open(pdf_path) as pdf:
                text = "\n\n".join([page.extract_text() or "" for page in pdf.pages])

            # Lire le fichier Markdown et conserver le frontmatter
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

            print(f"✅ Contenu mis à jour pour : {md_file}")

        else:
            print(f"⚠️ Aucun PDF trouvé pour : {md_file}")
