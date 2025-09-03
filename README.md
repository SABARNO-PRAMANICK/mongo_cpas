# User Input Storage API

A production-grade FastAPI application for storing and managing user input in MongoDB. This RESTful API supports creating, retrieving, updating, and partially updating user input records with robust error handling, data validation, and asynchronous endpoints.

## Features
- **Endpoints**:
  - `POST /inputs/`: Create a new user input entry.
  - `GET /inputs/`: Retrieve all user input entries.
  - `GET /inputs/{request_id}`: Retrieve a single entry by `request_id`.
  - `PUT /inputs/{request_id}`: Fully update an existing entry.
  - `PATCH /inputs/{request_id}`: Partially update an existing entry.
- **Production-Grade**:
  - MongoDB Atlas integration with retry and timeout.
  - Environment variable configuration for security.
  - Pydantic models for data validation.
  - Asynchronous endpoints for high concurrency.
  - Error handling with HTTP exceptions.
  - Unique `request_id` enforcement via MongoDB indexes.
  - Basic logging for debugging.

## Prerequisites
- Python 3.8+
- MongoDB Atlas account (or local MongoDB instance)
- Git
- Terminal access (macOS, Linux, or Windows)

## Project Structure
```
user-input-api/
├── app.py              # FastAPI application and endpoints
├── crud.py             # MongoDB connection and CRUD functions
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
├── .gitignore          # For ignoring the env varriables 
└── README.md           # This file
```

## Setup Instructions
Follow these steps to clone and run the project locally.

### 1. Clone the Repository
Clone the repository from Git:
```bash
git clone <repository-url>
cd user-input
```

### 2. Set Up MongoDB
- Create a MongoDB Atlas cluster (or use a local MongoDB instance).
- Obtain your MongoDB connection URI (e.g., `mongodb+srv://<user>:<pass>@cluster0.mongodb.net/?retryWrites=true&w=majority`).
- Create a database (e.g., `user_input_db`) and a collection (e.g., `inputs`).

### 3. Configure Environment Variables
- Copy the `.env.example` file to `.env`:
  ```bash
  cp .env.example .env
  ```
- Edit `.env` with your MongoDB details:
  ```plaintext
  MONGO_URI=mongodb+srv://<your-username>:<your-password>@cluster0.mongodb.net/?retryWrites=true&w=majority
  DATABASE_NAME=user_input_db
  COLLECTION_NAME=inputs
  ```

### 4. Create a Virtual Environment (macOS/Linux)
Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 5. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 6. Run the Application
Start the FastAPI server:
```bash
python app.py
```
Alternatively, for development with auto-reload:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`. Access the Swagger UI at `http://localhost:8000/docs` for interactive testing.

## Testing the API
Use the Swagger UI (`http://localhost:8000/docs`) or tools like curl/Postman to test the endpoints. Example requests:

- **Create an Input (POST)**:
  ```bash
  curl -X POST "http://localhost:8000/inputs/" -H "Content-Type: application/json" -d '{"request_id": "req123", "input": "Hello world", "metadata": {"source": "web"}}'
  ```

- **Get All Inputs (GET)**:
  ```bash
  curl "http://localhost:8000/inputs/"
  ```

- **Get Single Input (GET)**:
  ```bash
  curl "http://localhost:8000/inputs/req123"
  ```

- **Fully Update Input (PUT)**:
  ```bash
  curl -X PUT "http://localhost:8000/inputs/req123" -H "Content-Type: application/json" -d '{"request_id": "req123", "input": "Updated input", "metadata": {"source": "web"}, "date_time": "2025-09-04T12:00:00"}'
  ```

- **Partially Update Input (PATCH)**:
  ```bash
  curl -X PATCH "http://localhost:8000/inputs/req123" -H "Content-Type: application/json" -d '{"input": "Partially updated input"}'
  ```

## Environment Variables
The application uses the following environment variables (defined in `.env`):
- `MONGO_URI`: MongoDB connection string.
- `DATABASE_NAME`: Name of the MongoDB database (default: `user_input_db`).
- `COLLECTION_NAME`: Name of the MongoDB collection (default: `inputs`).

## Troubleshooting
- **Connection Issues**: Verify `MONGO_URI` in `.env` and ensure your IP is whitelisted in MongoDB Atlas.
- **Dependency Errors**: Ensure you're in the virtual environment (`source venv/bin/activate`) and have installed dependencies (`pip install -r requirements.txt`).
- **Port Conflicts**: If port 8000 is in use, change it in `app.py` (e.g., `uvicorn.run(app, host="0.0.0.0", port=8001)`).
