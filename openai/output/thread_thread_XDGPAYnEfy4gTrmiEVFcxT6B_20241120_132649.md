# Conversation Thread

[35mTime: 2024-11-05 11:21:38
Role: user
Content: ช่วย list ชื่อ table ที่เกี่ยวข้องใน Scipt นี้ทั้งหมดให้หน่อย

---------------Check BEER-----------------
DECLARE @ParamDateFrom date = DATEADD(dd,-(DAY(DATEADD(mm,1, CAST(GETDATE() as date)))-1),DATEADD(mm,0,CAST(GETDATE() as date))) --21/06/2024 สร้างตัวแปร ในการเริ่มต้นลบตั้งแต่ต้นเดือน
	DECLARE @ParamDateEnd date = DATEADD(dd,-(DAY(DATEADD(mm,1, CAST(GETDATE() as date)))-1),DATEADD(mm,1,CAST(GETDATE() as date))) --21/06/2024 สร้างตัวแปร ในการเริ่มต้นลบตั้งแต่ต้นเดือน
 
	
		   SELECT distinct rpd.OrderRank AS [ลำดับ]
			,soc.CustomerCode AS [รหัสร้านค้า]
			, c.CustomerName AS [ชื่อร้านค้า]
			, re.RegionGroupName AS [ภาค]
			, sal.SalesUnitDesc AS [หน่วยขาย]
			, branch.BranchGroupName AS [สาขา]
			, su.LocalFirstName + ' ' + su.LocalLastName AS [Sale ที่ดูแล]
			, su.EmployeeId AS [Sale ID]
			, rp.AssignedDate /* FORMAT(rp.AssignedDate, 'dd/MM/yyyy HH:MM:ss')*/ AS [แผนวันที่]
			--, FORMAT(@dateFrom, 'dd/MM/yyyy HH:MM:ss') AS [Start Month]
			--, FORMAT(@dateTo, 'dd/MM/yyyy HH:MM:ss') AS [End Month]
			,ISNULL(cc.CustomerCatDesc, '') AS [ประเภทร้านค้า]
			,c.Latitude,c.Longitude,MAX(v.OnDate) AS N'วันที่อัพเดทพิกัด',CASE WHEN c.ActiveFlag=1 THEN N'ปกติ' ELSE N'เลิกติดต่อ' END  AS N'สถานะ การติดต่อ'
			--FROM dbo.TB_VSMS_HierarchySalesTeam h
			--INNER JOIN dbo.TB_VSMS_Territory t ON t.SalesTeamId = h.SalesTeamId AND t.DelFlag=0
			--INNER JOIN dbo.TB_VSMS_TerritorialSalesPerson ts ON ts.TerritoryId =t.TerritoryId AND ts.delflag=0 AND CONVERT(DATE, GETDATE(),103)  BETWEEN ts.FromDate AND ts.ToDate			
			FROM [dbo].[Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking] s 
			LEFT JOIN [dbo].[Survey_VSMS_TBV_TB_VSMS_RegionGroup] re
                        ON re.RegionGroupId = s.RegionGroupId AND re.DelFlag = 0
			INNER JOIN [dbo].[Survey_VSMS_TBV_TB_VSMS_SalesTeam] sal ON sal.SalesTeamId = s.SalesTeamId AND sal.DelFlag = 0
			INNER JOIN [dbo].[Survey_VSMS_TBV_TB_VSMS_BranchGroup] branch  ON branch.BranchGroupId = s.BranchGroupId AND branch.DelFlag = 0
			INNER JOIN [dbo].[Survey_VSMS_TBV_TB_SYS_User] su ON s.UserId=su.UserId AND su.DelFlag=0
			INNER JOIN [dbo].[Sales_VSMS_TBV_TB_VSMS_Route] r ON r.TerritoryId=s.TerritoryId --AND r.DelFlag=0
			--INNER JOIN dbo.TB_VSMS_RouteCustomer rc ON rc.RouteId = r.RouteId AND rc.DelFlag=0
			--INNER JOIN dbo.TB_VSMS_RoutePlan rp ON rp.RouteId=r.RouteId AND rp.DelFlag=0 AND rp.AssignedDate BETWEEN @dateFrom AND @dateTo
			INNER JOIN [dbo].[Sales_VSMS_TBV_TB_VSMS_RoutePlan] rp ON rp.UserId = su.UserId AND rp.DelFlag=0 AND rp.AssignedDate >= @ParamDateFrom AND rp.AssignedDate < @ParamDateEnd 
				AND rp.RouteId = r.RouteId
			INNER JOIN [dbo].[Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail] rpd ON rpd.RoutePlanId=rp.RoutePlanId AND rpd.DelFlag=0
			INNER JOIN [dbo].[Survey_VSMS_TBV_TB_VSMS_SOCustomer] soc ON rpd.SOCustomerId=soc.SOCustomerId AND soc.DelFlag=0 AND soc.CustomerCode <> ''
			INNER JOIN [dbo].[Survey_VSMS_TBV_TB_VSMS_Customer] c ON c.CustomerId=soc.CustomerId AND c.DelFlag=0
			LEFT JOIN [dbo].[Survey_VSMS_TBV_TB_VSMS_BranchedCustomer] bc ON bc.SOCustomerId = soc.SOCustomerId  AND bc.BranchGroupId =s.BranchGroupId AND  bc.DelFlag = 0
			LEFT JOIN [dbo].[Survey_VSMS_TBV_TB_VSMS_ChannelCategory] cc ON cc.ChannelCatId = bc.ChannelCatId
			LEFT JOIN [Sales_VSMS_TBV_TB_VSMS_CustomerVisit] v ON soc.SOCustomerId = v.SOCustomerId   AND rp.AssignedDate = cast(v.OnDate as Date) AND v.VisitType = 2 AND v.OnDate >  '2022-12-01 00:00:00.000'
			--AND v.VisitType = 2 AND v.OnDate >  '2022-12-01 00:00:00.000'
			WHERE s.OnDate >= @ParamDateFrom AND s.OnDate < @ParamDateEnd 
			AND s.ChannelId <> 9
			--WHERE s.RegionGroupId = @GroupId AND s.SalesTeamId = @SalesTeamId --AND fc.BranchGroupId IS NOT NULL
			--ORDER BY sal.SalesUnitDesc, su.EmployeeId, rp.AssignedDate
			AND s.ChannelId in (12,19,25)
 
			GROUP BY rpd.OrderRank
			, soc.CustomerCode
			, c.CustomerName
			, re.RegionGroupName
			, sal.SalesUnitDesc
			, branch.BranchGroupName
			, su.LocalFirstName + ' ' + su.LocalLastName
			, su.EmployeeId
			, rp.AssignedDate,c.Latitude,c.Longitude,cc.CustomerCatDesc,c.ActiveFlag[0m
==================================================
[34mTime: 2024-11-05 11:21:40
Role: assistant
Content: ใน Script ที่คุณได้แสดงให้ดู มีการเรียกใช้หลาย Table ใน SQL Query นั้น โดยผมจะ list ชื่อ table ทั้งหมดที่เกี่ยวข้องให้ด้านล่างนี้:

1. **Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking** (ใช้ alias `s`)
2. **Survey_VSMS_TBV_TB_VSMS_RegionGroup** (ใช้ alias `re`)
3. **Survey_VSMS_TBV_TB_VSMS_SalesTeam** (ใช้ alias `sal`)
4. **Survey_VSMS_TBV_TB_VSMS_BranchGroup** (ใช้ alias `branch`)
5. **Survey_VSMS_TBV_TB_SYS_User** (ใช้ alias `su`)
6. **Sales_VSMS_TBV_TB_VSMS_Route** (ใช้ alias `r`)
7. **Sales_VSMS_TBV_TB_VSMS_RoutePlan** (ใช้ alias `rp`)
8. **Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail** (ใช้ alias `rpd`)
9. **Survey_VSMS_TBV_TB_VSMS_SOCustomer** (ใช้ alias `soc`)
10. **Survey_VSMS_TBV_TB_VSMS_Customer** (ใช้ alias `c`)
11. **Survey_VSMS_TBV_TB_VSMS_BranchedCustomer** (ใช้ alias `bc`)
12. **Survey_VSMS_TBV_TB_VSMS_ChannelCategory** (ใช้ alias `cc`)
13. **Sales_VSMS_TBV_TB_VSMS_CustomerVisit** (ใช้ alias `v`)

ดังนั้น ชื่อ table ทั้งหมดที่เกี่ยวข้องใน Script นี้ ได้แก่:

- Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking
- Survey_VSMS_TBV_TB_VSMS_RegionGroup
- Survey_VSMS_TBV_TB_VSMS_SalesTeam
- Survey_VSMS_TBV_TB_VSMS_BranchGroup
- Survey_VSMS_TBV_TB_SYS_User
- Sales_VSMS_TBV_TB_VSMS_Route
- Sales_VSMS_TBV_TB_VSMS_RoutePlan
- Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail
- Survey_VSMS_TBV_TB_VSMS_SOCustomer
- Survey_VSMS_TBV_TB_VSMS_Customer
- Survey_VSMS_TBV_TB_VSMS_BranchedCustomer
- Survey_VSMS_TBV_TB_VSMS_ChannelCategory
- Sales_VSMS_TBV_TB_VSMS_CustomerVisit

หากคุณต้องการให้ช่วยในส่วนอื่น ๆ ของ Script นี้ เช่น การปรับแต่งหรือแก้ไขข้อผิดพลาด สามารถบอกได้เลยครับ![0m
==================================================
[35mTime: 2024-11-05 11:22:36
Role: user
Content: ช่วยสร้าง script SQL สำหรับตรวจสอบจำนวนของตารางด้านบนให้หน่อย[0m
==================================================
[34mTime: 2024-11-05 11:22:39
Role: assistant
Content: ในการตรวจสอบจำนวนของแถวในแต่ละตารางที่คุณได้แสดงไว้ใน SQL Query ก่อนหน้านี้ คุณสามารถใช้คำสั่ง `SELECT COUNT(*)` เพื่อหาจำนวนแถวของแต่ละตารางได้ นี่คือ Script SQL ที่สามารถใช้ตรวจสอบจำนวนแถวของแต่ละตาราง:

```sql
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking]
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_RegionGroup' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_RegionGroup]
WHERE 
    DelFlag = 0
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_SalesTeam' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_SalesTeam]
WHERE 
    DelFlag = 0
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_BranchGroup' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_BranchGroup]
WHERE 
    DelFlag = 0
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_SYS_User' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_SYS_User]
WHERE 
    DelFlag = 0
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_Route' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Sales_VSMS_TBV_TB_VSMS_Route]
WHERE 
    DelFlag = 0
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_RoutePlan' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Sales_VSMS_TBV_TB_VSMS_RoutePlan]
WHERE 
    DelFlag = 0
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail]
WHERE 
    DelFlag = 0
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_SOCustomer' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_SOCustomer]
WHERE 
    DelFlag = 0 AND CustomerCode <> ''
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_Customer' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_Customer]
WHERE 
    DelFlag = 0
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_BranchedCustomer' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_BranchedCustomer]
WHERE 
    DelFlag = 0
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_ChannelCategory' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_ChannelCategory]
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_CustomerVisit' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Sales_VSMS_TBV_TB_VSMS_CustomerVisit]
WHERE 
    VisitType = 2 AND OnDate > '2022-12-01 00:00:00.000';
```

### คำอธิบายเกี่ยวกับ Script:
1. **COUNT(*)**: ใช้ในการนับจำนวนแถวในแต่ละตาราง
2. **UNION ALL**: ใช้ในการรวมผลลัพธ์จากหลาย SELECT statements เข้าด้วยกัน
3. **WHERE Clauses**: นำมาใช้เพื่อกรองข้อมูลให้ตรงตามเงื่อนไขที่กำหนด เช่น `DelFlag = 0 หรือ VisitType = 2`

คุณสามารถทำการรัน Script นี้ในฐานข้อมูลของคุณ เพื่อดูจำนวนแถวในแต่ละตารางที่ได้ระบุไว้ หากต้องการความช่วยเหลือเพิ่มเติม สามารถสอบถามได้เลยครับ![0m
==================================================
[35mTime: 2024-11-05 11:23:06
Role: user
Content: ไม่เอา where [0m
==================================================
[34mTime: 2024-11-05 11:23:07
Role: assistant
Content: ได้ครับ! หากคุณไม่ต้องการใช้เงื่อนไขใน `WHERE` clause สำหรับการนับจำนวนแถวในแต่ละตาราง สามารถใช้ Script SQL ด้านล่างนี้ได้:

```sql
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking]
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_RegionGroup' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_RegionGroup]
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_SalesTeam' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_SalesTeam]
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_BranchGroup' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_BranchGroup]
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_SYS_User' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_SYS_User]
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_Route' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Sales_VSMS_TBV_TB_VSMS_Route]
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_RoutePlan' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Sales_VSMS_TBV_TB_VSMS_RoutePlan]
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail]
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_SOCustomer' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_SOCustomer]
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_Customer' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_Customer]
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_BranchedCustomer' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_BranchedCustomer]
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_ChannelCategory' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Survey_VSMS_TBV_TB_VSMS_ChannelCategory]
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_CustomerVisit' AS TableName,
    COUNT(*) AS RowCount
FROM 
    [dbo].[Sales_VSMS_TBV_TB_VSMS_CustomerVisit];
```

### คำอธิบาย:
- Script นี้จะทำการนับจำนวนแถวในแต่ละตาราง โดยไม่มีการกรองข้อมูลใด ๆ
- ผลลัพธ์ที่ได้จะบอกจำนวนแถวในแต่ละตารางที่มีอยู่ทั้งหมดในฐานข้อมูล

คุณสามารถรัน Script นี้ในฐานข้อมูลของคุณได้เลย หากมีคำถามเพิ่มเติมหรือต้องการความช่วยเหลือในเรื่องอื่น ๆ สามารถแจ้งได้ครับ![0m
==================================================
[35mTime: 2024-11-05 11:26:40
Role: user
Content: ปรับให้สามารถรันที่ sql server ได้หรือไม่[0m
==================================================
[34mTime: 2024-11-05 11:26:42
Role: assistant
Content: แน่นอนครับ! Script ที่ให้ไปก่อนหน้านี้ต้องใช้ใน SQL Server ได้เลย แต่หากต้องการตรวจสอบจำนวนแถวในแต่ละตารางให้เหมาะสมกับ SQL Server และทำให้แน่ใจว่า Syntax ถูกต้อง เราสามารถใช้ `[dbo].` เหมือนในตัวอย่างที่กำหนดไว้ก่อนหน้านี้

นี่คือ Script SQL ที่สามารถรันได้ที่ SQL Server:

```sql
-- ตรวจสอบจำนวนแถวในแต่ละตาราง
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking]) AS RowCount
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_RegionGroup' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Survey_VSMS_TBV_TB_VSMS_RegionGroup]) AS RowCount
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_SalesTeam' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Survey_VSMS_TBV_TB_VSMS_SalesTeam]) AS RowCount
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_BranchGroup' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Survey_VSMS_TBV_TB_VSMS_BranchGroup]) AS RowCount
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_SYS_User' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Survey_VSMS_TBV_TB_SYS_User]) AS RowCount
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_Route' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Sales_VSMS_TBV_TB_VSMS_Route]) AS RowCount
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_RoutePlan' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Sales_VSMS_TBV_TB_VSMS_RoutePlan]) AS RowCount
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail]) AS RowCount
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_SOCustomer' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Survey_VSMS_TBV_TB_VSMS_SOCustomer]) AS RowCount
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_Customer' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Survey_VSMS_TBV_TB_VSMS_Customer]) AS RowCount
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_BranchedCustomer' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Survey_VSMS_TBV_TB_VSMS_BranchedCustomer]) AS RowCount
UNION ALL
SELECT 
    'Survey_VSMS_TBV_TB_VSMS_ChannelCategory' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Survey_VSMS_TBV_TB_VSMS_ChannelCategory]) AS RowCount
UNION ALL
SELECT 
    'Sales_VSMS_TBV_TB_VSMS_CustomerVisit' AS TableName,
    (SELECT COUNT(*) FROM [dbo].[Sales_VSMS_TBV_TB_VSMS_CustomerVisit]) AS RowCount;
```

### การปรับตัวใช้ที่ SQL Server:
1. **Subquery**: ใช้ Subquery ในการนับจำนวนแถวแต่ละตารางแทนการใช้ `COUNT(*)` โดยตรงใน Select หลัก
2. **UNION ALL**: ใช้ในการรวมผลลัพธ์จากทุกตารางเข้าด้วยกัน โดยไม่ต้องมีการกรอง

ให้แน่ใจว่าคุณได้เลือก Database ที่ถูกต้องใน SQL Server ก่อนทำการรัน Script นี้ครับ หากมีคำถามเพิ่มเติมหรือช่วยเหลือในเรื่องอื่น ๆ สามารถสอบถามได้ครับ![0m
==================================================
[35mTime: 2024-11-05 11:29:12
Role: user
Content: ปรับให้สามารถใช้งานที่ tidb database [0m
==================================================
[34mTime: 2024-11-05 11:29:13
Role: assistant
Content: เพื่อทำให้ SQL Script ที่เรามีก่อนหน้านี้ทำงานได้ใน TiDB database ควรปรับ Syntax เล็กน้อย เนื่องจาก TiDB มีข้อควรระวังเกี่ยวกับการจัดการการรวม และอาจไม่อนุญาตให้ใช้ `UNION ALL` พร้อมกับ Subqueries ลงใน `SELECT` statement แบบนี้ ในกรณีนี้เราจะใช้ `WITH` clause เพื่อให้สามารถใช้ common table expressions (CTEs) ได้

นี่คือ Script SQL ที่สามารถใช้งานได้ใน TiDB:

```sql
WITH RowCounts AS (
    SELECT 
        'Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Survey_VSMS_TBV_TB_VSMS_SalesPersonTracking
    
    UNION ALL
    
    SELECT 
        'Survey_VSMS_TBV_TB_VSMS_RegionGroup' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Survey_VSMS_TBV_TB_VSMS_RegionGroup
    
    UNION ALL
    
    SELECT 
        'Survey_VSMS_TBV_TB_VSMS_SalesTeam' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Survey_VSMS_TBV_TB_VSMS_SalesTeam
    
    UNION ALL
    
    SELECT 
        'Survey_VSMS_TBV_TB_VSMS_BranchGroup' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Survey_VSMS_TBV_TB_VSMS_BranchGroup
    
    UNION ALL
    
    SELECT 
        'Survey_VSMS_TBV_TB_SYS_User' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Survey_VSMS_TBV_TB_SYS_User
    
    UNION ALL
    
    SELECT 
        'Sales_VSMS_TBV_TB_VSMS_Route' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Sales_VSMS_TBV_TB_VSMS_Route
    
    UNION ALL
    
    SELECT 
        'Sales_VSMS_TBV_TB_VSMS_RoutePlan' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Sales_VSMS_TBV_TB_VSMS_RoutePlan
    
    UNION ALL
    
    SELECT 
        'Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Sales_VSMS_TBV_TB_VSMS_RoutePlanDetail
    
    UNION ALL
    
    SELECT 
        'Survey_VSMS_TBV_TB_VSMS_SOCustomer' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Survey_VSMS_TBV_TB_VSMS_SOCustomer
    
    UNION ALL
    
    SELECT 
        'Survey_VSMS_TBV_TB_VSMS_Customer' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Survey_VSMS_TBV_TB_VSMS_Customer
    
    UNION ALL
    
    SELECT 
        'Survey_VSMS_TBV_TB_VSMS_BranchedCustomer' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Survey_VSMS_TBV_TB_VSMS_BranchedCustomer
    
    UNION ALL
    
    SELECT 
        'Survey_VSMS_TBV_TB_VSMS_ChannelCategory' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Survey_VSMS_TBV_TB_VSMS_ChannelCategory
    
    UNION ALL
    
    SELECT 
        'Sales_VSMS_TBV_TB_VSMS_CustomerVisit' AS TableName,
        COUNT(*) AS RowCount
    FROM 
        Sales_VSMS_TBV_TB_VSMS_CustomerVisit
)

SELECT * FROM RowCounts;
```

### คำอธิบาย:
1. **WITH RowCounts**: สร้าง CTE ที่เก็บจำนวนแถวของทุกตาราง
2. **UNION ALL**: ใช้ในการรวมผลลัพธ์สำหรับแต่ละตาราง
3. **SELECT * FROM RowCounts**: ดึงข้อมูลทั้งหมดจาก CTE ที่เราสร้างขึ้น

โดยการทำงานร่วมกับ TiDB การใช้ CTE จึงจะทำให้เราสามารถจัดการกับการรวมผลลัพธ์ได้อย่างมีประสิทธิภาพ หากคุณมีคำถามเพิ่มเติมหรือความต้องการในการช่วยเหลือในเรื่องอื่น ๆ สามารถแจ้งได้เลยครับ![0m
==================================================
