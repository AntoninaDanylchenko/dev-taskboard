# 🧩 Dev Taskboard — Task Manager for IT Team

A simple yet functional task management system built with **Django** and styled using **AdminLTE**.  
The project simulates the workflow of an IT company, allowing developers, designers, project managers, and QA specialists to create, assign, and track tasks.

https://dev-taskboard.onrender.com/

login: user
password: user12345

---

## 🚀 Features

### 👤 Authentication & User Roles
- User registration, login, and logout (using Django Auth).
- Custom `Worker` model with assigned **Position** (e.g., Developer, Project Manager, QA).
- Profile pages:
  - View team members.
  - “About Me” page for each user.
  - Edit personal information.

### 📋 Task Management
- Create, update, delete, and view tasks.
- Tasks include:
  - `name`, `description`, `deadline`, `priority`, `task_type`, `is_completed`.
- Filter tasks by:
  - **Status:** Done / In Progress / Overdue  
  - **Priority:** High / Medium / Low
- Search tasks by name or description (universal search form).

### 👥 Team Collaboration
- Assign or remove yourself from a task (“Assign me / Remove me”).
- Mark tasks as done or reopen them.
- View tasks assigned to each team member.
- Pagination and responsive AdminLTE design.

---

## 🧱 Models Overview

- **Position** — job role of a team member.  
- **Worker (custom user)** — extends Django `AbstractUser`, adds position.  
- **TaskType** — category of the task (e.g., Backend, Design, Testing).  
- **Task** — main model representing each task, linked to `TaskType` and `Worker`.





