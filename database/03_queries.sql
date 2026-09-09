-- ============================================================================
-- PHARMACY INVENTORY AND PRESCRIPTION TRACKING SYSTEM
-- DA2 College Database Project - 25+ Comprehensive Academic SQL Queries
-- Demonstrating Core Relational Concepts, Subqueries, Joins & Aggregations
-- ============================================================================

USE pharmacy_system_new;

-- ----------------------------------------------------------------------------
-- QUERY 1: SELECT, WHERE, and ORDER BY
-- Concept: Basic projection, predicate filtering, and descending sort
-- Purpose: List all active medicines priced above INR 100 sorted from highest to lowest
-- ----------------------------------------------------------------------------
SELECT 
    `Medicine_ID`,
    `Name` AS `Medicine_Name`,
    `Price` AS `Unit_Price_INR`,
    `Exp_Date`
FROM `MEDICINE`
WHERE `Price` >= 100.00
ORDER BY `Price` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 2: DISTINCT
-- Concept: Elimination of duplicate tuples from projection
-- Purpose: Identify all unique cities where patients in our healthcare network reside
-- ----------------------------------------------------------------------------
SELECT DISTINCT 
    `City`,
    `State`
FROM `PATIENT`
ORDER BY `State`, `City`;

-- ----------------------------------------------------------------------------
-- QUERY 3: LIKE (Pattern Matching)
-- Concept: Wildcard matching using '%' and '_'
-- Purpose: Find all doctors with a cardiology, neurology, or doctoral qualification
-- ----------------------------------------------------------------------------
SELECT 
    `Doctor_ID`,
    CONCAT(`First_Name`, ' ', `Last_Name`) AS `Doctor_Name`,
    `Qualification`,
    `Experience` AS `Years_Experience`,
    `Contact_No`
FROM `DOCTOR`
WHERE `Qualification` LIKE '%DM%' OR `Qualification` LIKE '%Cardiology%'
ORDER BY `Experience` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 4: BETWEEN (Range Comparison)
-- Concept: Inclusive closed interval filtering on temporal/numeric attributes
-- Purpose: Retrieve clinical prescriptions created between mid-August and early September 2026
-- ----------------------------------------------------------------------------
SELECT 
    `Prescription_ID`,
    `Doctor_ID`,
    `Patient_ID`,
    `Date` AS `Prescription_Date`
FROM `PRESCRIPTION`
WHERE `Date` BETWEEN '2026-08-15' AND '2026-09-02'
ORDER BY `Date` ASC;

-- ----------------------------------------------------------------------------
-- QUERY 5: IN (Membership Set Operation)
-- Concept: Set inclusion verification against an enumerated collection of literals
-- Purpose: Identify purchase orders awaiting active fulfillment (Pending or Processing)
-- ----------------------------------------------------------------------------
SELECT 
    `Order_ID`,
    `Supplier_ID`,
    `Pharmacy_ID`,
    `Quantity_Ordered`,
    `Date` AS `Order_Date`,
    `Order_Status`,
    `Payment_Status`
FROM `ORDER`
WHERE `Order_Status` IN ('Pending', 'Processing')
ORDER BY `Date` ASC;

-- ----------------------------------------------------------------------------
-- QUERY 6: COUNT and GROUP BY
-- Concept: Relational aggregation over partitioned equivalence classes
-- Purpose: Compute total number of clinical prescriptions issued by each doctor
-- ----------------------------------------------------------------------------
SELECT 
    D.`Doctor_ID`,
    CONCAT(D.`First_Name`, ' ', D.`Last_Name`) AS `Doctor_Name`,
    D.`Qualification`,
    COUNT(P.`Prescription_ID`) AS `Total_Prescriptions_Issued`
FROM `DOCTOR` D
LEFT JOIN `PRESCRIPTION` P ON D.`Doctor_ID` = P.`Doctor_ID`
GROUP BY D.`Doctor_ID`, D.`First_Name`, D.`Last_Name`, D.`Qualification`
ORDER BY `Total_Prescriptions_Issued` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 7: SUM and GROUP BY
-- Concept: Total accumulation across grouped relational entities
-- Purpose: Calculate total gross billed revenue generated per dispensing pharmacy branch
-- ----------------------------------------------------------------------------
SELECT 
    PH.`Pharmacy_ID`,
    PH.`Name` AS `Pharmacy_Name`,
    PH.`City`,
    COUNT(B.`Bill_ID`) AS `Total_Bills_Generated`,
    COALESCE(SUM(B.`Amount`), 0.00) AS `Total_Revenue_INR`
