Job Recruiting and Seeking System

Description:
This project is a job recruiting and seeking system developed in Python. It allows job seekers to find job postings and recruiters to post job openings. The system includes features for searching, applying, and managing job listings.

Features:
    Job seekers can upload/update their resumes.
    Recruiters can post job openings and search for best matching candidates.
    Users can search for jobs based on company and position name.
    Messaging/notifying to seekers when their application has been approved by a recruiter.

Installation:
To set up the project, follow these steps:
    Ensure you have Python installed: The project requires Python 3.12.3. You can download Python from python.org.

    Install necessary packages:
    Open your terminal or command prompt and install the required packages using pip.

    To install the dependencies:
        pip install pymysql
        pip install -U pip setuptools wheel
        pip install -U spacy
        python -m spacy download en_core_web_lg
        pip install webbrowser
        pip install pillow
        pip install pymupdf
        pip install vonage

Usage:
    Run the application:
    Navigate to the project directory and run the main script, which is welcome.py.

    Interacting with the system:
        Job seekers can register, log in, and search for jobs.
        Recruiters can log in, post job openings, and search for candidates.

Project Structure:
    welcome.py: Entry point of the application.
    signup.py: Signing in to save account to database.
    fgot_pwd.py: Changing password for account.
    main.py: Log in as recruiter or seeker.
    nithishlogin.py: Home page for seeker.
    pdfread.py: Upload resume.
    apply.py: Search and apply for jobs.
    viewoffer.py: View if any applications have been approved.
    rechome.py: Home page for recruiter.
    createjob.py: Create job positions for company.
    resumecmpr.py: Find best matching applicant for their job.

Dependencies:
This project requires the following Python libraries:
    PyMySQL
    tkinter
    spaCy
    webbrowser
    PyMuPDF
    Pillow
    Vonage
