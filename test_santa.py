import os
import pytest
from app import app, allowed_file, parse_xlsx, generate_secret_santa

# Setup for test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Utility function for creating test files
def create_test_file(directory, filename, data):
    from openpyxl import Workbook
    if not os.path.exists(directory):
        os.makedirs(directory)
    workbook = Workbook()
    sheet = workbook.active
    for row in data:
        sheet.append(row)
    path = os.path.join(directory, filename)
    workbook.save(path)
    return path

# Test: Home Page
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Secret Santa' in response.data

# Test: File Upload Validation
def test_allowed_file():
    assert allowed_file("employees.xlsx")
    assert not allowed_file("employees.txt")

# Test: Parsing XLSX File
def test_parse_xlsx(tmp_path):
    test_file = create_test_file(tmp_path, "employees.xlsx", [["Name", "Email"], ["Alice", "alice@example.com"]])
    data = parse_xlsx(test_file)
    assert len(data) == 1
    assert data[0]['name'] == "Alice"
    assert data[0]['email'] == "alice@example.com"

# Test: Successful File Upload and Processing
def test_file_upload_and_processing(client, tmp_path):
    emp_file = create_test_file(tmp_path, "employees.xlsx", [["Name", "Email"], ["Alice", "alice@example.com"], ["Bob", "bob@example.com"]])
    prev_file = create_test_file(tmp_path, "previous.xlsx", [["Name", "Email"], ["Alice", "bob@example.com"]])

    with open(emp_file, 'rb') as emp, open(prev_file, 'rb') as prev:
        data = {
            'employee_file': (emp, "employees.xlsx"),
            'previous_file': (prev, "previous.xlsx"),
        }
        response = client.post('/', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert b'Secret Santa assignments generated successfully!' in response.data

# Fixed: test_generate_secret_santa
def test_generate_secret_santa():
    employees = [{"name": "Alice", "email": "alice@example.com"}, {"name": "Bob", "email": "bob@example.com"}]
    previous_assignments = {"Alice": [{"name": "Bob", "email": "bob@example.com"}]}
    with pytest.raises(ValueError):
        generate_secret_santa(employees, previous_assignments)

    previous_assignments = {}
    assignments = generate_secret_santa(employees, previous_assignments)

    # Fix: Verify both key-value pairs and ensure validity
    assert assignments["Alice"]["name"] == "Bob"
    assert assignments["Bob"]["name"] == "Alice"

# Fixed: test_file_download
def test_file_download(client, tmp_path):
    test_file = create_test_file(tmp_path, "secret_santa_result.xlsx", [["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"]])
    app.config['RESULT_FOLDER'] = tmp_path

    response = client.get(f'/download/secret_santa_result.xlsx')
    assert response.status_code == 200
    # Fix: Convert content type to string
    assert 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in response.content_type

# Fixed: test_download_nonexistent_file
def test_download_nonexistent_file(client):
    response = client.get('/download/nonexistent.xlsx', follow_redirects=True)
    # Fix: Check for flash message in the response body after following the redirect
    assert b"The requested file does not exist." in response.data