FROM `PHARMACY` PH
LEFT JOIN `BILL` B ON PH.`Pharmacy_ID` = B.`Pharmacy_ID`
GROUP BY PH.`Pharmacy_ID`, PH.`Name`, PH.`City`
ORDER BY `Total_Revenue_INR` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 8: AVG (Arithmetic Mean)
-- Concept: Aggregation calculating the statistical mean of a continuous attribute
-- Purpose: Determine the network-wide average retail price of pharmaceutical formulations
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(`Medicine_ID`) AS `Total_Formulations_Cataloged`,
    ROUND(AVG(`Price`), 2) AS `Average_Medicine_Price_INR`
FROM `MEDICINE`;

-- ----------------------------------------------------------------------------
-- QUERY 9: MIN and MAX (Extremum Identification)
-- Concept: Extremal boundary extraction from numerical attributes
-- Purpose: Identify the minimum and maximum priced medicines within the formulary
-- ----------------------------------------------------------------------------
SELECT 
    MIN(`Price`) AS `Lowest_Medicine_Price_INR`,
    MAX(`Price`) AS `Highest_Medicine_Price_INR`,
    ROUND(MAX(`Price`) - MIN(`Price`), 2) AS `Price_Range_Spread_INR`
FROM `MEDICINE`;

-- ----------------------------------------------------------------------------
-- QUERY 10: GROUP BY and Multi-Column Aggregation
-- Concept: Multi-attribute aggregation on procurement records
-- Purpose: Quantify procurement orders and volume fulfilled by each supplier
-- ----------------------------------------------------------------------------
SELECT 
    S.`Supplier_ID`,
    S.`Name` AS `Supplier_Name`,
    COUNT(O.`Order_ID`) AS `Total_Orders_Placed`,
    COALESCE(SUM(O.`Quantity_Ordered`), 0) AS `Total_Units_Supplied`
FROM `SUPPLIER` S
LEFT JOIN `ORDER` O ON S.`Supplier_ID` = O.`Supplier_ID`
GROUP BY S.`Supplier_ID`, S.`Name`
ORDER BY `Total_Units_Supplied` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 11: HAVING Clause
-- Concept: Post-aggregation group qualification filter
-- Purpose: Filter and retrieve patients whose cumulative medical billing exceeds INR 300
-- ----------------------------------------------------------------------------
SELECT 
    PT.`Patient_ID`,
    CONCAT(PT.`First_Name`, ' ', PT.`Last_Name`) AS `Patient_Name`,
    COUNT(B.`Bill_ID`) AS `Invoices_Count`,
    SUM(B.`Amount`) AS `Cumulative_Spending_INR`
FROM `PATIENT` PT
INNER JOIN `BILL` B ON PT.`Patient_ID` = B.`Patient_ID`
GROUP BY PT.`Patient_ID`, PT.`First_Name`, PT.`Last_Name`
HAVING SUM(B.`Amount`) > 300.00
ORDER BY `Cumulative_Spending_INR` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 12: INNER JOIN (Binary Equijoin)
-- Concept: Preserves matching tuples between Doctor and Hospital relations
-- Purpose: Display medical specialists along with their affiliated hospital hospital details
-- ----------------------------------------------------------------------------
SELECT 
    D.`Doctor_ID`,
    CONCAT(D.`First_Name`, ' ', D.`Last_Name`) AS `Doctor_Name`,
    D.`Qualification`,
    H.`Name` AS `Hospital_Name`,
    H.`City` AS `Hospital_City`,
    H.`Contact` AS `Hospital_Emergency_Contact`
FROM `DOCTOR` D
INNER JOIN `HOSPITAL` H ON D.`Hospital_ID` = H.`Hospital_ID`
ORDER BY H.`Name`, D.`First_Name`;

