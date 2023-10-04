# FX Derivative Analyzer

## Description
This project, "FX Derivative Analyzer," is a user-friendly interface for performing computations mainly related to FX options. It allows users to input data for an FX option and provides computed prices, greeks (sensitivity measures), and graphical representations of the option's characteristics. Users can choose from various methods for these computations.

## Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/fx-option-pricer.git
2. Navigate to the project directory:
   cd fx-option-pricer

3. Install the required dependencies using pip:
   pip install -r requirements.txt

4. To run the application, open a command prompt, navigate to the project folder (e.g., "C:\Users\my_name\rest_of_path\fx-option-pricer"), and enter the following command:
  streamlit run WebPricer.py

Usage
Instructions for using the application are available within the user interface.

FAQ
Q: Can I use my own data with the application?
A: Yes, you can replace the data used in the application with your own, but you must ensure that the Excel (xlsx) file you use has the same overall attributes, including column names and table size, as the one provided. If your data file differs significantly, you may need to make modifications to the code to accommodate the changes.

Q: Why do I get incorrect results with the Monte Carlo simulation?
A: The Monte Carlo simulation in the application is currently incomplete and in the process of being corrected. It may yield false results as of now. We are actively working on improving this feature, and updates will be provided in future releases.
