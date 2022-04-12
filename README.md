# Performing-Symptom-Analysis-using-Big-Data-Management-Expert-Systems-to-Detect-Potential-Diseases (Feb 2022)

The key idea is to fully utilize the potential of Big Data Management & Analytics in combination with Machine Learning and Natural Language Processing that belong to the umbrella of Expert Systems. This project is used to suggest the likeliness of having top 10 diseases along with their probabilities based on the extent to which there is a match with the symptoms a person is experiencing. As an extension, an interactive system using a GUI is built which acts as a platform for the user to find which diseases he/she may be exposed to by providing the symptoms to the System.

- Natural Language Processing : Handles knowledge extraction & feature generation.
- Machine Learning : Building models based on the data.
- Big Data Management & Data Analytics : Processing huge data & Visualizing the inferences.


--------------------------------------------------
Django Setup

For Mac:
Navigate to env —> cd env
Activate the virtual environment —> Source env/bin/activate —> Before the username, you should see (env)
Now back to project folder —> cd ..

For Windows:
Navigate to env/Scripts —> cd env/Scripts
Activate the virtual environment —> activate —> Before the username, you should see (env)
Now back to project folder —> cd ..    cd ..

Common Installations:
Do the following installations only after the virtual environment is activated
pip install pymysql
pip install Django
Download & install xampp

To run the project:
Start xampp server
Go to http://localhost/phpmyadmin/
Import —> Run the swiftdiagnosis.sql file (Do this only once)
python manage.py runserver
To stop, use Ctrl+C
localhost:8000