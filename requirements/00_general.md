# Medixio-AI: General Vision and Architecture

## 1. Project Description
Medixio-AI is an intelligent medical assistant built on Telegram, designed to help patients with chronic illnesses or disabilities. Its main goal is to reduce the mental burden of administrative health management.

**MVP Goal:** Validate the AI's capability to interpret unstructured medical data (photos of prescriptions, medical orders, or free text) and convert them into structured records for appointments and medication supply tracking.

## 2. Technology Stack
* **Language:** Python 3.10+
* **Backend Framework:** FastAPI (Handling lifecycle and future APIs).
* **User Interface:** Telegram Bot API (using the `aiogram` asynchronous library).
* **Database:** SQLite (local file `medixio.db`).
* **ORM:** SQLModel (Native Async + Pydantic support).
* **AI Engine:** Google Gemini Flash.
* **AI Processing:** `instructor` library to ensure structured JSON output.
* **Background Tasks:** APScheduler (for reminders and inventory checks).

## 3. Architectural Principles
1.  **Async First:** All I/O operations (Database, Telegram API calls, Gemini calls) must be asynchronous (`async/await`).
2.  **Ephemeral Image Privacy:** Images sent by the user are processed in RAM to extract data and discarded immediately. They are not saved to disk or cloud storage.
3.  **Bot State:** The use of complex state machines (FSM) will be minimized. The prioritized flow is: **Input -> AI -> Confirmation -> Persistence**.

## 4. Database Structure (Global)
The system uses a simple relational database.
* **User:** Patient identification linked to their Telegram ID.
* **Appointment:** Medical appointments.
* **MedicationInventory:** Medication supply control.