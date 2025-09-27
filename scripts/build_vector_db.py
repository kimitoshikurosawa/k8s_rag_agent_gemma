import os
import glob
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Définir les chemins des dossiers
KNOWLEDGE_BASE_DIR = "../knowledge_base"
VECTOR_DB_PATH = "../app"

def build_vector_database():
    """
    Crée une base de données vectorielle à partir des documents
    présents dans le dossier knowledge_base.
    """
    print("Démarrage de la création de la base de données vectorielle...")

    # 1. Charger les documents depuis le dossier knowledge_base
    # Nous utilisons glob pour trouver tous les fichiers .md
    md_files = glob.glob(os.path.join(KNOWLEDGE_BASE_DIR, "*.md"))
    documents = []
    for file_path in md_files:
        loader = TextLoader(file_path, encoding='utf-8')
        documents.extend(loader.load())
    
    if not documents:
        print("Aucun document trouvé. Vérifiez le chemin du dossier knowledge_base.")
        return

    print(f"{len(documents)} document(s) chargé(s).")

    # 2. Découper les documents en morceaux (chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    print(f"Les documents ont été découpés en {len(docs)} morceaux (chunks).")

    # 3. Créer les embeddings
    # Nous utilisons un modèle open-source léger et performant.
    # Le modèle sera téléchargé automatiquement lors de la première exécution.
    print("Création des embeddings... (cela peut prendre quelques minutes au premier lancement)")
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    # 4. Créer la base de données vectorielle avec FAISS et y stocker les documents et embeddings
    db = FAISS.from_documents(docs, embeddings)

    # 5. Sauvegarder la base de données localement
    # Le fichier d'index sera utilisé par notre application FastAPI.
    db.save_local(VECTOR_DB_PATH, index_name="vector_db")

    print("-" * 80)
    print(f"✅ Base de données vectorielle créée et sauvegardée avec succès dans le dossier '{VECTOR_DB_PATH}'.")
    print("-" * 80)

if __name__ == "__main__":
    build_vector_database()