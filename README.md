# 🎬 MovieWeb App

MovieWeb App is a Flask-based web application designed to manage personal movie collections. It allows users to create profiles and curate their favorite films, with data automatically enriched via the OMDb API.

---

## 🚀 Features

* **User Management:** Create and list multiple user profiles.
* **Movie Management:** Add, update, and delete movies for each user.
* **API Integration:** Fetches movie details (Poster, Director, Year) automatically using the OMDb API.
* **Modern UI:** Responsive design powered by Bootstrap 5, featuring Font Awesome icons and interactive hover effects.
* **Reliability:** Built-in ID validation, SEO-friendly 301 redirects, and Flash messages for real-time user feedback.

---

## 🛠️ Installation & Setup

To run the project locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd movieweb-app
    ```

2.  **Install Dependencies:**
    Make sure you have Python installed and a virtual environment active, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables:**
    Create a `.env` file in the root directory and add your keys:
    ```env
    API_KEY=your_omdb_api_key_here
    SECRET_KEY=your_secret_key_here
    ```

4.  **Run the Application:**
    ```bash
    python app.py
    ```
    The app will be available at `http://127.0.0.1:5000`.

---

## 🗃️ Database & Data
The project uses **SQLite** with **SQLAlchemy** as the ORM. 

* **Automatic Setup:** The database file is automatically generated in the `data/` directory upon the first run.
* **Git Notice:** The `data/` folder and the `.env` file are excluded from the repository to ensure privacy and clean version control.

---

## 📝 License
This project was created for educational purposes.