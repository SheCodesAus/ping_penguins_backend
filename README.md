## BloomBoard

### Team PingPenguins

## Table of Contents

- [Mission Statement](#mission-statement)
- [Features](#features)
  - [Summary](#summary)
  - [Users](#users)
  - [Sticky Notes](#sticky-notes)
  - [Workshop Boards](#workshop-boards)
  - [Pages/End Point Functionality](#pagesend-point-functionality)
  - [Nice To Haves](#nice-to-haves)
- [Technical Implementation](#technical-implementation)
  - [Back-End](#back-end)
  - [Front-End](#front-end)
  - [Git \& Deployment](#git--deployment)
- [Target Audience](#target-audience)
- [Back-end Implementation](#back-end-implementation)
  - [API Specifications](#api-specifications)
  - [Object Definitions](#object-definitions)
    - [Users](#users-1)
    - [Sticky Notes](#sticky-notes-1)
  - [Database Schema](#database-schema)
- [Front-end Implementation](#front-end-implementation)
  - [Wireframes](#wireframes)
    - [Landing Page](#landing-page)
    - [Create Profile](#create-profile)
    - [Project Board](#project-board)
    - [Admin Dashboard](#admin-dashboard)
    - [User Dashboard](#user-dashboard)
    - [Create New Project](#create-new-project)
  - [Colours and Fonts](#colours-and-fonts)
    - [Logo](#logo)
    - [Design Options](#design-options)


## Mission Statement

The goal for the Ping Penguins is to build a web-based application for Emma from Crowdbloom to facilitate workshops, where participants can collaborate on a virtual project board using sticky notes. The application will consist of a Django backend and a React frontend, with clearly defined responsibilities between the two.

## Features

### Summary

- Admins can create and manage workshop boards for collaborative projects.
- Participants register and join using a unique link to the workshop board (UID).
- Participants can contribute to boards by:
  - Posting sticky notes.
  - Editing sticky notes.
  - Deleting sticky notes.
- Sticky notes are categorised into predefined sections.
- The platform ensures:
  - Secure access.
  - Engagement.
  - A user-friendly experience.
### Users

| User Type   | Access Rights                                             | Example Roles            |
|-------------|----------------------------------------------------------|--------------------------|
| **Admin**   | Full access to create/manage workshops, boards, users, and sticky notes. Export and analyse board data. | Crowdbloom facilitators |
| **Participant** | Register and log in using a project code. Post, edit, or delete sticky notes and view workshop boards. | Workshop attendees      |

### Sticky Notes

| Feature       | Details                                                                                   | Notes |
|---------------|-------------------------------------------------------------------------------------------|-------|
| **Create**    | Participants can create sticky notes with a comment (max 160 characters).                 | Default colours: Primary hues aligned with the thematic palette |
| **Edit/Delete** | Participants can edit or delete their notes post-submission.                             | Notes are linked to the user via user ID in the backend database. |
| **Display**   | Notes are categorised into predefined columns on the board.                               | Board categories are defined during project creation. |
| **colours**    | Magenta, Black, Off-White, Light Gray.                                                    | Additional colour options to be tested with the client during build. |

### Workshop Boards

| Feature       | Details                                                                                   | Notes |
|---------------|-------------------------------------------------------------------------------------------|-------|
| **Unique Link/Code** | Generated for each workshop. Participants use the project code to access the board. | Back-end uses UID (Unique Identifier) to provide a secure link. |
| **Board Access** | Boards become accessible at the workshop start time and remain active until the workshop ends. | Access policies can be updated by the Admin. |

### Pages/End Point Functionality

*** Insert ***


### Nice To Haves

- Link to project code expires after a set period of time.
- Real-time board updates without page reload.
- Notes data exports to Excel.
- Custom colour palette for sticky notes.
- Countdown Timer is displayed on the board showing the time remaining until the workshop begins.
- Automatically generated QR codes for workshop links.
- Admin defines the maximum number of sticky notes each user can create per board.

## Technical Implementation

### Back-End

- **Framework:**  Django
- **Responsibilities:**  User registration, authentication (token-based), project management, board data storage, permissions and role management.
- **Error Handling:**  Appropriate HTTP error codes (e.g., 400, 403). Custom error messages as needed.

### Front-End

- **Framework:**  React
- **Responsibilities:**  Interactive UI for workshop setup, user registration/login, and sticky note functionality.
- **Design:**  Bright, professional UI with responsive design for mobile and desktop.

### Git & Deployment

- **Back-End:**  Deployed on Heroku.
- **Front-End:**  Deployed on Netlify.
- **Version Control:**  GitHub repositories.

---

## Target Audience

- **Facilitators and Admins:** Crowdbloom team members responsible for managing workshops.
- **Participants:** Workshop attendees who collaborate on boards and share their comments via notes.

## Back-End Implementation

### API Specifications

| HTTP Method | URL                  | Purpose                                     | Request Body | Successful Response Code | Authentication and Authorisation |
|-------------|----------------------|---------------------------------------------|--------------|--------------------------|-----------------------------------|
| GET         | `/board/`            | Returns all boards for the Admin            |              | 200                      | Admin ONLY                       |
| POST        | `/board/`            | Creates a new board                         |              | 201                      | Admin ONLY                       |
| GET         | `/board/int:pk/`     | Returns project with INT ID                 |              | 200                      | Auth token matches accessed_user ID & Admin |
| PUT         | `/board/int:pk/`     | Edits an existing Board                     |              | 200                      | Admin ONLY                       |
| DELETE      | `/board/int:pk/`     | Permanent cascade deletion of board and all notes |       | 202                      | Admin ONLY                       |
| GET         | `/notes/`            | Returns all notes                           |              | 200                      | Auth token matches accessed_user ID & Admin |
| POST        | `/notes/`            | Creates new note                            |              | 201                      | Auth token matches accessed_user ID & Admin |
| GET         | `/notes/int:pk/`     | Returns note with INT ID                    |              | 200                      | Auth token matches accessed_user ID for board & Admin |
| PUT         | `/notes/int:pk/`     | Edits an existing Note                      |              | 200                      | Note Owner &/Admin               |
| DELETE      | `/notes/int:pk/`     | Permanent delete of note                    |              | 202                      | Note Owner &/Admin               |
| POST        | `/users/`            | Creates new User                            |              | 201                      | Unique Username and Email address |
| GET         | `/users/`            | Returns list of all Users                   |              | 200                      | Admin ONLY                       |
| GET         | `/users/int:pk/`     | Returns User details for INT ID             |              | 200                      | Auth Token for User & Admin      |
| PUT         | `/users/int:pk/`     | Edits User details with INT ID              |              | 200                      | Auth Token for User & Admin      |
| DELETE      | `/users/int:pk/`     | Permanent cascade deletion of User and all notes |       | 202                      | Admin ONLY                       |
| POST        | `/api-token-auth/`   | Creates a JWT for User                      | Provide correct username and password | 201 |

### Object Definitions

#### Users

| Field         | Data Type |
|---------------|-----------|
| id            | integer   |
| password      | hash      |
| last_login    | timestamp |
| is_superuser  | bool      |
| username      | text      |
| first_name    | text      |
| last_name     | text      |
| email         | email     |
| company       | text      |
| role_title    | text      |
| tenure        | integer   |
| is_staff      | bool      |
| is_active     | bool      |
| date_joined   | timestamp |

#### Project Board

| Field         | Data Type |
|---------------|-----------|
| id            | integer   |
| title         | text      |
| description   | varchar   |
| date_start    | timestamp |
| accessed_users| key       |
| column_number | int       |
| category_titles | array   |
| disclaimer    | text      |
| UID           | key       |

#### Sticky Notes

| Field         | Data Type |
|---------------|-----------|
| id            | integer   |
| comment       | varchar   |
| anonymous     | bool      |
| board_id      | key       |
| owner_id      | key       |


## Database Schema

![Database Schema](/img/database-schema.png)


## Front-End Implementation

### Wireframes

[Click this link to see the live Demo on Figma](https://www.figma.com/proto/vYhnfeEaDvn8mpsmz4RcmS/WinWall?node-id=6-20&t=n4WIUrTsQ1dB0W03-1&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=6%3A20&show-proto-sidebar=1)

**Landing Page**

![Landing Page](/img/landing-page.PNG)

**Create Profile**

![Create Profile](/img/create-profile.PNG)

**Project Board**

![Project Board](/img/project-board.PNG)

**Admin Dashboard**

![Admin Dashboard](/img/admin-dashboard.PNG)

**User Dashboard**

![User Dashboard](/img/user-dashboard.PNG)

**Create New Project**

![Create New Project](/img/create-new-project.PNG)


### Colours and Fonts

**Logo**

![Logo](/img/bloomboard-logo.PNG)

**Design Options** 

![Colours and Fonts - Option 1](/img/colours-fonts1.PNG)

![Colours and Fonts - Option 2](/img/colours-fonts2.PNG)