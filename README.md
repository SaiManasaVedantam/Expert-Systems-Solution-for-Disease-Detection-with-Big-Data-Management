# Performing-Symptom-Analysis-using-Big-Data-Management-Expert-Systems-to-Detect-Potential-Diseases (Feb 2022)

## About the Project
The key idea is to fully utilize the potential of Big Data Management & Analytics in combination with Machine Learning and Natural Language Processing that belong to the umbrella of Expert Systems. This project is used to suggest the likeliness of having top 10 diseases along with their probabilities based on the extent to which there is a match with the symptoms a person is experiencing. As an extension, an interactive system using a GUI is built which acts as a platform for the user to find which diseases he/she may be exposed to by providing the symptoms to the System.

- Natural Language Processing : Handles knowledge extraction & feature generation.
- Machine Learning : Building models based on the data.
- Big Data Management & Data Analytics : Processing huge data & Visualizing the inferences.

## Instructions to set up Django

#### For Mac:
1. Navigate to env —> cd env
2. Activate the virtual environment —> source env/bin/activate —> Before the username, you should see (env)
3. Now back to project folder —> cd ..

#### For Windows:
1. Navigate to env/Scripts —> cd env/Scripts
2. Activate the virtual environment —> activate —> Before the username, you should see (env)
3. Now back to project folder —> cd ..    cd ..

#### Common Installations:
Do the following installations only after the virtual environment is activated
1. pip install pymysql
2. pip install Django
3. Download & install xampp

#### To run the project:
1. Start xampp server
2. Go to http://localhost/phpmyadmin/
3. Import —> Run the swiftdiagnosis.sql file (Do this only once)
4. Navigate to project folder & then --> python -m venv env (For Mac users)
5. python manage.py runserver
6. To stop, use Ctrl+C
7. http://localhost:8000 to view the UI up & running

## About files in "StartApp" folder
1. urls.py: Provides the mapping of our apps urls to their respective python views(methods).
2. views.py: Provides the mapping of the logic behind every screen of the application. This is mapped from the urls.py      folder.
3. models.py: Provides the mapping to our SQL database.
The Template folder contains the webpage's html files.
