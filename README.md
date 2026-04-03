# 🎓 School Fee Collection & Student Records System

A full-stack web application developed using Flask (Python), HTML, CSS, JavaScript, and MySQL to automate student record management and fee collection in educational institutions.

---

## 🚀 Features
- Admin & Student Login System  
- Student Record Management  
- Fee Collection & Payment Tracking  
- Receipt Generation  
- Unpaid Fees Management  
- Dashboard for Admin & Students  
- Structured Database with Multiple Tables  

---

## 🏗️ System Architecture
The project follows a 3-Tier Architecture:

Frontend (Presentation Layer):
- HTML, CSS, JavaScript  
- User dashboards (Admin & Student)  
- Forms for login, registration, and payments  

Backend (Application Layer):
- Python Flask Framework  
- Handles routing, logic, authentication  
- Connects frontend with database  

Database (Data Layer):
- MySQL Database  
- Stores students, fees, payments, admin data  

---

## 🛠️ Technologies Used

Frontend:
- HTML5  
- CSS3  
- JavaScript  

Backend:
- Python  
- Flask  

Database:
- MySQL  

Tools:
- VS Code  
- XAMPP / MySQL Server  

---

## 📂 Project Structure

School-Fee-System/
│── app.py
│── db.py
│── requirements.txt
│
├── templates/
│   ├── admin_dashboard.html
│   ├── student_dashboard.html
│   ├── login.html
│   └── signup.html
│
├── static/
│   ├── css/
│   ├── js/
│
├── database/
│   ├── students.sql
│   ├── admin.sql
│   ├── payments.sql
│   └── fees.sql

---

## ⚙️ Installation & Setup

1. Clone Repository
git clone https://github.com/your-username/your-repo-name.git  
cd your-repo-name  

2. Create Virtual Environment
python -m venv .venv  

3. Activate Virtual Environment
Windows:
.venv\Scripts\activate  

Mac/Linux:
source .venv/bin/activate  

4. Install Dependencies
pip install -r requirements.txt  

5. Setup Database
- Open MySQL  
- Create database:
CREATE DATABASE school_db;  
- Import SQL files from database folder  

6. Run Application
python app.py  

Open in browser:
http://127.0.0.1:5000  

---

## 🔑 Modules

Admin Module:
- Manage students  
- View payments  
- Track unpaid fees  
- Dashboard overview  

Student Module:
- View fee details  
- Make payments  
- View payment history  

---

## ⚠️ Challenges Faced
- Managing multiple database tables  
- Preventing duplicate payments  
- Synchronizing frontend & backend  
- Handling authentication securely  

---

## 📈 Future Enhancements
- Online Payment Gateway Integration  
- Email/SMS Notifications  
- Analytics Dashboard  
- Mobile App Version  
- Role-Based Authentication (JWT)  

---

## 🧑‍💻 Author
Sabina Nadar  

---

## 📜 License
This project is for academic purposes.  

---

## ⭐ Acknowledgements
- Flask Documentation  
- MySQL Documentation  
- W3Schools  
- GeeksforGeeks  
