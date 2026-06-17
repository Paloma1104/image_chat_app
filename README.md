# Lens - AI Powered Image Intelligence

Lens is a full-stack web application that combines computer vision and generative AI to analyze images. Users can upload images, detect objects using YOLOv8, generate captions using Gemini, and ask questions about image content through a conversational interface.

## Features

* Upload and manage images
* Object detection using YOLOv8
* Annotated image generation with bounding boxes
* AI-generated image captions using Gemini 2.5 Flash
* Natural language chat with images
* Chat history storage
* Full CRUD operations for image records

## Tech Stack

* **Backend:** FastAPI, Python
* **Database:** SQLite, SQLAlchemy
* **Object Detection:** YOLOv8 (Ultralytics)
* **AI Model:** Google Gemini 2.5 Flash
* **Frontend:** HTML, CSS, JavaScript

## Project Structure

```text
app/
├── database/
├── services/
├── static/
├── templates/
├── schemas.py
└── main.py

uploads/
annotated/
requirements.txt
```

## Setup

### Clone Repository

```bash
git clone <repository-url>
cd image_chat_app
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

### Run Application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | /images            | List images         |
| POST   | /images            | Upload image        |
| PUT    | /images/{id}       | Update metadata     |
| DELETE | /images/{filename} | Delete image        |
| POST   | /detect/{id}       | Run YOLO detection  |
| POST   | /caption/{id}      | Generate caption    |
| POST   | /chat/{id}         | Ask image questions |
| GET    | /chat/{id}         | View chat history   |

## Screenshots

Add screenshots of:

* Dashboard
* Object Detection
* Caption Generation
* Image Chat

## Author

**Paloma Jain**
B.Tech Computer Science Engineering
The LNM Institute of Information Technology (LNMIIT), Jaipur
