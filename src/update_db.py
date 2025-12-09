# %%
import os
import pandas as pd
import psycopg2
import psycopg2.extras
import re
from datetime import datetime
import numpy as np
from dateutil.parser import parse 
import chardet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import glob
from email.mime.base import MIMEBase
from email import encoders

# --- CONFIGURATION & CREDENTIALS (REDACTED) ---
DB_USER = 'REDACTED_DB_USER'
DB_PASSWORD = 'REDACTED_DB_PASSWORD'
DB_NAME = 'REDACTED_DB_NAME'
DB_HOST = 'REDACTED_DB_HOST' # e.g., 192.168.x.x

EMAIL_SENDER = 'bot-support@REDACTED_DOMAIN.com'
EMAIL_PASSWORD = 'REDACTED_EMAIL_PASSWORD'
EMAIL_SERVER = 'smtp.office365.com'

# List of email recipients
EMAILS_INTERNAL = ["REDACTED_ADMIN_1@email.com", "REDACTED_ADMIN_2@email.com"]
EMAILS_CLIENTS = ['REDACTED_CLIENT_1@email.com', 'REDACTED_CLIENT_2@email.com']

# File System Paths
ROOT_DOC_DIR = r"C:\Users\REDACTED_USER\Documents"
# ----------------------------------------------

# %%
def connect_db():
    # Establishes connection using redacted credentials
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=5432,
        cursor_factory=psycopg2.extras.DictCursor
    )

conn = connect_db()
conn.autocommit = True
cursor = conn.cursor()

# %%
def custom_date_parser(date_str):
    try:
        return parse(str(date_str))
    except (ValueError, TypeError):
        return pd.NaT

# %%
def get_codes(cursor, item_name, supp_name):
    cursor.execute("select ac_code from all_supplier_master where account_name= %s;", (supp_name,))
    supplier_code = cursor.fetchone()
    cursor.execute("select item_code from all_item_master where item_name= %s;", (item_name,))
    item_code = cursor.fetchone()
    return (supplier_code['ac_code'], item_code['item_code']) if supplier_code and item_code else (None, None)

# %%
def insert_pur_daily(cursor, filename, encoding):
    df = pd.read_csv(filename, header=5, skiprows=[6], encoding= encoding) 
    df.drop(df.columns[0], axis=1, inplace=True) 
    df.drop(df.index[-1], inplace=True)
    df['Order Date'] = df['Order Date'].apply(custom_date_parser)
    
    # SCD Type 1 Logic: Update existing rows, insert new ones
    insert_sql= """INSERT INTO pur_order_daily_main (
        order_date, supplier_code, supplier_name, item_category_code, item_category_name,
        item_code, item_name, um, order_number, entered_by_name,
        indent_number, department, department_name, cost_project, cost_project_name,
        currency_code, currency_name, exchange_rate, stock_type_name, order_value, order_quantity, bal_qty, rate
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (order_date, item_code, order_number, department, cost_project)
    DO UPDATE SET
        supplier_name = EXCLUDED.supplier_name,
        item_category_code = EXCLUDED.item_category_code,
        item_category_name = EXCLUDED.item_category_name,
        item_name = EXCLUDED.item_name,
        um = EXCLUDED.um,
        entered_by_name = EXCLUDED.entered_by_name,
        indent_number = EXCLUDED.indent_number,
        department_name = EXCLUDED.department_name,
        cost_project_name = EXCLUDED.cost_project_name,
        currency_code = EXCLUDED.currency_code,
        currency_name = EXCLUDED.currency_name,
        exchange_rate = EXCLUDED.exchange_rate,
        stock_type_name = EXCLUDED.stock_type_name,
        order_value = EXCLUDED.order_value,
        order_quantity = EXCLUDED.order_quantity,
        bal_qty = EXCLUDED.bal_qty,
        rate = EXCLUDED.rate;
    """

    for inx, row in df.iterrows():
        values = (row['Order Date'], row['Supplier Code'], row['Supplier Name'], row['Item Category Code'], row['Item Category Name'], row['Item Code'], row['Item Name'], row['UM'], row['Order Number'], row['Entered By Name'], row['Indent Number'], row['Department'], row['Department Name'], row['Cost/Project'], row['Cost/Project Name'], row['Currency Code'], row['Currency Name'], row['Exchange Rate'], row['Stock Type Name'], row['Order Value'], row['Order Quantity'], row['Bal Qty'], row['Rate'])
        try:
            cursor.execute(insert_sql, values)
        except Exception as e:
            print(f"Error inserting row {inx}: {e}")
            continue
    return len(df)

