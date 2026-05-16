# AI Assistant

A small Flask web app that turns a stack of PDFs into a grounded question-answering chatbot, with an optional voice loop. Upload a few documents, ask a question in the browser (or speak it), and the assistant retrieves the most relevant passage from your PDFs and asks GPT-3.5 to answer using only that passage.

Built September 2023 as a focused exercise in retrieval-augmented generation before "RAG" was the default acronym in every tutorial. Kept here as a reference implementation of the core loop without the framework weight of LangChain or LlamaIndex.

## Why this exists

I wanted to see how far a deliberately minimal RAG stack could go for a single domain:

- Plain `PyPDF2` for ingest.
- `scikit-learn` `TfidfVectorizer` plus cosine similarity for retrieval (no vector DB).
- A tightly-scoped system prompt that refuses to answer from outside the supplied passage.
- A Flask front-end with a chat widget and a "human-like typing" effect on the response.

An optional path uses `sentence-transformers` plus FAISS for dense retrieval, with a similarity check that verifies the model's answer is actually grounded in the source text before returning it (see `retrieval_from_embeddings.py`).

The voice loop (`SpeechRecognition` + `pyttsx3`) is included but commented out in the main flow, because the web UI ended up being the more useful surface.

## Architecture

```
PDF(s) ──> PDFProcessor ──> sentence list
                                 │
                                 ▼
                     TfidfVectorizer.fit_transform
                                 │
                                 ▼
   user question ──> cosine_similarity ──> best-match passage
                                                 │
                                                 ▼
                       OpenAI Chat Completions (gpt-3.5-turbo)
                       system prompt: "use only this passage"
                                                 │
                                                 ▼
                              answer ──> Flask UI / pyttsx3 TTS
```

Files:

- `app.py`: Flask routes (`/`, `/chat`, `/upload`).
- `assistant.py`: Orchestrator that wires PDF ingest, retrieval, and chat.
- `pdf_processor.py`: Extracts and tokenises PDF text into sentences.
- `chatbot.py`: TF-IDF retrieval plus OpenAI Chat Completions call.
- `audio_processor.py`: `speech_recognition` (Google Web Speech API) for STT, `pyttsx3` (SAPI5 voice) for TTS.
- `retrieval_from_embeddings.py`: Alternate path using `sentence-transformers` embeddings, FAISS index, and a grounding-verification step.
- `templates/index.html`, `static/`: Flask UI plus a small chat widget.

## Tech

| Layer | Choice |
| --- | --- |
| Web | Flask, Jinja templates, vanilla JS |
| Ingest | PyPDF2 |
| Retrieval (default) | scikit-learn TF-IDF + cosine similarity |
| Retrieval (alt) | sentence-transformers (`paraphrase-distilroberta-base-v1`) + FAISS |
| LLM | OpenAI `gpt-3.5-turbo` via REST |
| STT (optional) | `SpeechRecognition` with Google Web Speech backend |
| TTS (optional) | `pyttsx3` (Windows SAPI5) |

## Quickstart

Requires Python 3.10+ and an OpenAI API key. The voice features additionally require system audio libraries (see below).

```bash
git clone https://github.com/dparikh79/AI-Assistant.git
cd AI-Assistant

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install flask PyPDF2 scikit-learn requests \
            SpeechRecognition pyttsx3 gTTS \
            sentence-transformers faiss-cpu
```

Create `secrets.json` in the project root (it is gitignored):

```json
{
  "API_ENDPOINT": "https://api.openai.com/v1/chat/completions",
  "API_KEY": "sk-your-openai-key"
}
```

Edit `config.py` to point `PATH_TO_BOOK` at your own PDFs, or leave the list empty and upload PDFs through the web UI at runtime.

Run the web app:

```bash
python app.py
# open http://127.0.0.1:5000
```

Or run the terminal-only loop (no Flask):

```bash
python assistant.py
```

### Audio dependencies (only if you enable the voice loop)

- macOS: `brew install portaudio` then `pip install pyaudio`.
- Debian/Ubuntu: `sudo apt-get install portaudio19-dev espeak ffmpeg` then `pip install pyaudio`.
- Windows: `pyttsx3` uses SAPI5 out of the box; `pip install pyaudio` usually works on recent Python builds.

The voice calls are commented out in `assistant.py::main`. Uncomment the `AudioProcessor.text_to_speech(...)` and `AudioProcessor.voice_to_text()` lines to switch from typed input to spoken input.

## Known limits

This is a 2023-era sketch, not a product. Worth being upfront about what it is and is not:

- TF-IDF retrieval over sentence splits is fast but brittle on long, multi-page reasoning. The FAISS path in `retrieval_from_embeddings.py` is better but not wired into the Flask app.
- `pyttsx3` is initialised with `sapi5`, so out-of-the-box TTS is Windows-only. On macOS or Linux, swap the driver (`nsss` or `espeak`) in `audio_processor.py`.
- The Google Web Speech backend used by `SpeechRecognition` is undocumented and unsuitable for production. A modern rewrite would use Whisper (local) or the OpenAI audio API.
- No wake word, no OS control (no app launching, no web search). It is a grounded Q&A loop, not a Siri replacement.
- Bare `requests.post` to OpenAI with no retry/backoff and no streaming; a `try/except` swallows errors and prints to stdout.
- The `app.secret_key` in `app.py` is a placeholder. Set it from an environment variable before exposing the app to anyone other than yourself.

## What I would change today

If I rebuilt this in 2026 I would: swap PyPDF2 for `pypdf` or `unstructured`; replace TF-IDF with a small embedding model and an actual vector store; move the OpenAI call to the official SDK with streaming and structured output; use Whisper for STT; and put the grounding check from `retrieval_from_embeddings.py` in front of every answer, not just the alternate path.

## License

MIT. See [LICENSE](LICENSE).
