# Conversation Thread

[35mTime: 2024-11-14 14:43:04
Role: user
Content: I have a question here. How do I เพิ่มสิทธิ์ Role & Permissions ระบบ OTC Sale???[0m
==================================================
[34mTime: 2024-11-14 14:43:09
Role: assistant
Content: 1. **Summary of the Case Incident:**
   The user is seeking guidance on how to add roles and permissions within the OTC Sale system.

2. **References Used:**
   - Article on "เพิ่มสิทธิ์ Role & Permissions ระบบ OTC Sale" from the knowledgebase.

3. **Application of Knowledgebase Information:**
   The article outlines a series of SQL commands necessary to add roles and permissions for users in the OTC Sale system. The steps include:
   - Identifying the role ID from the `TB_OTC_Role` table.
   - Identifying the company ID from the `TB_OTC_Company` table.
   - Checking if the user exists in the `TB_OTC_User` table and adding the user if not found.
   - Executing a stored procedure to add the user with the specified employee ID.
   - Adding the role to the user using another stored procedure.
   - Verifying the role assignment by querying the `TB_OTC_UserRoleCompany` table.

4. **Final Answer/Suggested Resolution:**
   To add roles and permissions in the OTC Sale system, follow these steps:
   1. Retrieve the `roleId` of the desired role from the `TB_OTC_Role` table.
   2. Retrieve the `CompanyId` of the company from the `TB_OTC_Company` table.
   3. Check if the user exists in `TB_OTC_User`:
      ```sql
      SELECT * FROM TB_OTC_User WHERE EmployeeId = 'your_employee_id';
      ```
   4. If the user does not exist, add the user:
      ```sql
      DECLARE @Employee_Ids NVARCHAR(MAX)
      SET @Employee_Ids = 'your_employee_id'; 
      EXEC [USP_AddUser_With_EmployeeId_To_OTCSale] @Employee_Ids;
      ```
   5. If the user exists, proceed to add the role:
      ```sql
      DECLARE @EmployeeId NVARCHAR(10) = N'your_employee_id';
      DECLARE @CompanyId NVARCHAR(20) = N'your_company_id';
      DECLARE @RoleId NVARCHAR(20) = N'your_role_id';
      EXEC [dbo].[USP_AddPermission_OTCSale] @EmployeeId, @CompanyId, @RoleId;
      ```
   6. Verify the role assignment:
      ```sql
      EXEC [USP_Check_User_In_OTCSale] @Company, 'your_employee_id';
      ```

   If you encounter any issues during this process, check the `TB_OTC_UserRoleCompany` table to see the existing roles and delete any incorrect assignments if necessary【4:0†source】.[0m
==================================================