-- ----------------------------------------------------------------------------
-- QUERY 13: LEFT OUTER JOIN
-- Concept: Preserves all tuples from the left relation regardless of join match
-- Purpose: Audit medicines and their prescribed counts, retaining never-prescribed items
-- ----------------------------------------------------------------------------
SELECT 
    M.`Medicine_ID`,
    M.`Name` AS `Medicine_Name`,
    M.`Price` AS `Unit_Price_INR`,
    COUNT(PI.`Item_ID`) AS `Times_Prescribed`
FROM `MEDICINE` M
LEFT JOIN `PRESCRIPTION_ITEM` PI ON M.`Medicine_ID` = PI.`Medicine_ID`
GROUP BY M.`Medicine_ID`, M.`Name`, M.`Price`
ORDER BY `Times_Prescribed` DESC, M.`Name` ASC;

-- ----------------------------------------------------------------------------
-- QUERY 14: Multi-Table JOIN (5 Relations: Patient -> Presc -> Item -> Med -> Doctor)
-- Concept: Composed equi-joins across the full clinical prescribing chain
-- Purpose: Produce a comprehensive clinical audit report of all prescribed medications
-- ----------------------------------------------------------------------------
SELECT 
    P.`Prescription_ID`,
    P.`Date` AS `Prescription_Date`,
    CONCAT(PT.`First_Name`, ' ', PT.`Last_Name`) AS `Patient_Name`,
    CONCAT(D.`First_Name`, ' ', D.`Last_Name`) AS `Prescribing_Doctor`,
    M.`Name` AS `Medicine_Prescribed`,
    PI.`Dosage`,
    PI.`Frequency`,
    PI.`Duration`
FROM `PRESCRIPTION` P
INNER JOIN `PATIENT` PT ON P.`Patient_ID` = PT.`Patient_ID`
INNER JOIN `DOCTOR` D ON P.`Doctor_ID` = D.`Doctor_ID`
INNER JOIN `PRESCRIPTION_ITEM` PI ON P.`Prescription_ID` = PI.`Prescription_ID`
INNER JOIN `MEDICINE` M ON PI.`Medicine_ID` = M.`Medicine_ID`
ORDER BY P.`Date` DESC, P.`Prescription_ID` ASC;

-- ----------------------------------------------------------------------------
-- QUERY 15: Subquery in WHERE (Scalar Subquery)
-- Concept: Dynamic operand comparison against inner query scalar output
-- Purpose: Identify premium pharmaceuticals priced higher than the portfolio average
-- ----------------------------------------------------------------------------
SELECT 
    `Medicine_ID`,
    `Name` AS `Medicine_Name`,
    `Price` AS `Price_INR`,
    `Exp_Date`
FROM `MEDICINE`
WHERE `Price` > (
    SELECT AVG(`Price`) 
    FROM `MEDICINE`
)
ORDER BY `Price` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 16: Correlated Subquery
-- Concept: Inner subquery execution parameterized per outer tuple evaluation
-- Purpose: Identify doctors possessing more experience than the average in their hospital
-- ----------------------------------------------------------------------------
SELECT 
    D1.`Doctor_ID`,
    CONCAT(D1.`First_Name`, ' ', D1.`Last_Name`) AS `Doctor_Name`,
    D1.`Hospital_ID`,
    D1.`Experience` AS `Doctor_Experience_Years`
FROM `DOCTOR` D1
WHERE D1.`Experience` > (
    SELECT AVG(D2.`Experience`)
    FROM `DOCTOR` D2
    WHERE D2.`Hospital_ID` = D1.`Hospital_ID`
)
ORDER BY D1.`Hospital_ID`, D1.`Experience` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 17: EXISTS (Semi-Join Predicate)
-- Concept: Set existence evaluation returning boolean TRUE upon first match
-- Purpose: Find suppliers who have successfully fulfilled at least one 'Delivered' order
-- ----------------------------------------------------------------------------
SELECT 
    S.`Supplier_ID`,
    S.`Name` AS `Supplier_Name`,
    S.`City`,
    S.`Contact`
