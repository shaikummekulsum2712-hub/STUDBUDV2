# Document-Based Q&A Assistant (RAG System)

An end-to-end Retrieval-Augmented Generation (RAG) web application that enables users to upload PDF and text documents, perform semantic vector search, and receive accurate, natural-language answers grounded strictly in the uploaded content.

---

## 📌 Project Overview

This project implements a practical document-based Q&A assistant built to demonstrate key LLM engineering principles:
* **Grounding:** Answers are generated using retrieved context rather than relying solely on parametric model memory.
* **Context Visibility:** The UI displays synthesized answers alongside raw retrieved chunks for full transparency and verification.
* **Efficient Ingestion:** Automatic text extraction, chunking, embedding generation, and vector indexing.

---

## ⚡ Key Features

* **Multi-Format Ingestion:** Supports uploading `.pdf` and `.txt` files.
* **Smart Text Chunking:** Implements recursive text splitting with configurable chunk sizes and overlaps to preserve semantic continuity.
* **Vector Similarity Search:** Uses dense embeddings and a vector database to fetch top-$k$ relevant text passages per query.
* **Grounded Synthesis:** System prompt guardrails ensure the LLM answers strictly using retrieved context without hallucinating external facts.
* **Source Transparency:** Dedicated context panel allowing users to inspect raw source snippets and similarity scores.
* **Error & Edge Case Handling:** Robust handling for empty uploads, unparseable documents, and out-of-context queries.

---

## 🏗️ Architecture & Pipeline

```text
               ┌───────────────────────┐
               │  Uploaded PDF / TXT   │
               └───────────┬───────────┘
                           │
                           v
               ┌───────────────────────┐
               │   Document Loader     │
               └───────────┬───────────┘
                           │
                           v
               ┌───────────────────────┐
               │  Recursive Chunking   │
               │  (1000 char / 200 overlap)
               └───────────┬───────────┘
                           │
                           v
               ┌───────────────────────┐
               │ Embeddings Generation │
               └───────────┬───────────┘
                           │
                           v
               ┌───────────────────────┐
               │ Vector Store (FAISS)  │
               └───────────┬───────────┘
                           │
 User Query ───────────────┼───────────────┐
                           │               │
                           v               │
               ┌───────────────────────┐   │
               │ Top-k Similarity Search │  │
               └───────────┬───────────┘   │
                           │               │
                           v               │
               ┌───────────────────────┐   │
               │ Context + User Query  │◄──┘
               └───────────┬───────────┘
                           │
                           v
               ┌───────────────────────┐
               │   LLM Synthesizer     │
               └───────────┬───────────┘
                           │
                           v
               ┌───────────────────────┐
               │ Grounded Answer + UI  │
               └───────────────────────┘
