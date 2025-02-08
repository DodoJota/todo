Flask Todo List Application
Description
This is a simple and modern web-based Todo List application built with Flask, SQLite, HTML, CSS, and JavaScript. The application allows users to add, complete, and delete tasks through an intuitive and visually appealing interface.

Features
Add Tasks: Quickly add new tasks to your todo list.
Complete Tasks: Mark tasks as completed by checking the checkbox.
Delete Tasks: Remove tasks that are no longer needed.
Responsive Design: The interface is responsive and adapts to different screen sizes.
Modern UI: Clean and modern user interface with intuitive colors and styles.
Technologies Used
Backend: Python, Flask, Flask_SQLAlchemy
Database: SQLite
Frontend: HTML5, CSS3, JavaScript (ES6)
Styling: Custom CSS with modern design principles
Fonts: Google Fonts ("Roboto")
Installation
Follow these steps to set up and run the application locally:

Prerequisites
Python 3.x installed on your machine.
Git installed for cloning the repository (optional).
Steps
Clone the Repository

BASH

git clone https://github.com/DodoJota/todo.git
cd your-repo-name
Alternatively, you can download the ZIP file from GitHub and extract it.

Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

BASH

python -m venv venv
Activate the Virtual Environment

On Windows:

BASH

venv\Scripts\activate
On macOS and Linux:

BASH

source venv/bin/activate
Install Dependencies

BASH

pip install -r requirements.txt
Note: If you don't have a requirements.txt file, create one in the project root directory with the following content:


Flask
Flask_SQLAlchemy
Then run the install command again.

Set Up the Database

The application uses SQLite, and the database will be created automatically when you run the app for the first time.

Run the Application

BASH

python app.py
The app will start running on http://127.0.0.1:5000/.

Access the Application

Open your web browser and navigate to http://127.0.0.1:5000/ to see the Todo List application in action.

Project Structure

- app.py
- todo.db
- requirements.txt
- /templates
    - index.html
- /static
    - styles.css
    - main.js
app.py: The main Flask application file containing backend logic.
todo.db: SQLite database file (created automatically).
requirements.txt: Python dependencies required for the project.
/templates/index.html: HTML template for the application's frontend.
/static/styles.css: CSS stylesheet for styling the application.
/static/main.js: JavaScript file for frontend interactivity.
Usage
Add a Task: Enter a task description in the input field and click "Add".
Complete a Task: Click the checkbox next to a task to mark it as completed. The task text will have a line-through effect.
Delete a Task: Click the "×" button next to a task to delete it from the list.
Flash Messages: Success and error messages will appear at the top of the page for actions performed.

Customization
Feel free to customize the application to suit your needs. You can modify the styles in styles.css, adjust the HTML structure in index.html, or add new features in app.py and main.js.

Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please create a pull request or open an issue.

Steps to Contribute
Fork the Repository

Create a New Branch

BASH

git checkout -b feature/YourFeatureName
Make Your Changes

Commit Your Changes

BASH

git commit -m "Add your commit message here"
Push to Your Fork

BASH

git push origin feature/YourFeatureName
Create a Pull Request on the original repository.

License
This project is licensed under the MIT License - see the LICENSE file for details.
