
# CSIT327-IM2-G5-MediServe Repository

## Project Title & Short Description

**Project Title:** MediServe: Community Health Portal  

**Short Description:**  
The MediServe project aims to address inefficiencies and challenges faced by barangay residents and local health center staff in accessing and managing medical services. This platform transforms manual processes into a convenient, centralized digital system.

**Current Problem:**  
Residents — especially the elderly and PWDs — must physically visit health centers to check medicine availability, which is time-consuming and inconvenient. Manual tracking also causes delays, errors, and inaccurate records.

**MediServe Solution:**  
MediServe provides a centralized portal to improve healthcare delivery by allowing residents to check medicine inventory and health news online, while empowering medical staff with efficient tools for inventory, orders, and data management.

---

## Key Features

The MediServe application has two main interfaces: **User Portal (Residents)** and **Admin Portal (Health Center Staff)**.

### 🧍‍♂️ 1. User Portal (Barangay Residents)
| **Feature** | **Description** |
|--------------|----------------|
| **Medicine Catalog** | Browse available medicines with real-time stock status (In Stock, Low Stock, Out of Stock). |
| **Online Ordering** | Add medicines to a cart, submit an order, and confirm total price. |
| **Queue Management** | View your queue number and estimated wait time for pickup. |
| **Profile & History** | View/Edit profile, settings, and past orders. |
| **Announcements** | Access health-related news, vaccine drives, and updates. |

### 🧑‍⚕️ 2. Admin Portal (Health Center Staff)
| **Feature** | **Description** |
|--------------|----------------|
| **Admin Dashboard** | Centralized hub accessible only by staff (`/management/menu/`). |
| **Stock Management** | View/edit medicine quantities and prices with color-coded stock alerts. |
| **Order Fulfillment** | View and manage orders (“Processing” or “Shipped”) and mark them as completed. |
| **Analytics & Records** | View key performance indicators and transaction logs for all stock updates. |

---

## Tech Stack Used

| **Component** | **Technology / Version** |
|----------------|---------------------------|
| **Backend** | Python 3.x, Django 5.x |
| **Database** | PostgreSQL (Hosted on Supabase) |
| **Frontend** | Django Templates, HTML, CSS, JavaScript |

---

## Setup & Run Instructions (Development)

Follow these steps to set up **MediServe** locally:

### Environment Setup & Dependencies
```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Django and PostgreSQL dependencies
pip install django psycopg2-binary dj-database-url
````

---

### Database Connection & Superuser Setup

Create a `.env` file in your root directory with:

```bash
DATABASE_URL=postgres://user:password@host:port/dbname
```

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

---

### Running the Server

```bash
python manage.py runserver
```

---

## 🌐 Accessing the Application

| **Role**           | **URL**                                                      | **Credentials**                            |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------ |
|  **User Access**  | [http://127.0.0.1:8000/](http://127.0.0.1:8000/)             | Create a new user via the **Sign Up** page |
| **Admin Access** | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) | Use your **Superuser** credentials         |

---

## Deployed Link

*Not yet deployed.*

---

## Team Members

| **Name**                  | **Role**       | **CIT-U Email**                                                           |
| ------------------------- | -------------- | ------------------------------------------------------------------------- |
| Pangilinan, Vein Carmell  | Lead Developer | [veincarmell.pangilinan@cit.edu](mailto:veincarmell.pangilinan@cit.edu)   |
| Panugaling, Franklyn John | Developer      | [franklynjohn.panugaling@cit.edu](mailto:franklynjohn.panugaling@cit.edu) |
| Pureza, Kristine Eunice   | Developer      | [kristineeunice.pureza@cit.edu](mailto:kristineeunice.pureza@cit.edu)     |
