# QuizzyLead Test Platform

QuizzyLead is a test platform designed to simplify test creation and assessment for teachers, enabling efficient student knowledge evaluation and progress monitoring.

## Installation

To use QuizzyLead, follow these steps:

1. Install Python: Make sure you have Python installed on your system. You can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Clone the Repository: Clone the QuizzyLead repository to your local machine using Git or download the source code directly.

3. Navigate to the Project Directory: Open a command prompt or terminal and navigate to the directory where you cloned or downloaded the QuizzyLead project.

4. Create a Virtual Environment (optional): It is recommended to create a virtual environment to isolate the project dependencies. Run the following command to create a virtual environment:
   ```
   python -m venv venv
   ```

5. Activate the Virtual Environment (optional): Activate the virtual environment using the appropriate command for your operating system:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

6. Install Dependencies: Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```

7. Set Up the Database: QuizzyLead uses a database to store user information and quiz data. Make sure you have a compatible database system installed (e.g., SQLite, PostgreSQL, MySQL). Create a database for QuizzyLead and update the database connection details in the `database.py` file.

8. Run the Application: Start the QuizzyLead application by running the following command:
   ```
   python app.py
   ```

9. Access the Application: Open a web browser and go to [http://localhost:5000/](http://localhost:5000/) to access the QuizzyLead Test Platform.

## Usage

### 1. Login

- Click on the "Login" link on the top right corner of the home page.
- Enter your username and password.
- Click the "Login" button to log into your account.

### 2. Admin Dashboard

- If you log in as an admin, you will have access to the admin dashboard.
- The admin dashboard provides various functionalities:
  - View all users: Click on the "View All Users" link to see a list of all registered users.
  - Add students: Click on the "Add Students" link to add new student users.
  - Add teachers/admins: Click on the "Add Teachers/Admins" link to add new teacher or admin users.
  - Reset passwords: Click on the "Reset Passwords" link to reset user passwords.
  - Delete users: Click on the "Delete Users" link to delete user accounts.
  - View results: Click on the "View Results" link to see the results of tests.

### 3. Teacher Dashboard

- If you log in as a teacher, you will have access to the teacher dashboard.
- The teacher dashboard provides various functionalities:
  - Create tests: Click on the "Create Test" link to create new tests.
  - View tests: Click on the "View Tests" link to see a list of created tests.
  - Delete tests: Click on the "Delete Tests" link to delete tests.
  - Assign tests: Click on the "Assign Tests" link to assign tests to classes.
  - View student results: Click on the "View Student Results" link to see the results of tests.

### 4. Student Dashboard

- If you log in as a student, you will have access to the student dashboard.
- The student dashboard provides various functionalities:
  - Take assigned tests: Click on the "Take Test" link to take tests assigned to your class.
  - View past tests: Click on the "Past Tests" link to view previous tests you have taken.
  - View results: Click on the "View Results" link to see your own quiz results.

### 5. Logout

- To log out, click on the "Logout" link in the navigation menu.

## Configuration

- The QuizzyLead Test Platform requires a database connection for storing user information and quiz data. Update the database connection details in the `database.py` file.

## File Structure

The QuizzyLead project follows the following file structure:

```
QuizzyLead/
├── questions/
│   ├── English_2023_pry_one.csv
│   ├── General_2023_pry_one.csv
│   ├── Maths_2023_pry_one.csv
│   ├── sample_2.csv
│   └── sample_3.csv
├── static/
│   ├── assets/
│   │   ├── favicon.ico
│   │   └── img/
│   │       ├── about-video.jpg
│   │       ├── background.jpg
│   │       ├── ee1.png
│   │       ├── google-play-badge.svg
│   │       ├── portrait_black.png
│   │       ├── app-store-badge.svg
│   │       ├── demo-screen.mp4
│   │       ├── ee2.png
│   │       ├── hero-bg.jpg
│   │       ├── quiz.jpg
│   │       ├── apple-touch-icon.png
│   │       ├── e12.png
│   │       ├── favicon.png
│   │       ├── home.png
│   │       ├── tnw-logo.svg
│   ├── css/
│   │   └── styles.css
│   ├── img/
│   └── js/
│       └── scripts.js
├── templates/
│   ├── allusers.html
│   ├── delete_test.html
│   ├── login.html
│   ├── resetpassword.html
│   ├── take_test.html
│   ├── view_std_result.html
│   ├── assign_test.html
│   ├── deleteuser.html
│   ├── nav.html
│   ├── results_admin.html
│   ├── tests_created.html
│   ├── viewquiz.html
│   ├── create_test.html
│   ├── index.html
│   ├── register.html
│   ├── results_student.html
│   ├── tests_given.html
│   ├── dashboard.html
│   ├── index2.html
│   ├── register_student.html
│   ├── results_teacher.html
│   └── view_result.html
├── app.py
├── config.py
├── database.py
├── README.md
└── requirements.txt

```

## Contributing

Contributions to QuizzyLead are welcome! If you want to contribute, please follow these guidelines:
- Fork the repository and clone it to your local machine.
- Create a new branch for your feature or bug fix.
- Make your changes and ensure that the code passes any tests.
- Commit your changes and push them to your forked repository.
- Open a pull request with a detailed description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Authors

- [Olatunde Timothy](https://github.com/leadconsult)

## Acknowledgments

- ALX and MasterCard for the opportunity.
- My wife for supporting me and encouraged me to keep going and persit till the end.
- Thank you to the creators and contributors of the libraries and frameworks used in this project.
