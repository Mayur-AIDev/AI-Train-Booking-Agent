# 🚂 AI-Driven Train Ticket Booking Agent

A production-grade, multi-turn AI Assistant built to automate train search queries and ticket seat bookings. This project showcases advanced AI engineering practices by using a state-machine graph framework for context continuity, wrapped in an asynchronous REST API, and delivered via an interactive web interface.

## 🚀 Core Tech Stack
* **Orchestration & State Management:** LangGraph (with `MemorySaver` checkpointer for thread persistence)
* **LLM Engine:** Qwen-2.5-7B-Instruct (via Hugging Face API Integration)
* **Backend Application Server:** FastAPI (Asynchronous REST API endpoints)
* **Frontend UI Dashboard:** Streamlit (Features a dual-column layout for live slot tracking visualization)
* **Data Persistence Layer:** Custom Python File-System Operations (`train_db.json`)

---

## 🏗️ Architecture Design Flow

