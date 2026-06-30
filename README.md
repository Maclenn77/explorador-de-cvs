---
title: Explorador de CVs
emoji: 📚
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
pinned: false
---

# Explorador de CVs

El explorador de Cvs es un chatbot RAG + LLM para consultar CVs de candidatos. Carga archivos PDF y PNG, construye una base de conocimiento semántica y haz preguntas en lenguaje natural — sin necesidad de coincidencia de palabras clave.

**[▶ Probar la demo en vivo](https://huggingface.co/spaces/maclenn77/explorador-de-cvs) 

---

## Caso de uso: Descubrimiento de CVs para Reclutadores

Gestionar grandes volúmenes de CVs es difícil. Los reclutadores a menudo no conocen los nombres exactos de tecnologías o habilidades que buscar, y la búsqueda por palabras clave omite términos semánticamente equivalentes (por ejemplo, "machine learning" vs "aprendizaje automático", o experiencia en un framework análogo al requerido).

GnosisPages resuelve esto con recuperación semántica: un reclutador puede preguntar "¿Quién tiene experiencia con sistemas distribuidos y ha trabajado en startups?" y el sistema encuentra perfiles relevantes aunque la redacción exacta no coincida.

Los datos de los candidatos son sensibles (datos de contacto, historial personal). GnosisPages los mantiene privados por diseño: los documentos viven en una base de datos vectorial local o privada, y el LLM nunca se entrena con ellos — solo lee el contexto recuperado en el momento de inferencia.

La demo incluye una colección precargada de CVs sintéticos generados con Claude Sonnet 4.6 y vectorizados con `text-embedding-3-small` de OpenAI.

---

## Flujo de datos

```
Documentos PDF
      │
      ▼
  Extracción de texto (PyMuPDF)
      │
      ▼
  Segmentación (LangChain TextSplitter)
      │
      ▼
  Embeddings (text-embedding-3-small · OpenAI)
      │
      ▼
  Almacenamiento vectorial (ChromaDB)
      │
      ▼
  Consulta del usuario (lenguaje natural)
      │
      ├─► Embeber consulta ──► Búsqueda semántica (similitud coseno ChromaDB)
      │                               │
      │                         Top-k fragmentos
      │                               │
      └─────────────────► Construcción del prompt
                                      │
                                GPT-4o-Mini (LangChain)
                                      │
                              Respuesta → Interfaz Streamlit
```


## Arquitectura

### Aplicación

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9be08d2e-0c80-4dc5-8cbf-174eef28db59" />

### Ingesta de documentos

<img width="1416" height="974" alt="image" src="https://github.com/user-attachments/assets/ddc873b3-aaf7-4980-9173-bc5a3c966693" />

### Consulta de documentos

<img width="1416" height="940" alt="image" src="https://github.com/user-attachments/assets/e36714ac-d5c1-483a-85e0-5d5706f0299f" />

### Componentes

| Capa | Tecnología | Rol |
|---|---|---|
| UI | Streamlit 1.58 | Interfaz web y carga de archivos |
| Orquestación | LangChain 0.3 | Cadena RAG, gestión de prompts |
| Base vectorial | ChromaDB 1.5 | Almacenamiento y recuperación semántica |
| Embeddings | `text-embedding-3-small` (OpenAI) | Vectorización de documentos y consultas |
| LLM | GPT-4o-Mini (OpenAI) | Generación de respuestas |
| Parseo de PDF | PyMuPDF 1.24 | Extracción de texto de archivos PDF |

`text-embedding-3-small` reemplaza el modelo por defecto de ChromaDB (`all-MiniLM-L6-v2`) para mejor calidad semántica, especialmente con contenido en varios idiomas.

### Por qué GPT-4o-Mini

- Tiempos de respuesta rápidos para QA conversacional sobre contexto recuperado
- Menor costo por token que GPT-4o o GPT-4 Turbo
- Integración nativa con LangChain
- API estable de OpenAI sin infraestructura adicional

### Por qué RAG

La base de conocimiento es privada, dinámica y no puede incorporarse a los pesos del modelo. RAG proporciona acceso bajo demanda a documentos con los que el LLM nunca fue entrenado, sin exponerlos a servicios externos más allá del momento de la consulta.

---

## Funcionalidades

- **Carga de PDFs** de hasta 200 MB (creados programáticamente o procesados con OCR)
- **Búsqueda semántica** en tu colección de documentos — encuentra contenido relevante sin necesidad de coincidencias exactas de palabras clave
- **Interfaz conversacional** — haz preguntas de seguimiento en la misma sesión
- **Dataset precargado** — la demo incluye CVs sintéticos para que puedas probarlo de inmediato sin subir nada
- **Privado por diseño** — los documentos permanecen en tu base vectorial; el LLM solo ve los fragmentos recuperados

---

## Uso de la Demo

La demo en vivo en HuggingFace solo requiere una clave de API de OpenAI.

**Ejemplos de preguntas para probar con el dataset de CVs precargado:**

```
¿Quién tiene experiencia con Python y machine learning?
Encuentra candidatos que hayan trabajado en startups o empresas en etapas tempranas.
¿Quién tiene más experiencia en roles de liderazgo técnico?
¿Hay alguien con experiencia tanto en ingeniería de datos como en desarrollo backend?
¿Qué candidatos mencionan experiencia con infraestructura en la nube?
```

---

## Configuración Local

**Requisitos:** Python 3.11, clave de API de OpenAI

```bash
# 1. Clonar
git clone https://github.com/maclenn77/pdf-explainer.git
cd pdf-explainer

# 2. Crear archivo de entorno
touch .env
```

Agrega tu clave al archivo `.env`:

```
OPENAI_API_KEY=tu_clave_aqui
```

```bash
# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
streamlit run GnosisPages.py
```

---

## Despliegue

El repositorio incluye tres flujos de trabajo de GitHub Actions que se ejecutan en cada PR y despliegan automáticamente al hacer merge a `main`:

| Flujo de trabajo | Qué hace |
|---|---|
| Check file size | Bloquea merges con archivos que superen el límite de tamaño de HuggingFace |
| Check lints | Ejecuta `pylint` en el código fuente |
| Deploy to HuggingFace | Sube el último `main` al Space de HuggingFace |

Para desplegar tu propio fork, agrega estos secretos en la configuración de tu repositorio:

- `HF_TOKEN` — tu token de acceso a HuggingFace
- `HF_USERNAME` — tu nombre de usuario en HuggingFace

---

## Estructura del Proyecto

```
pdf-explainer/
├── GnosisPages.py          # Punto de entrada de la app
├── gnosis/
│   ├── chroma_client.py    # Wrapper de ChromaDB
│   ├── settings.py         # Bootstrap de la colección (carga la BD preconstruida)
│   ├── gui_messages.py     # Textos de la UI
│   └── components/
│       ├── sidebar.py      # Carga de archivos y controles de BD
│       └── main.py         # Interfaz de chat y cadena RAG
├── pages/                  # Páginas adicionales de Streamlit
├── requirements.txt
├── Dockerfile
└── .github/workflows/      # CI/CD
```

---

## Licencia

MIT — ver [LICENSE](LICENSE) para más detalles.
