# Feature: Medication Inventory (Supply Tracking)

## 1. Description
Inventory management system for chronic patients. It is not a daily "take your pill" alarm, but an assistant that manages the **monthly resupply** of recurring medications.

## 2. User Requirements (User Stories)
* **US-M1:** As a patient, I want to register a medication by indicating the dosage and the **total duration of the treatment** (e.g., "3 months") so the system calculates how many boxes I need.
* **US-M2:** As a patient, I want to **upload a photo of the prescription** to create my monthly shopping list.
* **US-M3:** As a patient, I want to receive an **alert a few days before** my monthly supply runs out so I can go to the pharmacy on time.
* **US-M4:** As a patient, I want a button to confirm "I've already bought the medicine" so the system recalculates the next purchase date.

## 3. Functional Flow
1.  **Input:** "Take Atorvastatin 20mg, one every night for 6 months."
2.  **AI/Backend Calculation:**
    * Frequency: 1 daily.
    * Total Duration: 6 months.
    * Monthly Supply: 30 pills (approx).
    * Renewal Dates: Today + 30 days, Today + 60 days, etc.
3.  **Registration:** The active medication is saved.
4.  **Lifecycle:**
    * The system monitors the `next_renewal_date`.
    * 3 days before, it sends an alert.
    * User confirms purchase -> `next_renewal_date` is updated by +30 days.
    * If the total duration is met (6 months), the medication moves to `ARCHIVED` status.

## 4. Technical Requirements
### Data Model (MedicationSupply)
* `id`: Integer (PK).
* `user_id`: Integer (FK).
* `name`: String (Commercial/generic name).
* `dosage_instructions`: String (e.g., "1 every 8 hours").
* `total_duration_months`: Integer (Total duration of treatment).
* `start_date`: Date (Start date).
* `next_renewal_date`: Date (Critical date for notification).
* `status`: String Enum (`ACTIVE`, `FINISHED`, `PAUSED`).

### Business Rules
* **Date Calculation:** The AI must extract the duration and frequency, but the calculation of the renewal date (`next_renewal_date`) must be done in **Python** (deterministic logic) to avoid hallucinations of distant future dates.
* **Notifications:**
    * Daily job (e.g., 09:00 AM).
    * Query: `SELECT * FROM medications WHERE next_renewal_date <= (TODAY + 3 days)`.