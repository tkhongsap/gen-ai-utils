# Conversation Thread

[35mTime: 2024-11-14 14:52:17
Role: user
Content: TO ไม่อัพเดต ทำอย่างไรได้บ้าง[0m
==================================================
[34mTime: 2024-11-14 14:52:20
Role: assistant
Content: ### Summary of the Case Incident
The user is experiencing issues with a Transport Order (TO) that is not updating properly in the system.

### References Used
1. **TO cancel ไม่ได้ ในระบบ LE** - discusses the potential reasons and checks for issues related to Transport Orders not updating or being canceled.
2. **LE ต้องไม่มีค้างขน แต่หน้าเว็บแสดงค้างขนผิด** - provides guidance on how to check and update database fields related to TOs.

### Application of Knowledgebase Information
From the knowledgebase, the following steps can be taken to troubleshoot and resolve the issue of the TO not updating:

1. **Check Web Socket Connection**: Ensure that the web application can connect to the web socket. This can be done by pressing F12 to open the developer tools, navigating to the Network tab, filtering for "ws", and checking that the status is 101 (indicating a successful connection).

2. **Verify SAP Cancellation**: If the issue involves canceling a TO, check whether the cancellation was successful in the SAP system. If it was, the data in the LE database (specifically in the `DocumentInfo` collection) should reflect this. The field `Transports.DO.State` should show the status as `SAPCanceled`.

3. **Update Database Fields**: If the cancellation was successful but the TO is still not updating, you may need to manually update the relevant fields in the database. For example, ensure that the fields related to remaining quantities and amounts are correctly set to zero if applicable.

### Conclusion and Suggested Resolution
To resolve the issue of the TO not updating:
1. Verify that the web application can connect to the web socket.
2. Check the status of the TO in the SAP system and ensure that it reflects the correct cancellation state.
3. If necessary, manually update the relevant fields in the `DocumentInfo` collection to ensure that they reflect the correct status.

If the above steps do not resolve the issue, consider reaching out to your technical team for further assistance with database updates or system configurations.[0m
==================================================
[35mTime: 2024-11-14 14:55:16
Role: user
Content: เลข DO มีปัญหา ตรวจสอบตรงไหนได้บ้า[0m
==================================================
[34mTime: 2024-11-14 14:55:19
Role: assistant
Content: ### Summary of the Case Incident
The user is facing issues with the Delivery Order (DO) number, indicating that there might be a problem with the DO that needs to be investigated.

### References Used
1. **เลข DO มีปัญหา** - provides steps to check and troubleshoot issues related to DO numbers.
2. **รายงานขนเลข DO ออกไม่ถูก SALE/CNDN_DELIVDOC** - includes SQL queries to verify the accuracy of DO numbers and related documents.

### Application of Knowledgebase Information
To troubleshoot issues with the DO number, the following steps can be followed based on the knowledgebase:

1. **Check the Database**: Use the LEDocumentNumber associated with the DO to query the relevant database table. This can be done using the following SQL query:
   ```sql
   use RPT_Sales_OR;
   select * from RPT_OTC_Transport_Detail with(nolock) Where LEDocumentNumber = 'your_document_number';
   ```

2. **Verify DOId**: After running the query, check if the DOId matches the one provided. If there is a discrepancy, you may need to delete the incorrect entry and reprocess the DO:
   ```sql
   delete from RPT_OTC_Transport_Detail Where TransportOrders_TransportOrderId = 'your_transport_order_id';
   ```

3. **Check Status in TOMS**: Ensure that the status in TOMS is accurate. If the status is showing as "All Assigned," it may indicate that the data needs to be re-produced or refreshed in the system:
   - Check the status using:
   ```sql
   select * from TB_FTD_LE_Order_TransportOrders with(nolock) Where LEDocumentNumber = 'your_document_number';
   ```

4. **Reproduce the DO**: If the DO is not showing up correctly, you may need to reproduce the document in the system. Ensure that the state of the document in the MongoDB collection `DocumentInfo` is set to `TOComplete` before reproducing it.

### Conclusion and Suggested Resolution
To resolve the issue with the DO number:
1. Execute the SQL queries provided to check the status and details of the DO.
2. Verify that the DOId is correct and matches the expected values.
3. If discrepancies are found, delete the incorrect entries and reprocess the DO.
4. If necessary, reproduce the DO in the system ensuring the document state is correct.

If the issue persists after following these steps, consider escalating the matter to your technical team for further investigation.[0m
==================================================
[35mTime: 2024-11-14 14:56:59
Role: user
Content: รายงานขนเลข DO ออกไม่ถูก SALE[0m
==================================================
[34mTime: 2024-11-14 14:57:02
Role: assistant
Content: ### Summary of the Case Incident
The user is reporting that the Delivery Order (DO) numbers are not being generated correctly in the sales reports.

### References Used
1. **รายงานขนเลข DO ออกไม่ถูก SALE/CNDN_DELIVDOC** - provides steps to verify the accuracy of DO numbers in the database.
2. **ตรวจสอบเลข DO** - discusses how to check the transport order details in the database to ensure the correct DO number is being used.

### Application of Knowledgebase Information
Based on the knowledgebase, the following steps can be taken to troubleshoot the issue with the DO numbers:

1. **Check the Database for Transport Order Details**: Use the following SQL query to check the details of the transport order:
   ```sql
   use RPT_Sales_OR; 
   select TransportOrders_TransportOrderId, DOId, * from RPT_OTC_Transport_Detail_LE with(nolock) Where TransportOrders_TransportOrderId = 'your_transport_order_id';
   ```
   Replace `'your_transport_order_id'` with the actual transport order ID you are investigating.

2. **Verify DOId**: After running the above query, check if the `DOId` matches the expected values. If it does not match, it indicates that there is an issue with the DO generation.

3. **Update Inventory Fields**: If discrepancies are found in the quantities or amounts associated with the DO, you may need to update the relevant fields in the `ItemInventory` collection. Ensure that the following fields are correctly set:
   - `QuantityRemaining`
   - `QuantityApprovedRemaining`
   - `AmountRemaining`
   - `VatRemaining`
   - `DiscountRemaining`

4. **Cross-Check with Reports**: Open the OTCSale web interface and navigate to the LE → AfterSale → Report section to compare the generated reports with the expected values.

### Conclusion and Suggested Resolution
To resolve the issue with the incorrect DO numbers in the sales reports:
1. Execute the SQL query to check the transport order details and verify the `DOId`.
2. If discrepancies are found, update the relevant fields in the `ItemInventory` collection as needed.
3. Finally, cross-check the reports in the OTCSale web interface to ensure consistency with the database information.

If the issue persists, consider escalating it to your technical team for further investigation and resolution【12:1†source】.[0m
==================================================
[35mTime: 2024-11-14 15:05:00
Role: user
Content: ใบกำกับภาษีพิมพ์ไม่ออก[0m
==================================================
[34mTime: 2024-11-14 15:05:04
Role: assistant
Content: ### Summary of the Case Incident
The user is experiencing issues with printing the tax invoice, indicating that the invoice is not being printed correctly or is missing from the system.

### References Used
1. **ปริ๊นใบกำกับภาษีไม่ได้** - provides steps to check if the tax invoice document exists and how to resolve issues related to printing.

### Application of Knowledgebase Information
To troubleshoot the issue with printing the tax invoice, follow these steps based on the knowledgebase:

1. **Check Document Management System**: Access the ThaiBev Document Management system (docdev) to verify if the tax invoice document exists. You can search for the document using the FIDoc number:
   - Go to the **ThaiBev Document Management** system.
   - Search for the document using the FIDoc number to see if the tax invoice is available.

2. **Explore Tax Invoice Folder**: If the document is not found in the Document Management system, check the folder structure where tax invoices are stored:
   - Navigate to the **File Explorer**.
   - Go to the folder path **TaxInvoices** > **Year** > **Month** > **Day**.
   - Search for the tax invoice using the invoice number.

3. **Delete and Retry Printing**: If you find the tax invoice document within the folder:
   - Delete the existing document.
   - Attempt to print the tax invoice again to see if it resolves the issue.

### Conclusion and Suggested Resolution
To resolve the issue of the tax invoice not printing:
1. Check the ThaiBev Document Management system for the existence of the tax invoice using the FIDoc number.
2. If not found, explore the TaxInvoices folder for the document.
3. If the document exists, delete it and retry printing the invoice.

If the problem persists after following these steps, further investigation may be needed, potentially involving the technical support team to check for any system errors or configurations affecting the printing process【16:12†source】.[0m
==================================================
[35mTime: 2024-11-14 15:08:08
Role: user
Content: user ขอเพิ่มสิทธการเข้าถุง[0m
==================================================
[34mTime: 2024-11-14 15:08:13
Role: assistant
Content: ### Summary of the Case Incident
The user is requesting to add permissions for accessing certain functionalities or areas in the system, specifically related to the "ถุง" (bag) access.

### References Used
1. **เพิ่มสิทธิ์ Role & Permissions ระบบ OTC Sale** - outlines the steps to add roles and permissions for users in the OTC Sale system.
2. **เพิ่มสิทธิ์ Role & Permissions ระบบ OTC LE** - provides guidance on how to manage user permissions within the OTC LE system.

### Application of Knowledgebase Information
To grant additional access rights for the user, follow these steps based on the knowledgebase:

1. **Identify the Role and Company**:
   - First, identify the `roleId` of the role you want to add by executing:
     ```sql
     select * from TB_OTC_Role;
     ```
   - Note down the `CompanyId` of the company you wish to associate with the user:
     ```sql
     select * from TB_OTC_Company;
     ```

2. **Check Existing User**:
   - Verify if the user already exists in the system by running:
     ```sql
     select * from TB_OTC_User where EmployeeId = 'your_employee_id';
     ```
   - Replace `'your_employee_id'` with the actual employee ID.

3. **Add User if Not Found**:
   - If the user does not exist, add them using:
     ```sql
     Declare @Employee_Ids NVARCHAR(MAX);   
     Set @Employee_Ids = 'your_employee_id';  // Replace with actual ID
     EXEC [USP_AddUser_With_EmployeeId_To_OTCSale] @Employee_Ids;
     ```

4. **Assign Role to User**:
   - After ensuring the user exists, add the role using:
     ```sql
     Declare @EmployeeId NVARCHAR(10) = N'your_employee_id';  // Replace with actual ID
     Declare @CompanyId NVARCHAR(20) = N'your_company_id';  // Replace with actual Company ID
     Declare @RoleId NVARCHAR(20) = N'your_role_id';  // Replace with actual Role ID
     EXEC [dbo].[USP_AddPermission_OTCSale] @EmployeeId, @CompanyId, @RoleId;
     ```

5. **Verify Permissions**:
   - Finally, check if the role was added correctly by querying:
     ```sql
     select * from TB_OTC_UserRoleCompany where UserId = your_user_id and CompanyId = your_company_id;
     ```

### Conclusion and Suggested Resolution
To add access rights for the specified user:
1. Identify the necessary role and company ID.
2. Check if the user already exists; if not, add them.
3. Assign the appropriate role to the user.
4. Verify the permissions to ensure they were correctly applied.

If further assistance is required, consider consulting with your system administrator or technical support team for additional help【20:2†source】.[0m
==================================================
