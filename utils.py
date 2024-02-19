import chromadb
import csv

def get_csv_file(filename):
    # Read the data from the CSV file
    with open(filename, "r") as f:
        # Skip the header row
        next(f)
        reader = csv.reader(f)
        return list(reader)
    
def add_logo_str():
    html = """
        <style>
    body {
    color: #ffffff;
    background-color:#ffffff;
    },
            [data-testid="stSidebarNav"] {
                background-image: url(https://seeklogo.com/images/F/florida-blue-logo-5766E58EBE-seeklogo.com.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            },
            {
        flex-direction: row-reverse;
        text-align: right;
    }
    </style>
    """
    return html