# %%
def insert_grn_daily(cursor, filename, encodeing):
    df = pd.read_csv(filename, header=5, skiprows=[6], encoding= encodeing) 
    df.drop(df.columns[0], axis=1, inplace=True) 
    df.drop(df.index[-1], inplace=True)
    df['GRN Date'] = df['GRN Date'].apply(custom_date_parser)
    
    insert_sql = """INSERT INTO grn_daily_main (
        grn_date, supplier_code, supplier_name, item_ctag_code, item_ctag_name,
        item_code, item_name, um, stock_type_name, grn_number,
        purchase_order_number, department, department_name, indent_number,
        currency_code, exchange_rate, cost_project, cost_project_name,
        currency_name, challan_qty, rate, net_amount
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s
    )
    ON CONFLICT (grn_date, item_code, grn_number, purchase_order_number, department, cost_project)
    DO UPDATE SET
        supplier_name     = EXCLUDED.supplier_name,
        item_ctag_code    = EXCLUDED.item_ctag_code,
        item_ctag_name    = EXCLUDED.item_ctag_name,
        item_name         = EXCLUDED.item_name,
        um                = EXCLUDED.um,
        stock_type_name   = EXCLUDED.stock_type_name,
        department_name   = EXCLUDED.department_name,
        indent_number     = EXCLUDED.indent_number,
        currency_code     = EXCLUDED.currency_code,
        exchange_rate     = EXCLUDED.exchange_rate,
        cost_project_name = EXCLUDED.cost_project_name,
        currency_name     = EXCLUDED.currency_name,
        challan_qty       = EXCLUDED.challan_qty,
        rate              = EXCLUDED.rate,
        net_amount        = EXCLUDED.net_amount;
    """

    for inx, row in df.iterrows():
        values = (row['GRN Date'], row['Supplier Code'], row['Supplier Name'], row['Item Ctag Code'], row['Item Ctag Name'], row['Item Code'], row['Item Name'], row['UM'], row['Stock Type Name'], row['Grn  Number'], row['Purchase Order Number'], row['Department'], row['Department Name'], row['Indent Number'], row['Currency Code'], row['Exchange Rate'], row['Cost/Project'], row['Cost/Project Name'], row['Currency Name'], row['Challan Qty'], row['Rate'], row['Net Amount'])
        try:
            cursor.execute(insert_sql, values)
        except Exception as e:
            print(f"Error inserting row {inx}: {e}")
            continue
    return len(df)

# %%
def insert_issue_daily(cursor, filename, encoding):
    df = pd.read_csv(filename, header=5, skiprows=[6], encoding= encoding) 
    df.drop(df.columns[0], axis=1, inplace=True) 
    df.drop(df.index[-1], inplace=True)
    df['Issue date'] = df['Issue date'].apply(custom_date_parser)
    
    insert_sql = """INSERT INTO issue_daily_main (
        issue_date, item_category_code, item_category_name,
        department_code, department_name,
        item_code, cost_centre_code, cost_name,
        item_name, um, quantity, rate, value, stock_type_name
    ) VALUES (
        %s, %s, %s,
        %s, %s,
        %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
    ON CONFLICT (issue_date, item_code, cost_centre_code, department_code)
    DO UPDATE SET
        item_category_code = EXCLUDED.item_category_code,
        item_category_name = EXCLUDED.item_category_name,
        department_name    = EXCLUDED.department_name,
        cost_name          = EXCLUDED.cost_name,
        item_name          = EXCLUDED.item_name,
        um                 = EXCLUDED.um,
        quantity           = EXCLUDED.quantity,
        rate               = EXCLUDED.rate,
        value              = EXCLUDED.value,
        stock_type_name    = EXCLUDED.stock_type_name;
    """

    for inx, row in df.iterrows():
        values = (
            row['Issue date'], row['Item Category Code'], row['Item Category Name'],
            row['Department Code'], row['Department Name'],
            row['Item Code'], row['Cost Centre Code'], row['Cost Name'],
            row['Item Name'], row['UM'], row['Quantity'], row['Rate'], row['Value'], row['Stock Type Name']
        )
        try:
            cursor.execute(insert_sql, values)
        except Exception as e:
            print(f"Error inserting row {inx}: {e}")
            continue
    
    # Cleaning Logic: Remove redundancy in Category names
    cursor.execute("""
        UPDATE issue_daily_main
        SET item_category_name = TRIM(
            CASE 
                WHEN item_category_name LIKE item_category_code || ' %' 
                THEN SUBSTRING(item_category_name FROM LENGTH(item_category_code) + 2)
                ELSE item_category_name 
            END
        )
        WHERE item_category_code IS NOT NULL 
        AND item_category_name IS NOT NULL
        AND item_category_name LIKE item_category_code || ' %';
        """)
    return len(df)

# %%
def move_inserted_files(filename):
    base_dir = os.path.dirname(filename)
    new_dir = os.path.join(base_dir, 'Inserted Files')
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_path = os.path.join(new_dir, os.path.basename(filename))
    os.rename(filename, new_path)
    print(f"Moved {filename} to {new_path}")


