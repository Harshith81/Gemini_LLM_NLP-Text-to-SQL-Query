from dotenv import load_dotenv
load_dotenv()  # load all the environment variables
import streamlit as st
import os
import sqlite3
import pandas as pd
import plotly.express as px
import spacy
import google.generativeai as genai   
from io import BytesIO

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))     

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [description[0] for description in cur.description]
        return rows, columns
    except sqlite3.Error as e:
        return None, str(e)
    finally:
        conn.close()

# Function to get database schema
def get_db_schema(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    schema = {}
    for table in tables:
        cur.execute(f"PRAGMA table_info({table[0]});")
        columns = cur.fetchall()
        schema[table[0]] = [col[1] for col in columns]
    conn.close()
    return schema

# Preprocess question
def preprocess_question(question):
    doc = nlp(question)
    return " ".join([token.lemma_ for token in doc])

# Visualize data
def visualize_data(df):
    fig = px.bar(df, x=df.columns[0], y=df.columns[1:], title="Query Results Visualization")
    st.plotly_chart(fig)

# Export data
def export_data(df, format):
    if format == "csv":
        return df.to_csv(index=False).encode('utf-8')
    elif format == "excel":
        output = BytesIO()
        df.to_excel(output, index=False)
        return output.getvalue()
    elif format == "json":
        return df.to_json().encode('utf-8')

# Define your prompt
prompt = [
    """
    
    You are an expert in converting English questions to SQL query for an SQLite database.
    The SQLite database has the following tables and columns: {schema}
    
    Follow the column names and their corresponding values correctly without any mistakes,
    and take care of underscores,semicolon,operators.      

    For example:
    
    Example 1 - How many entries of records are present in table X?, 
    the SQL command will be something like this: 
    SELECT COUNT(*) FROM X;
    
    Example 2 - Tell me all the records from table Y where column Z equals 'value'?, 
    the SQL command will be something like this: 
    SELECT * FROM Y WHERE Z='value';
    
    Example 3 - Retrieve all customers who made purchases above $1000 in the last month, 
    the SQL command will be something like this: 
    SELECT * FROM Customers WHERE CustomerID IN (SELECT CustomerID FROM Orders WHERE OrderDate >= DATE('now', '-1 month') AND TotalAmount > 1000);

    Example 4 - List all departments and their average salaries, ordered by department name, 
    the SQL command will be something like this:
    SELECT DepartmentName, AVG(Salary) FROM Employees INNER JOIN Departments ON Employees.DepartmentID = Departments.DepartmentID GROUP BY DepartmentName ORDER BY DepartmentName;
    
    Example 5 - Show all products with their total sales, sorted by total sales in descending order, 
    the SQL command will be something like this:
    SELECT Products.*, SUM(Quantity * UnitPrice) AS TotalSales FROM Products INNER JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID GROUP BY Products.ProductID ORDER BY TotalSales DESC;
    
    Example 6 - Display employees and their managers, where the manager's name starts with 'John', 
    the SQL command will be something like this:
    SELECT Employees.*, Managers.ManagerName FROM Employees LEFT JOIN Employees AS Managers ON Employees.ManagerID = Managers.EmployeeID WHERE Managers.ManagerName LIKE 'John%';
    
    Example 7 -Retrieve all products from the Products table?: 
    the SQL command will be something like this: 
    SELECT * FROM Products;
    
    Example 8 - List all employees and their departments?, 
    the SQL command will be something like this: 
    SELECT Employees.*, Departments.DepartmentName
    FROM Employees
    INNER JOIN Departments ON Employees.DepartmentID = Departments.DepartmentID;

    Example 9 - Find customers with a specific email address?,
    the SQL command will be something like this: 
    SELECT * FROM Customers WHERE Email = 'example@email.com';
    
    Example 10 - Retrieve orders made by customers in a specific city?,
    the SQL command will be something like this: 
    SELECT Orders.*, Customers.CustomerName
    FROM Orders
    INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    WHERE Customers.City = 'New York';

    Example 11 - Get all orders and their corresponding customers?,
    the SQL command will be something like this: 
    SELECT Orders.*, Customers.CustomerName
    FROM Orders
    INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID;

    Example 12 - List all employees and their managers?,
    the SQL command will be something like this: 
    SELECT Employees.*, Managers.EmployeeName AS ManagerName
    FROM Employees
    LEFT JOIN Employees AS Managers ON Employees.ManagerID = Managers.EmployeeID;

    Example 13 - Calculate total sales for each product?,
    the SQL command will be something like this: 
    SELECT ProductID, SUM(Quantity * UnitPrice) AS TotalSales
    FROM OrderDetails
    GROUP BY ProductID;

    Example 14 - Show total revenue per month?,
    the SQL command will be something like this: 
    SELECT strftime('%Y-%m', OrderDate) AS Month, SUM(TotalAmount) AS TotalRevenue
    FROM Orders
    GROUP BY strftime('%Y-%m', OrderDate)
    ORDER BY Month;

    Example 15 - Find departments with more than 10 employees?,
    the SQL command will be something like this: 
    SELECT DepartmentID, COUNT(*) AS EmployeeCount
    FROM Employees
    GROUP BY DepartmentID
    HAVING COUNT(*) > 10;

    Example 16 - Calculate average order amount for customers who placed more than 5 orders?,
    the SQL command will be something like this: 
    SELECT CustomerID, AVG(TotalAmount) AS AverageOrderAmount
    FROM Orders
    GROUP BY CustomerID
    HAVING COUNT(*) > 5;

    Example 17 - Get customers who made both online and in-store purchases?,
    the SQL command will be something like this: 
    (SELECT CustomerID FROM Orders WHERE PurchaseType = 'Online')
    INTERSECT
    (SELECT CustomerID FROM Orders WHERE PurchaseType = 'In-Store');

    Example 18 - Retrieve products with a specific category and price range?,
    the SQL command will be something like this: 
    SELECT * FROM Products
    WHERE Category = 'Electronics' AND Price BETWEEN 1000 AND 2000;

    Example 19 - Find orders placed by customers in a specific region or with a high total amount?,
    the SQL command will be something like this: 
    SELECT * FROM Orders
    WHERE Region = 'North' OR TotalAmount > 5000;
    
    Example 20 - Search for products with names containing 'Phone'?,
    the SQL command will be something like this: 
    SELECT * FROM Products
    WHERE ProductName LIKE '%Phone%';

    Example 21 - Find employees with names starting with 'J' or 'K'?,
    the SQL command will be something like this: 
    SELECT * FROM Employees
    WHERE EmployeeName LIKE 'J%' OR EmployeeName LIKE 'K%';

    Example 22 - How many entries of records are present in table X?, 
    the SQL command will be something like this: 
    SELECT COUNT(*) FROM X;
    
    The SQL code should not have ``` in the beginning or end and no "sql" word in output.
    
    """
]  

# Streamlit app
st.set_page_config(page_title="Natural Language to SQL Query App")
st.header("Gemini_LLM Natural Language Text to SQL Query App 🗃️")

# Database upload
uploaded_file = st.file_uploader("Choose Your DataBase File", type="db")
if uploaded_file:
    db_path = f"temp_{uploaded_file.name}"
    with open(db_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    schema = get_db_schema(db_path)
    st.write("Database Schema of Uploaded File 📑:")
    st.json(schema)

    question = st.text_input("Input your Query in Plain Text :", key="input")

    if st.button("Get Query Response 🔍"):
        preprocessed_question = preprocess_question(question)
        formatted_prompt = prompt[0].format(schema=schema)
        response = get_gemini_response(preprocessed_question, [formatted_prompt])
        st.write(f"Generated SQL Query: {response}")

        response_data, columns_or_error = read_sql_query(response, db_path)
        st.subheader("Query Response 📃")

        if response_data is not None:
            df = pd.DataFrame(response_data, columns=columns_or_error)
            st.dataframe(df)

            if st.button("Visualize My Results"):
                visualize_data(df)

            st.download_button(label="Download CSV 📩", data=export_data(df, "csv"), file_name="data.csv", mime="text/csv")
            st.download_button(label="Download Excel 📩", data=export_data(df, "excel"), file_name="data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            st.download_button(label="Download JSON 📩", data=export_data(df, "json"), file_name="data.json", mime="application/json")
        else:
            st.write(f"Error executing query: {columns_or_error}")
              






