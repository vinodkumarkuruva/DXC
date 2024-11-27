* Title : CSV_Extraction

* Description :
This program automates the Secret Santa assignment process for a group of employees. It ensures that each employee is assigned a different person to whom they will give a gift, following rules such as avoiding assigning someone their own name or the person they were assigned last year. The assignments are saved to a CSV file for easy sharing and organization.

* Features :
1.Input File: A CSV file containing employee details, including name and email. And a previous Year's CSV file with the previous year's Secret Santa assignments to ensure no repetitive assignments. 2.Assigns each employee a Secret Santa partner, avoiding the previous year's assignments. 3.Output File: A CSV file with the new assignments showing each employee's secret child.

* Requirements :
  1.Python 3.7+
  2.pytest (for running unit tests)
  3.random: To randomly assign secret children.
  4.openpyxl (optional, if you need to read/write Excel files).

* Technologies:
  1.Flask
  2.Flask-Forms

* Installation

  1.Clone this repository : git clone https://github.com/vinodkumarkuruva/Digital.git cd Digital

  2.Install the required dependencies : pip install -r requirements.txt

  3 .Run the Application : python app.py

  4 .Run the test cases : pytest test_santa.py

*Usage --> Prepare the Input Files:
  1 . Create an Excel file for employees, e.g., Employee-List.xlsx, with the following columns : Employee_Name , Employee_EmailID 
  2 . Create an Excel file for previous assignments, e.g., Secret-Santa-Game-Result-2023.xlsx, with the following columns : Employee_Name , Secret_Child_Name (the person they were assigned last year)