FROM `SUPPLIER` S
WHERE EXISTS (
    SELECT 1 
    FROM `ORDER` O
    WHERE O.`Supplier_ID` = S.`Supplier_ID` 
      AND O.`Order_Status` = 'Delivered'
);

-- ----------------------------------------------------------------------------
-- QUERY 18: NOT EXISTS (Anti-Join Predicate)
-- Concept: Set absence evaluation returning boolean TRUE if inner query returns empty set
-- Purpose: Detect unprescribed medicines in the catalog (dormant formulary items)
-- ----------------------------------------------------------------------------
SELECT 
    M.`Medicine_ID`,
    M.`Name` AS `Unprescribed_Medicine`,
    M.`Price` AS `Price_INR`
FROM `MEDICINE` M
WHERE NOT EXISTS (
    SELECT 1 
    FROM `PRESCRIPTION_ITEM` PI
    WHERE PI.`Medicine_ID` = M.`Medicine_ID`
);

-- ----------------------------------------------------------------------------
-- QUERY 19: CASE Expression (Conditional Derivation)
-- Concept: Categorical attribute transformation based on boundary conditions
-- Purpose: Classify branch inventory stock health into operational actionable tiers
-- ----------------------------------------------------------------------------
SELECT 
    PH.`Name` AS `Pharmacy_Branch`,
    M.`Name` AS `Medicine_Name`,
    INV.`Quantity` AS `Stock_On_Hand`,
    INV.`Reorder_Level`,
    CASE 
        WHEN INV.`Quantity` = 0 THEN 'OUT OF STOCK - URGENT'
        WHEN INV.`Quantity` <= INV.`Reorder_Level` THEN 'LOW STOCK - REORDER'
        ELSE 'OPTIMAL STOCK'
    END AS `Inventory_Status`
FROM `INVENTORY` INV
INNER JOIN `PHARMACY` PH ON INV.`Pharmacy_ID` = PH.`Pharmacy_ID`
INNER JOIN `MEDICINE` M ON INV.`Medicine_ID` = M.`Medicine_ID`
ORDER BY INV.`Quantity` ASC;

-- ----------------------------------------------------------------------------
-- QUERY 20: Date-based Query (Impending Expiry in Next 90 Days)
-- Concept: Temporal interval arithmetic using CURDATE() and DATEDIFF()
-- Purpose: Flag medicines expiring within the next 90 days for safety clearance
-- ----------------------------------------------------------------------------
SELECT 
    `Medicine_ID`,
    `Name` AS `Medicine_Name`,
    `Exp_Date`,
    DATEDIFF(`Exp_Date`, CURDATE()) AS `Days_Until_Expiry`
FROM `MEDICINE`
WHERE `Exp_Date` >= CURDATE() 
  AND `Exp_Date` <= DATE_ADD(CURDATE(), INTERVAL 90 DAY)
ORDER BY `Exp_Date` ASC;

-- ----------------------------------------------------------------------------
-- QUERY 21: Expired Medicines Quarantine Query
-- Concept: Identifying strictly expired pharmaceuticals where Exp_Date < CURDATE()
-- Purpose: Isolate expired batches across pharmacies requiring disposal
-- ----------------------------------------------------------------------------
SELECT 
    M.`Medicine_ID`,
    M.`Name` AS `Medicine_Name`,
    M.`Exp_Date`,
    COALESCE(SUM(INV.`Quantity`), 0) AS `Total_Expired_Units_Held`
FROM `MEDICINE` M
LEFT JOIN `INVENTORY` INV ON M.`Medicine_ID` = INV.`Medicine_ID`
WHERE M.`Exp_Date` < '2026-09-04' -- Local demonstration cutoff date
GROUP BY M.`Medicine_ID`, M.`Name`, M.`Exp_Date`;

-- ----------------------------------------------------------------------------
-- QUERY 22: Patients with Multiple Prescriptions
-- Concept: High-frequency healthcare consumer profiling using COUNT and HAVING
-- Purpose: Identify chronic or regular patients with 2 or more clinical prescriptions
-- ----------------------------------------------------------------------------
SELECT 
    PT.`Patient_ID`,
    CONCAT(PT.`First_Name`, ' ', PT.`Last_Name`) AS `Patient_Name`,
    PT.`City`,
    COUNT(P.`Prescription_ID`) AS `Prescription_Count`
