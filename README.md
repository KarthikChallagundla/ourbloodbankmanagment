# Blood Bank Management System

This project is a Blood Bank Management System developed using Django, a high-level Python web framework. The system allows users to manage blood donations, donors, patients, and blood requests efficiently.

## ScreenShots
### Homepage
![Home page](static/screenshot/homepage.png?raw=true)
### Admin Dashboard Page
![Admin Dashboard](static/screenshot/admindashboard.png?raw=true)
### Blood Donation Page
![Blood Doantion Page](static/screenshot//blooddonation.png?raw=true)
### Blood Request Page
![Blood Request Page](static/screenshot//bloodrequest.png?raw=true)
### Logout Page
![Logout Page](static/screenshot/logout.png?raw=true)

## Features

- User authentication and authorization system.
- Role-based access control for administrators, donors, and patients.
- Ability to register as a donor or a patient.
- Donors can donate blood and manage their donations.
- Patients can request blood and manage their requests.
- Admins can manage donors, patients, blood donations, blood requests, and user accounts.

## Technologies Used

- Python
- Django
- HTML
- CSS

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/KarthikChallagundla/ourbloodbankmanagment
    ```

2. Navigate to the project directory:

    ```
    cd ourbloodbankmanagment
    ```

3. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

4. Run migrations:

    ```
    python3 manage.py migrate
    ```

5. Create a superuser:

    ```
    python3 manage.py createsuperuser
    ```

6. Start the development server:

    ```
    python3 manage.py runserver
    ```

7. Open your web browser and go to `http://127.0.0.1:8000/` to access the application.

## Usage

- Log in using the credentials of an administrator, donor, or patient.
- Perform actions based on your role:
  - **Admin**: Manage donors, patients, blood donations, blood requests, and user accounts.
  - **Donor**: Donate blood, manage donations.
  - **Patient**: Request blood, manage requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was inspired by the need for efficient blood bank management systems.
- Special thanks to the Django community for providing excellent documentation and resources.
- Icons used in this project are from [FontAwesome](https://fontawesome.com/).