def add_csv_attachments(msg, documents_path):
    attachment_count = 0
    file_prefixes = ['PUR', 'GRN', 'ISSUE']
    
    try:
        if not os.path.exists(documents_path):
            print(f"Warning: Directory {documents_path} does not exist")
            return 0
        
        # Find all CSV files with required prefixes
        csv_files = []
        for prefix in file_prefixes:
            pattern = os.path.join(documents_path, f"{prefix}*.csv")
            matching_files = glob.glob(pattern)
            csv_files.extend(matching_files)
        
        print(f"Found {len(csv_files)} CSV files to attach")
        
        # Add each file as attachment
        for file_path in csv_files:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                try:
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    # Encode file in ASCII characters to send by email    
                    encoders.encode_base64(part)
                    
                    # Add header as key/value pair to attachment part
                    filename = os.path.basename(file_path)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {filename}'
                    )
                    
                    # Attach the part to message
                    msg.attach(part)
                    attachment_count += 1
                    print(f"  ✓ Attached: {filename}")
                    
                except Exception as e:
                    print(f"  ✗ Failed to attach {os.path.basename(file_path)}: {e}")
            else:
                print(f"  ⚠ Skipped {os.path.basename(file_path)} (file not found or empty)")
    
    except Exception as e:
        print(f"Error processing attachments: {e}")
    
    return attachment_count


def send_email(completed):
    curr_date__ = datetime.now().strftime('%d-%m-%Y')
    print(f"Date: {curr_date__}")
    print("Mail Sending >>>>>>>>>>>>>>> starts")
    
    recipients_config = {
        'internal_team': EMAILS_INTERNAL,
        'clients': EMAILS_CLIENTS
    }
    
    subject = f'File Downloads - {curr_date__}'
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['Subject'] = subject
    
    if completed:
        recipients = recipients_config['clients'] + recipients_config['internal_team']
        msg.attach(MIMEText("All 3 Downloaded files are attached below.", 'plain'))
        msg['To'] = ', '.join(recipients_config['clients'])
        msg['Cc'] = ', '.join(recipients_config['internal_team'])
        
        attachment_count = add_csv_attachments(msg, ROOT_DOC_DIR)
        print(f"Internal notification with {attachment_count} attachments")
    else:
        recipients = recipients_config['internal_team']
        msg['To'] = ', '.join(recipients_config['internal_team'])
        msg.attach(MIMEText("Automation Download UNSUCCESSFUL. Check System!", 'plain'))
    
    # Send email
    return send_smtp_email(recipients, msg)

def send_smtp_email(recipients, msg):    
    try:
        with smtplib.SMTP(EMAIL_SERVER, 587) as session:
            session.starttls()
            # Login using redacted credentials
            session.login(EMAIL_SENDER, EMAIL_PASSWORD)
            session.sendmail(EMAIL_SENDER, recipients, msg.as_string())
        
        print(f"✅ Message sent successfully to {len(recipients)} recipients")
        return True
        
    except Exception as e:
        print(f"✗ Mail sending error: {e}")
    
    return False


def file_present(curr_dir):
    required_prefixes = ["PUR", "GRN", "ISSUE"]
    files_in_dir = [f for f in os.listdir(curr_dir) if f.lower().endswith(".csv")]
    missing = [prefix for prefix in required_prefixes if not any(f.startswith(prefix) for f in files_in_dir)]
    
    if missing:
        print(f"Missing files starting with: {', '.join(missing)}")
        
        for prefix in missing:
            print(f"Running automation for missing prefix: {prefix}")
            try:
                # Calls the automation script if files are missing
                result = subprocess.run(["python", "automation.py", "-s", prefix], check=True)
                print(f"Successfully ran automation for {prefix}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to run automation for {prefix}: {e}")
        
        files_in_dir_after = [f for f in os.listdir(curr_dir) if f.lower().endswith(".csv")]
        still_missing = [prefix for prefix in required_prefixes if not any(f.startswith(prefix) for f in files_in_dir_after)]
        
        if still_missing:
            send_email(False)
            return False
        else:
            send_email(True)
            return True
    else:
        print("All required files are present.")
        send_email(True)
        return True


# MAIN EXECUTION
curr_dir = os.path.abspath(ROOT_DOC_DIR)
file_present(curr_dir)

for file in os.listdir(curr_dir):
    if file.endswith('.csv'):
        file_path = os.path.join(curr_dir, file)
        try:
            with open(file_path, 'rb') as f:
                raw = f.read(100_000)
            guess = chardet.detect(raw)
            print(f"Processing file: {file} with encoding: {guess['encoding']}")
            
            if file.startswith('PUR'):
                insert_pur_daily(cursor, file_path, guess['encoding'])
            elif file.startswith('GRN'):
                insert_grn_daily(cursor, file_path, guess['encoding'])
            elif file.startswith('ISSUE'):
                insert_issue_daily(cursor, file_path, guess['encoding'])
            
            # Archive the file after processing
            move_inserted_files(file_path)
            
        except Exception as e:
            print(f"Failed to process {file}: {e}")
        
cursor.close()
# %%