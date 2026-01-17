# Medixio IA

## Objective

Medixio IA is a digital assistant designed to help individuals reliably manage their health-related schedules. The primary goal is to provide a secure and user-friendly platform for tracking medical appointments and medication regimens, thereby preventing missed appointments and ensuring adherence to treatment plans.

## Core Features (Phase 1)

*   **User Authentication:** Secure user registration and login.
*   **Appointment Management:** Create, view, update, and delete medical appointments.
*   **Medication Tracking:** Log prescribed medications, including dosage, instructions, and frequency.
*   **Reminder System:** Generate and manage reminders for both appointments and medication intake.

## Technology Stack

The backend for Medixio IA is being developed with the following technologies:

*   **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Programming Language:** Python 3.11+

## Project Structure

The project is organized into the following directories:

- **`app/`**: Contains the main application logic, including the FastAPI application and core configuration.
  - **`bot/`**: Holds the logic for the Telegram bot, including handlers for commands and messages.
  - **`core/`**: Core components of the application, such as configuration management.
- **`database/`**: Includes files related to the database, such as setup scripts and connection management.
- **`requirements/`**: Contains the project requirements, separated into different files for better organization.
- **`routes/`**: Defines the API endpoints for the different resources of the application.
- **`services/`**: Implements the business logic for each of the API endpoints.

