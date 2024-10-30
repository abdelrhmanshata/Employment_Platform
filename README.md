# Employment Platform for Software Developers

This project is an employment platform designed to connect Software Developers (employees) with employers seeking talent. The platform allows employees to create profiles, search for vacancies, and apply for jobs, while employers can post job openings, browse developer profiles, and manage applications.

## Project Objectives

- Facilitate employment opportunities for software developers.
- Enable employers to search for candidates based on programming languages, location, experience level, and profile bio.
- Enhance job-matching based on employee profiles.

## Features

### Employee (Software Developer) Features
- **Registration:** Employees register with personal information (National ID, Name, City, Email), biography, known programming languages, and experience level (Junior, Mid, Senior).
- **Job Search and Application:** Employees can search for available vacancies and apply directly through the platform.
- **Notifications:** Employees receive notifications about jobs matching their skills and profile bio.
- **Profile Insights:** Track the number of times an employee's profile has been viewed.

### Employer Features
- **Job Posting:** Employers can post job vacancies.
- **Candidate Search:** Employers can search for candidates based on specific criteria:
  - Programming languages
  - City
  - Experience level
  - Bio text content
- **Application Management:** Employers can manage the application process, accepting or rejecting candidates and notifying them of their application status.

## System Requirements and Design

### Functional Requirements
1. Register employee details, including personal and technical information.
2. Post and manage job vacancies.
3. Handle application processes, including rejection, acceptance, and notifications.
4. Inform employees of matching jobs.
5. Summarize profile status for employees (e.g., number of profile views).
6. Enable employer filtering of employee profiles based on set criteria.

### Non-Functional Requirements
- **Performance:** The platform must handle multiple concurrent users effectively.
- **Usability:** The user interface should be intuitive and user-friendly.
- **Scalability:** The system should support growing data as more users join the platform.
- **Security:** Secure handling of personal data, especially National ID and email information.

### Use Cases
1. Employee registration and profile setup
2. Job search and application by employee
3. Job posting and candidate search by employer
4. Application acceptance and rejection process


### Database Design
- **Entity Relationship Diagram (ERD):** ![image](https://github.com/user-attachments/assets/0275fdd9-2666-428a-b361-7c49facd94c7)
- **Use Case Diagram:** ![image](https://github.com/user-attachments/assets/ada0ee08-d8ed-456f-acce-6c099faaf38d)



