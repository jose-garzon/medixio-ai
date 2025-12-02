# Feature: Medical Appointment Management

## 1. Description
The system allows the patient to schedule, track, and be reminded of medical appointments. The user can enter the information by typing a message or sending a photo of the medical order.

## 2. User Requirements (User Stories)
* **US-C1:** As a patient, I want to send a **photo of my medical order** so the AI automatically extracts the date, time, doctor, and specialty.
* **US-C2:** As a patient, I want to **write in natural language** (e.g., "Appointment with the dermatologist on Tuesday at 3 pm") to quickly schedule.
* **US-C3:** As a patient, I want to receive a **confirmation request** with the data understood by the AI before saving the appointment.
* **US-C4:** As a patient, I want to receive **automatic reminders** when my appointment is approaching.

## 3. Functional Flow
1.  **Input:** User sends Text or Image to the bot.
2.  **Interpretation:** Gemini analyzes the input.
    * If data is missing (e.g., no time), the AI must infer or flag it as pending.
3.  **Confirmation:** The bot responds with a summary:
    * "Detected appointment with: Cardiology. Date: 10/15/2023 15:00. Confirm?"
    * Buttons: [Confirm] [Cancel].
4.  **Persistence:** Upon confirmation, it is saved in SQLite with `CONFIRMED` status.

## 4. Technical Requirements
### Data Model (Appointment)
* `id`: Integer (PK).
* `user_id`: Integer (FK).
* `specialty`: String (e.g., Cardiology).
* `doctor_name`: String (Optional).
* `date_time`: DateTime.
* `location`: String (Optional).
* `status`: String Enum (`PLACEHOLDER`, `CONFIRMED`, `COMPLETED`, `CANCELLED`).
* `raw_text`: String (The original text or image description for reference).

### Business Rules
* **AI Extraction:** Use `instructor` with a Pydantic model that forces the extraction of `ISO 8601` formatted date fields.
* **Notifications (Scheduler):**
    * Recurring job (every 15 min or 1 hour).
    * Reminder 1: 24 hours before.
    * Reminder 2: 1 hour before.