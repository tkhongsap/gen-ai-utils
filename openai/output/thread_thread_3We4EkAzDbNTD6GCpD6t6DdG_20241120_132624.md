# Conversation Thread

[35mTime: 2024-11-14 15:15:13
Role: user
Content: เพิ่มสิทธิ otc sale[0m
==================================================
[34mTime: 2024-11-14 15:15:17
Role: assistant
Content: ### Summary of the Case Incident
The request is to add permissions for the OTC Sale system. This involves modifying user roles and permissions within the system to enable specific functionalities for users.

### References Used
1. **OTC Sale Role & Permissions**: Instructions for adding user roles and permissions in the OTC Sale system【4:5†source】.
2. **Database Commands for Role Addition**: Specific SQL commands and procedures for adding a role to a user in the OTC Sale database【4:13†source】.

### Application of Knowledgebase Information
The knowledgebase provides detailed steps for adding roles and permissions in the OTC Sale system. It outlines the necessary SQL commands to select the appropriate role and user, as well as the procedures to add permissions. This includes checking if the user already exists, adding them if not, and then assigning the desired role.

### Suggested Resolution
To add permissions for OTC Sale, follow these steps:

1. **Identify the Role**:
   - Query the existing roles to find the `roleId` of the role you wish to add:
     ```sql
     SELECT * FROM TB_OTC_Role;
     ```

2. **Check User Existence**:
   - Verify if the user already exists in the database:
     ```sql
     SELECT * FROM TB_OTC_User WHERE EmployeeId = 'your_employee_id';
     ```

3. **Add User if Necessary**:
   - If the user does not exist, add them using:
     ```sql
     DECLARE @Employee_Ids NVARCHAR(MAX) = 'your_employee_id';
     EXEC [USP_AddUser_With_EmployeeId_To_OTCSale] @Employee_Ids;
     ```

4. **Assign Role**:
   - To assign the role to the user, execute:
     ```sql
     DECLARE @EmployeeId NVARCHAR(10) = 'your_employee_id';
     DECLARE @CompanyId NVARCHAR(20) = 'company_id';
     DECLARE @RoleId NVARCHAR(20) = 'role_id';
     EXEC [dbo].[USP_AddPermission_OTCSale] @EmployeeId, @CompanyId, @RoleId;
     ```

5. **Verify Role Assignment**:
   - Check if the role was successfully assigned:
     ```sql
     EXEC [USP_Check_User_In_OTCSale] @CompanyId, 'your_employee_id';
     ```

This process ensures that the user has the correct permissions to perform their tasks in the OTC Sale system. If any issues arise during this process, such as incorrect role assignments, they can be corrected by checking the `TB_OTC_UserRoleCompany` table and deleting any incorrect entries【4:13†source】.

Feel free to reach out if you need further assistance or clarification on any of these steps![0m
==================================================
[35mTime: 2024-11-14 15:20:55
Role: user
Content: ขอเพิ่มสิทธิ LE[0m
==================================================
[34mTime: 2024-11-14 15:21:03
Role: assistant
Content: ### Summary of the Case Incident
The request is to add permissions for the LE (Logistics Execution) system. This involves modifying user roles and permissions within the LE system to enable specific functionalities for users.

### References Used
1. **Adding User & Permission in LE**: Instructions for adding user roles and permissions in the LE system【8:2†source】.
2. **Database Commands for Role Addition**: Specific SQL commands and procedures for adding a role to a user in the LE database【8:16†source】.

### Application of Knowledgebase Information
The knowledgebase provides detailed steps for adding roles and permissions in the LE system. It outlines the necessary JSON structure required for user roles, how to generate this JSON from the database, and the specific commands to insert or update user roles in the database.

### Suggested Resolution
To add permissions for the LE system, follow these steps:

1. **Generate User JSON**:
   - Use the following SQL command to generate the JSON for the user:
     ```sql
     SELECT  
         CAST(Contactid AS NVARCHAR) AS _id,  
         EmployeeId AS employeeid,  
         ADUserId AS aduserid,  
         EmployeeTag AS employeetag,  
         LocalFirstName AS localfirstname,  
         LocalLastName AS locallastname,  
         FirstName AS firstname,  
         LastName AS lastname 
     FROM CommonDB.dbo.TB_CTC_Contact  
     WHERE EmployeeId = 'your_employee_id' 
     FOR JSON PATH, WITHOUT_ARRAY_WRAPPER;
     ```

2. **Modify the JSON for Permissions**:
   - Ensure the JSON includes the necessary role and permissions. For example:
     ```json
     {
         "_id": "1105805",
         "employeeid": "70090572",
         "aduserid": "70090572",
         "employeetag": "L88272",
         "localfirstname": "ศิรินันท์",
         "locallastname": "รังเพชร",
         "firstname": "Sirinan",
         "lastname": "Rangphet",
         "companies": [
             {
                 "code": "5700",
                 "permissions": [
                     "read",
                     "create",
                     "edit",
                     "cancel",
                     "approve"
                 ]
             }
         ]
     }
     ```

3. **Insert Data into the LE Database**:
   - Add the generated JSON data into the `Users` collection within the LE database. Use the following command:
     ```javascript
     db.Users.insertOne(your_generated_json);
     ```

4. **Verify the Role Assignment**:
   - Check if the user has the correct permissions assigned by querying the `Users` collection:
     ```javascript
     db.Users.find({_id: "your_user_id"});
     ```

This process ensures that the user has the correct permissions to perform their tasks in the LE system. If any issues arise during this process, such as incorrect role assignments, they can be corrected by checking the relevant permissions in the database【8:3†source】【8:5†source】.

If you have any further questions or need additional assistance, feel free to ask![0m
==================================================
[35mTime: 2024-11-14 15:21:56
Role: user
Content: ขอ connection database le dev[0m
==================================================
[34mTime: 2024-11-14 15:21:59
Role: assistant
Content: ### Summary of the Case Incident
The request is for the connection details to the LE (Logistics Execution) development database. This information is essential for accessing the database for development, testing, or troubleshooting purposes.

### References Used
1. **Database Connection Information for LE**: Specific details on how to connect to the LE development database【12:0†source】.
2. **Accessing MongoDB for LE**: Instructions on how to connect to the MongoDB instance used for LE【12:1†source】.

### Application of Knowledgebase Information
The knowledgebase outlines the connection details and procedures for accessing the LE development database. It includes the necessary credentials, database names, and the specific collections that are relevant for development tasks. 

### Suggested Resolution
To connect to the LE development database, follow these steps:

1. **MongoDB Connection**:
   - Use the following connection string format for MongoDB:
     ```
     mongodb://<username>:<password>@<host>:<port>/<database>
     ```
   - Replace `<username>`, `<password>`, `<host>`, `<port>`, and `<database>` with your actual connection details.

2. **Database and Collection Access**:
   - After connecting to MongoDB, you can access the relevant collections for LE, such as:
     - `DocumentInfo`
     - `ItemInventory`
     - `ProduceOMLogs`
   - Example command to access a collection:
     ```javascript
     use('OTCInterface');
     db.DocumentInfo.find({});
     ```

3. **Verify Connection**:
   - After establishing the connection, run a simple query to verify that you are connected properly and can access data:
     ```javascript
     db.DocumentInfo.findOne();
     ```

If you encounter any issues during the connection process, ensure that the credentials and connection string are correct, and that your network allows access to the database server.

Feel free to reach out if you need further assistance with connecting to the database or any other related queries![0m
==================================================