FROM `PATIENT` PT
INNER JOIN `PRESCRIPTION` P ON PT.`Patient_ID` = P.`Patient_ID`
GROUP BY PT.`Patient_ID`, PT.`First_Name`, PT.`Last_Name`, PT.`City`
HAVING COUNT(P.`Prescription_ID`) >= 2
ORDER BY `Prescription_Count` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 23: Top 5 Most Prescribed Medicines
-- Concept: Ranked frequency distribution with LIMIT restriction
-- Purpose: Determine top volume therapeutics driving clinical demand
-- ----------------------------------------------------------------------------
SELECT 
    M.`Medicine_ID`,
    M.`Name` AS `Medicine_Name`,
    M.`Price` AS `Unit_Price_INR`,
    COUNT(PI.`Item_ID`) AS `Prescription_Frequency`
FROM `MEDICINE` M
INNER JOIN `PRESCRIPTION_ITEM` PI ON M.`Medicine_ID` = PI.`Medicine_ID`
GROUP BY M.`Medicine_ID`, M.`Name`, M.`Price`
ORDER BY `Prescription_Frequency` DESC, M.`Price` DESC
LIMIT 5;

-- ----------------------------------------------------------------------------
-- QUERY 24: Supplier Order Fulfillment & Payment Status Audit
-- Concept: Matrix aggregation using Conditional SUMs inside GROUP BY
-- Purpose: Financial and operational dashboard of procurement by supplier
-- ----------------------------------------------------------------------------
SELECT 
    S.`Supplier_ID`,
    S.`Name` AS `Supplier_Name`,
    COUNT(O.`Order_ID`) AS `Total_Orders`,
    SUM(CASE WHEN O.`Order_Status` = 'Delivered' THEN 1 ELSE 0 END) AS `Delivered_Orders`,
    SUM(CASE WHEN O.`Order_Status` IN ('Pending', 'Processing', 'Shipped') THEN 1 ELSE 0 END) AS `Active_Pipeline_Orders`,
    SUM(CASE WHEN O.`Payment_Status` = 'Paid' THEN 1 ELSE 0 END) AS `Settled_Paid_Orders`,
    SUM(CASE WHEN O.`Payment_Status` = 'Pending' THEN 1 ELSE 0 END) AS `Unpaid_Orders`
FROM `SUPPLIER` S
LEFT JOIN `ORDER` O ON S.`Supplier_ID` = O.`Supplier_ID`
GROUP BY S.`Supplier_ID`, S.`Name`
ORDER BY `Total_Orders` DESC;

-- ----------------------------------------------------------------------------
-- QUERY 25: Complex Multi-Junction Healthcare Network Report
-- Concept: Navigating 5 associative & master tables (Supplier -> Manufacturer -> Wholesale -> Pharmacy)
-- Purpose: Comprehensive supply-chain partner topology audit report
-- ----------------------------------------------------------------------------
SELECT 
    S.`Name` AS `Distributor_Supplier`,
    MFG.`Brand_Name` AS `Represented_Manufacturer`,
    WS.`GST_No` AS `Wholesale_Tax_Identity`,
    PH.`Name` AS `Supplied_Pharmacy_Branch`
FROM `SUPPLIER` S
INNER JOIN `SUPPLIER_MANUFACTURER` SM ON S.`Supplier_ID` = SM.`Supplier_ID`
INNER JOIN `MANUFACTURER` MFG ON SM.`Manufacturer_ID` = MFG.`Manufacturer_ID`
INNER JOIN `SUPPLIER_WHOLESALE` SW ON S.`Supplier_ID` = SW.`Supplier_ID`
INNER JOIN `WHOLESALE_SUPPLIER` WS ON SW.`GST_No` = WS.`GST_No`
INNER JOIN `SUPPLIER_PHARMACY` SP ON S.`Supplier_ID` = SP.`Supplier_ID`
INNER JOIN `PHARMACY` PH ON SP.`Pharmacy_ID` = PH.`Pharmacy_ID`
ORDER BY S.`Name`, MFG.`Brand_Name`, PH.`Name`;
