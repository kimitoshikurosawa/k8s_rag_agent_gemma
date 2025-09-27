from fastapi import FastAPI
from pydantic import BaseModel
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# --- 1. Configuration et chargement des modèles ---

# Définir les chemins et les noms des modèles
VECTOR_DB_PATH = "."  # Le dossier courant car le script est dans /app
INDEX_NAME = "vector_db"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "google/gemma-3-270m-it"

# Initialiser l'application FastAPI
app = FastAPI(
    title="RAG Agent API",
    description="API pour un agent IA spécialisé avec Gemma et RAG",
    version="1.0.0"
)

# Charger les modèles au démarrage de l'application pour éviter de les recharger à chaque requête
@app.on_event("startup")
def load_models():
    print("Chargement des modèles en cours...")
    
    # Charger le modèle d'embedding
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # Charger la base de données vectorielle
    db = FAISS.load_local(VECTOR_DB_PATH, embeddings, index_name=INDEX_NAME, allow_dangerous_deserialization=True)
    app.state.retriever = db.as_retriever(search_kwargs={"k": 3}) # "k": 3 récupère les 3 chunks les plus pertinents

    # Charger le tokenizer et le modèle LLM (Gemma)
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
    
    # Utiliser la quantification 4-bit pour réduire l'utilisation de la mémoire
    model = AutoModelForCausalLM.from_pretrained(
        LLM_MODEL_NAME,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        # load_in_4bit=True, # Décommenter si vous avez une carte NVIDIA compatible et les dépendances
    )

    # Créer un pipeline de génération de texte
    app.state.llm_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512
    )
    print("✅ Modèles chargés avec succès.")

# --- 2. Définition de la chaîne RAG (RAG Chain) ---

# Template de prompt pour guider le modèle
template = """
Tu es un assistant spécialisé. En te basant UNIQUEMENT sur le contexte suivant, réponds à la question de l'utilisateur de manière claire et concise.
Si l'information n'est pas dans le contexte, dis simplement : "Je ne dispose pas de cette information dans ma base de connaissances."

CONTEXTE:
{context}

QUESTION:
{question}

RÉPONSE:
"""
prompt_template = PromptTemplate.from_template(template)

def format_docs(docs):
    """Met en forme les documents récupérés pour les insérer dans le prompt."""
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    """Construit et retourne la chaîne de traitement RAG."""
    return (
        {"context": app.state.retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | app.state.llm_pipeline
        | (lambda outputs: outputs[0]['generated_text'].split("RÉPONSE:")[1].strip()) # Extraire uniquement la réponse générée
    )

# --- 3. Définition de l'API Endpoint ---

class Query(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_answer(query: Query):
    """
    Reçoit une question, la traite avec la chaîne RAG et retourne la réponse.
    """
    if not hasattr(app.state, 'retriever'):
        return {"error": "Les modèles ne sont pas encore chargés. Veuillez patienter."}

    rag_chain = get_rag_chain()
    answer = rag_chain.invoke(query.prompt)
    
    return {"answer": answer}

@app.get("/")
def read_root():
    return {"status": "API de l'agent RAG est en ligne"}