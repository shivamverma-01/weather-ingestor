Project ELT Weather - Data Extraction from API
==============================================

  
<img src="img/etl-dag with mysql.png" alt="ETL DAG with MySQL" width="700"/>





  

 [![](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)[![](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white) ](https://airflow.apache.org/docs/)[![](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ](https://docs.docker.com/)[![](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/docs.html)

* * *

📌 About the Project
--------------------

This project demonstrates a complete **ETL (Extract, Transform, Load)** pipeline using weather data from an API. Here's the workflow:

*   **Extract**: Fetches weather data from the [WeatherAPI](https://www.weatherapi.com/) using a user-provided API key.
*   **Transform**: Processes the data with Python to prepare it for storage.
*   **Load**: Saves the clean data into an **SQLite** database (can also be connected to **MySQL** if modified).
*   The whole process is orchestrated using **Apache Airflow**, scheduled via a DAG.

* * *

⚙️ Installation & Setup
-----------------------

### 1\. Prerequisites

*   Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
*   (Optional) Install [MySQL CLI](https://dev.mysql.com/downloads/mysql/)

### 2\. Clone the Repository

    git clone https://github.com/patrickverol/Airflow
    cd Airflow

### 3\. Get Weather API Key

Sign up at [weatherapi.com](https://www.weatherapi.com/) and copy your API key.

### 4\. Update the API Key in the Script

Open `project_etl.py` and replace the placeholder key:

    key_api_weather = 'your_api_key_here'

### 5\. Start Airflow with Docker

Initialize Airflow:

    docker compose up airflow-init

Start Airflow Services:

    docker compose up

### 6\. Access Airflow Dashboard

Visit [http://localhost:8080](http://localhost:8080) in your browser

**Login Credentials:**

*   Username: `airflow`
*   Password: `airflow`

**Note:** If PostgreSQL is running on port 5432, stop it to avoid port conflicts.

* * *

💻 How It Works
---------------

*   The Airflow DAG automatically triggers the ETL pipeline.
*   You can schedule it or manually trigger it via the dashboard.
*   The data is stored in an MySQL database.

* * *

🗃️ Accessing the Data via MySQL CLI (Optional)
-----------------------------------------------

If using MySQL instead of SQLite, follow these steps:

1.  **Connect to MySQL via CLI**
    
        docker exec -it mysql mysql -u root -p
    
2.  **Show Databases**
    
        SHOW DATABASES;
    
3.  **Use the Relevant Database**
    
        USE your_database_name;
    
4.  **List Tables**
    
        SHOW TABLES;
    
5.  **Query Data**
    
        SELECT * FROM your_table_name LIMIT 10;
    

* * *

📝 Notes
--------

*   Modify `project_etl.py` if you want to redirect output to PostgreSQL instead of MySQL.

* * *

📬 Contact
----------

 [![](https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shivamverma61/)[![](https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white)](mailto:verma.shivam2605@gmail.com)
