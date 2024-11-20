# Conversation Thread

[35mTime: 2024-11-14 14:46:56
Role: user
Content: how do I solve this issue? my PM asked me. เพิ่มสิทธิ์ Role & Permissions ระบบ OTC Sale[0m
==================================================
[34mTime: 2024-11-14 14:46:58
Role: assistant
Content: To address the issue of adding role and permissions in the OTC Sale system, I will first search the uploaded files for relevant information regarding role and permission management. 

Let's begin by searching for terms related to "Role & Permissions" and "OTC Sale" in the provided documents. 

I'll conduct the search now.[0m
==================================================
[34mTime: 2024-11-14 14:47:00
Role: assistant
Content: ### Summary of the Case Incident
The request is to add role and permissions for the OTC Sale system. This involves updating the database to assign specific roles to users, ensuring they have the necessary permissions to perform their tasks within the system.

### References Used
1. **Document Title**: เพิ่มสิทธิ์ Role & Permissions ระบบ OTC Sale
   - Content: Steps to add roles and permissions in the OTC Sale database.
2. **Document Title**: เพิ่มสิทธิ์ Role & Permissions ระบบ OTC Sale (continued)
   - Content: Detailed SQL commands and procedures for adding user roles and permissions.

### Application of Knowledgebase Information
The knowledgebase provides a structured method for adding roles and permissions in the OTC Sale system. The following steps are outlined:
1. **Identify Role ID**: Use the command `select * from TB_OTC_Role;` to find the Role ID of the desired role.
2. **Identify Company ID**: Use the command `select * from TB_OTC_Company;` to find the Company ID for the company you want to add the role to.
3. **Check User Existence**: Verify if the user exists in the system with `select * from TB_OTC_User where EmployeeId = '70090572';` (replace with the actual Employee ID).
4. **Add User if Not Found**: If the user does not exist, add them using:
   ```sql
   Declare @Employee_Ids NVARCHAR(MAX)   
   Set @Employee_Ids = '70090572'  // Change according to user 
   EXEC [USP_AddUser_With_EmployeeId_To_OTCSale] @Employee_Ids;
   ```
5. **Assign Role to User**: If the user exists, assign the role using:
   ```sql
   Declare @EmployeeId NVARCHAR(10) = N'70090572';  // Change according to user 
   Declare @CompanyId NVARCHAR(20) = N'2';  // Change according to company 
   Declare @RoleId NVARCHAR(20) = N'15';  // Change according to role 
   EXEC [dbo].[USP_AddPermission_OTCSale] @EmployeeId, @CompanyId, @RoleId;
   ```
6. **Verify Role Assignment**: Finally, check if the role has been assigned correctly:
   ```sql
   EXEC [USP_Check_User_In_OTCSale] @Company, '70090572'; // Change according to user
   ```

### Conclusion and Suggested Resolution
To resolve the issue of adding role and permissions for the OTC Sale system, follow the structured steps provided in the knowledgebase. Ensure to replace the placeholder values with actual data relevant to the user and company. This approach will facilitate a smooth update of roles and permissions, allowing users to have the necessary access to perform their tasks efficiently.

If you encounter any issues during these steps, please provide the specific error messages or problems, and I will assist you further.[0m
==================================================
