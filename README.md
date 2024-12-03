# CS 440 Microservices Project

A microservices-based book review system that demonstrates key microservices architecture patterns.

## Services

- Book Service (Port 5001): Manages book data
- Review Service (Port 5002): Handles book reviews
- Web Interface (Port 3000): Provides user interface
- API Gateway (Port 4000): Routes API requests

## Running the Project

1. Ensure Docker and Docker Compose are installed
2. Clone the repository
3. Run: `docker-compose up --build`
4. Access the web interface at http://localhost:3000
5. API endpoints available at http://localhost:4000/api/*

## Architecture

Each service is containerized and manages its own SQLite database. The API Gateway provides a single entry point for all API requests, while the web interface offers a user-friendly front end.

## Team

Group 11
