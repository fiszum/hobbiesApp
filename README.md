# hobbiesApp

Welcome to **hobbiesApp**, a web application designed to help users track their hobbies, connect with friends, and share their interests. This app is built using Django for the backend and Vue.js for the frontend, providing a modern, full-stack experience.

## Features

- **Main Page**: View and manage your hobbies.
- **Friends Page**: Connect with friends and share your activities.
- **Authentication**: Secure login and user registration.
- **Responsive**: Optimized for both desktop and mobile devices.

## Screenshots

Here are a couple of screenshots to give you a preview of the app:

### Main Page
![Main Page](pictures/main.jpeg)

### Friends Page
![Friends Page](pictures/friends.jpeg)
---

## Installation

To get the app up and running locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/fiszum/hobbiesApp.git
cd hobbiesApp
```

### 2. Set Up the Backend (Django)

**Install the required Python packages:**

```bash
pip install django
pip install django-crispy-forms
pip install crispy_bootstrap4
pip install django-cors-headers
pip install whitenoise
pip install requests
```

**Apply migrations to set up the database:**

```bash
python manage.py migrate
```

**Run the Django development server:**

```bash
python manage.py runserver
```
- The backend should now be running at `http://127.0.0.1:8000/`.

### 3. Set Up the Frontend (Vue.js)

**Navigate to the frontend directory:**

```bash
cd frontend
```

**Install the required Node.js packages:**

```bash
npm install
```

**Start the Vue.js development server:**

```bash
npm run dev
```
- The frontend should now be running at `http://localhost:3000/`.

## Contributing

Feel free to fork this project, submit issues, and create pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

--- 

Happy coding with hobbiesApp!