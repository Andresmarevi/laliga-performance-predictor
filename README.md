# La Liga Performance Predictor

A web application to predict and analyze LaLiga fantasy football player performance using machine learning, Django (backend), and Vue.js (frontend).

---

## Project Structure

- **laliga-performance-predictor-app-backend**: Django backend (API, ML models with scikit-learn, data scraping)
- **laliga-performance-predictor-app-frontend**: Vue.js frontend (user interface)

---

## Setup Instructions

### Backend

1. **Navigate to the backend folder:**
   ```
   cd laliga-performance-predictor-app-backend
   ```
2. **Create and activate a virtual environment:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Open project folder:**
   ```
   cd backend_project
   ```
5. **Start the server:**
   ```
   python manage.py runserver
   ```

### Frontend

1. **Navigate to the frontend folder:**
   ```
   cd laliga-performance-predictor-app-frontend
   ```
2. **Install dependencies:**
   ```
   npm install
   ```
3. **Start the development server:**
   ```
   npm run dev
   ```

---

## Usage

- Access the frontend at [http://localhost:5173/](http://localhost:5173/)
- The backend API runs at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Search for players, view stats, see predictions and enjoy.

---

## Demo

Watch a demo of the app here:

[https://vimeo.com/1113281948](https://vimeo.com/1113281948)

---

## Technologies Used

- **Python**, **Django**
- **Vue.js**, **Vite**
- **scikit-learn**, **numpy**, **joblib**
- **django-cors-headers**, **requests**, **bs4**

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Andrés Martínez Reviriego