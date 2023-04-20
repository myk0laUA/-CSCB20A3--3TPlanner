Student: Mykola Zhuk id: 1007315512


Technologies Used:

    Python 3.9
    Flask 2.0.2
    Flask SQLAlchemy 2.0
    Flask Login 0.5.0
    Flask WTForms 0.15.1
    Flask Bootstrap 3.3.7.1
    Werkzeug 2.0.2

Usage:

    1. Register for a new account or log in to an existing account.

    2. Navigate to the My Day page to manage your tasks.

    3. Add a new task by entering a title and duration in minutes and clicking the Add button.

    4. Start a task by clicking the Start button next to it. The duration will count down in real-time.

    5. When you finish a task, click the Complete button to mark it as complete.

    6. If you need to stop a task before it's finished, click the Restart button to reset its duration.

    7. Navigate to the Tips page to see productivity tips from other users.

    8. Click the Like button on a tip to show your appreciation.

    9. Click the View Comments button to see existing comments or add a new comment using the form.

    10. Navigate to the Settings page to change your username, upload a new profile picture, or toggle dark mode.

    11. Log out when you're finished using the app.


Description:

        Home

    The home page of the Friendly Task application provides an overview of the project, including the implemented and planned features,
    as well as a list of frequently asked questions (FAQs) with answers to help users understand the purpose and functionality of the web app.

        Register

    To create a new account, navigate to the registration page by clicking on the "Register" link in the navigation bar.
    Enter your desired username, email, and password, then click the "Register" button. If the registration is successful, you will be redirected to the login page.

        Login

    To log in to your Friendly Task account, navigate to the login page by clicking on the "Login" link in the navigation bar.
    Enter your email and password, then click the "Log in" button. If the credentials are correct, you will be redirected to the home page.

        My Day

    The "My Day" page allows users to manage their daily tasks. To add a new task, fill out the "Add a new task" form and click the "Add task" button.
    The task will be added to the "Planned tasks" list. To start a task, click the "Start" button next to the task. The task will be moved to 
    the "Started tasks" list, and a timer will be displayed. To complete a task, click the "Complete" button. The task will be moved to the "Completed tasks" list. To restart a task,
    click the "Restart" button. The task will be moved back to the "Planned tasks" list.

        Settings

    The "Settings" page allows users to modify their settings. To change your username, enter a new username in the "Username" field and click the "Save changes" button.
    To upload a new profile picture, click the "Choose file" button and select a file from your computer. Then click the "Upload" button. To toggle dark mode, click the "Dark mode" checkbox.

        Tips

    The "Tips" page displays a list of tips. To add a new tip, fill out the "Add a new tip" form and click the "Add tip" button.
    The tip will be added to the list. To like a tip, click the "Like" button next to the tip. To view the comments on a tip, click the "Comments" button.
    The comments will be displayed in a modal window. To add a comment, enter your comment in the "Add a comment" field and click the "Add comment" button



Static:
    css:
        stylesheets.css: contains CSS styles for a website including general styles for fonts and links, styles for different themes (light and dark), styles for form inputs and buttons, styles for cards, modals, and smooth transitions between pages. The code utilizes transitions and box shadows to give the website a modern look.
    
    js:
        script.js: code for my_day.html includes a function that updates timers on the page, and the JS code for tips.html includes a function that sets focus on the first input field in a modal when it is displayed. Lastly, there is code for smooth transitions between pages, which sets the opacity of the page content to 1 once the page has loaded.

    profile_pics: folder that stores the profile pictures.(they are not used yet, but there will be features with them in the future.)

instance:
    app.db: SQL database for the web app.


Flask files:

    models.py: module defining models for a Flask web application. It includes models for User, Task, Tip, Comment, and Like, with properties such as id, username, email, password_hash, profile_picture, content, timestamp, duration, start_time, and completed. It uses Flask SQLAlchemy for database interaction, Flask Login for user authentication, and Werkzeug for password hashing and file uploads.

    forms.py: defines several forms using the FlaskForm class from the flask_wtf package and various fields and validators from the wtforms package.

    config.py: defines the configuration settings for the Flask application. It includes the secret key for secure sessions and the database URI for SQLAlchemy to connect to. If the environment variables for these values are not set, it defaults to a local SQLite database and a hard-coded secret key.

    app.py: The app is built with Flask and uses a SQLite database. Flask-WTF is used for form handling, and Flask-Bootstrap provides some pre-designed templates. SQLAlchemy is used as an ORM to manage database interactions, and Flask-Login is used to handle user authentication.