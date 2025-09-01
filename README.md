## Project Progress Tracker 🚀

This is a progress tracker to help you manage the development of your social media project. It lists the core features from your proposal, new features we've added, and a list of known bugs.

### Core Features (From Proposal)

- [ ] **User Authentication & Profiles**
  - [x] User registration
  - [x] User login
  - [x] User profiles
  - [x] Profile editing (username, email, bio)
- [ ] **Post Functionality**
  - [x] Create new posts
  - [x] Edit existing posts
  - [x] Delete posts
- [ ] **Social Interactions**
  - [x] Add reactions to posts
  - [x] Add comments to posts
  - [x] Follow and unfollow users
- [ ] **Homepage & Feed**
  - [ ] Homepage to display a feed of posts
  - [x] Display posts from followed users
  - [ ] Post reaction counters
  - [x] Post comment section

***

### Features Added During Development ✨

These features were not part of the original proposal but have been implemented to improve the project.

- **Post Image Management**
  - [x] Allow post creation without a required image
  - [x] Allow authors to remove an image from a post when editing

***

### Concurrent Bugs & Known Issues 🐛

This is a list of known bugs that we have decided to set aside for now but need to be addressed in the future.

- **Homepage Post Visibility:** The `post_list` function on the homepage currently does not filter to include the current user's own posts, only posts from followed users.
- **Reaction Counters:** The reaction counters on the homepage are not always working correctly and may display a count of `0` even when a post has reactions. This is due to an inefficient database query.

Of course. Here is a professionally rephrased guide for your groupmates.

-----

### **Project Setup and Execution Guide** 🚀

This document outlines the systematic procedure for setting up and running the Django project on a local machine. Adhering to these steps will ensure all dependencies are correctly managed and the application operates as intended.

-----

### **1. Repository Cloning**

Initiate the setup process by cloning the project repository. Open a terminal or command prompt, navigate to the desired parent directory, and execute the following command:

```bash
git clone <repository_url>
```

----

### **2. Virtual Environment Configuration**

It is a best practice to encapsulate project-specific dependencies within a dedicated virtual environment. This prevents potential conflicts with other Python projects on the system.

First, navigate into the cloned project directory:

```bash
cd <project_directory>
```

Next, create the virtual environment:

```bash
python -m venv venv
```

Finally, activate the environment using the command appropriate for the operating system:

  * **Windows:** `venv\Scripts\activate`
  * **macOS/Linux:** `source venv/bin/activate`

-----

### **3. Dependency Installation**

With the virtual environment active, install all required Python libraries by executing the following command, which references the project's dependency list:

```bash
pip install -r requirements.txt
```

-----

### **4. Database Migration**

Django's Object-Relational Mapper (ORM) manages the database schema through migration files. Apply these migrations to create the necessary database tables.

```bash
python manage.py makemigrations
python manage.py migrate
```

-----

### **5. Superuser Creation**

To gain access to the administrative interface and facilitate project testing, a superuser account must be created. Follow the on-screen prompts to define the credentials.

```bash
python manage.py createsuperuser
```

-----

### **6. Development Server Initiation**

The project can be executed on a local server for development and testing purposes.

```bash
python manage.py runserver
```

Upon successful execution, the application will be accessible via a web browser at the following address: `http://127.0.0.1:8000/`.

-----

### **Troubleshooting**

  * **`ModuleNotFoundError`**: This typically indicates that the virtual environment is not active or the required dependencies were not installed. Ensure that the virtual environment is activated and that `pip install -r requirements.txt` was run successfully.
  * **Database-related Errors**: Should any database issues arise, a common solution is to delete the `db.sqlite3` file and the migration files within the `migrations` folders (excluding `__init__.py`). Then, re-execute the migration commands from **Step 4**.