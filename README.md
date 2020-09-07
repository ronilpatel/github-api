#**A simple Github API data aggregator**

The sample_input.py file has all the API input data & can be changed as per needs.
This makes the entire code generalized. The API which the user intends to call can be mentioned 
in sample_input.py file along with other parameters.

./csv_writer/filters.py : This file contains all attributes that needs to be fetched from the API data 'items'.
                          In order to change the required attributes, the user only needs to make changes to this file.

Steps to run the code: 
1. Install packages from requirements.txt
2. Run all the tests using : python -m unittest
3. Make sure that all the tests are passing.
4. Run main.py: python main.py
5. Once the execution is complete, please check the logs.txt in the project directory
   for further detailedinformation
