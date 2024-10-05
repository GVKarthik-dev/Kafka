# Chat Messaging Application with FastAPI and Kafka

This is a messaging application built using **FastAPI** for the backend, **Kafka** for real-time messaging, and **SQLite** for persistent data storage. It includes user authentication with JWT tokens, message sending, and real-time message consumption via WebSocket.

## Features

- User Authentication (JWT-based)
- Send and receive messages
- Store messages in an SQLite database
- Real-time messaging using Kafka and WebSockets
- Mark messages as read after consumption

## Technologies Used

- FastAPI
- SQLite (SQLAlchemy ORM)
- Kafka (for message brokering)
- Pydantic (for data validation)
- OAuth2 (for authentication)
- WebSockets (for real-time messaging)

## Prerequisites

To run this project, ensure you have the following installed:

- Python 3.10+
- Kafka server
- Docker (optional, for containerization)
