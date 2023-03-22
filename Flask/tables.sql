You have multiple Excel files, each with multiple sheets.
You want to configure validation rules for each sheet and column of the Excel files, including checks for null values, PII data, and data transformations.
The validation rules should be configurable in a UI and should be stored in a database.
You want to keep an audit log of changes to the validation rules, and you want to implement a maker-checker process for approving changes.
You want to store the uploaded Excel files separately in a database table, along with details such as file name, location, and upload timestamp.
Based on these requirements, you could use the following table designs:

file_template table to store the configuration details for each sheet and column of the Excel files. This table could have columns for the template name, sheet names, column headers, and other relevant metadata.


CREATE TABLE file_template (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    template_name VARCHAR2(100) NOT NULL,
    sheet_names CLOB NOT NULL,
    column_headers CLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR2(100) NOT NULL,
    updated_by VARCHAR2(100) NOT NULL,
    status VARCHAR2(100) DEFAULT 'ACTIVE' NOT NULL
);


file_validation_config table to store the validation rules for each sheet and column of the Excel files. This table could have columns for the template ID, column name, PII status, null check status, data transformation, target date format, and column alias.

CREATE TABLE file_validation_config (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    template_id NUMBER NOT NULL,
    column_name VARCHAR2(100) NOT NULL,
    is_pii CHAR(1) DEFAULT 'N' NOT NULL,
    null_check CHAR(1) DEFAULT 'N' NOT NULL,
    transformation VARCHAR2(100),
    target_date_format VARCHAR2(100),
    column_alias VARCHAR2(100),
    CONSTRAINT fk_template FOREIGN KEY (template_id) REFERENCES file_template(id)
);


file_upload table to store the uploaded Excel files, along with details such as file name, location, and upload timestamp.

CREATE TABLE file_upload (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    file_name VARCHAR2(100) NOT NULL,
    file_location VARCHAR2(1000) NOT NULL,
    file_size NUMBER NOT NULL,
    uploaded_by VARCHAR2(100) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_template_id NUMBER NOT NULL,
    CONSTRAINT fk_file_template FOREIGN KEY (file_template_id) REFERENCES file_template(id)
);


file_validation_config_audit table to store the audit log of changes to the validation rules. This table could have columns for the configuration ID, old and new values, change type (e.g., update, delete), and the approver ID.

CREATE TABLE file_validation_config_audit (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    config_id NUMBER NOT NULL,
    old_value VARCHAR2(4000),
    new_value VARCHAR2(4000),
    change_type VARCHAR2(100) NOT NULL,
    approver_id VARCHAR2(100),
    approval_status VARCHAR2(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_config FOREIGN KEY (config_id) REFERENCES file_validation_config(id)
);


