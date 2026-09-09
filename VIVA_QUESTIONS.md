# COMPREHENSIVE DBMS & DA2 PROJECT VIVA QUESTIONS (45+ QUESTIONS & ANSWERS)
## Pharmacy Inventory and Prescription Tracking System
### Simple, Conceptually Strong Answers Prepared for College Students

---

### PART 1: GENERAL DBMS CONCEPTS & ARCHITECTURE

#### Q1. What is a Database Management System (DBMS)?
**Answer:**
A DBMS is system software that enables users to define, create, maintain, and control access to structured data. It provides data independence, eliminates redundancy, enforces integrity constraints, supports concurrent multi-user transactions, and guarantees data durability.

#### Q2. What are the key advantages of a DBMS over a traditional file-processing system?
**Answer:**
1. **Data Redundancy Control:** Eliminates multiple inconsistent copies of the same data.
2. **Data Consistency & Integrity:** Enforces constraints (PK, FK, CHECK).
3. **Concurrent Access & Crash Recovery:** Uses ACID transaction protocols.
4. **Data Independence:** Changes in storage structures do not affect application code.
5. **Security:** Granular user permissions and access control.

#### Q3. Explain the three-schema architecture (ANSI/SPARC).
**Answer:**
1. **Internal (Physical) Level:** Describes how data is physically stored on disk (indexes, B-trees, file allocation).
2. **Conceptual (Logical) Level:** Describes what data is stored and relationships between entities (our 17 DA1 tables).
3. **External (View) Level:** User-specific views tailoring data visibility (e.g., our Pharmacist view vs. Admin view).

---

### PART 2: ER MODEL, RELATIONSHIPS & CARDINALITY

#### Q4. What is an Entity, Entity Set, and Attribute?
**Answer:**
- **Entity:** A distinct real-world object or concept (e.g., a specific Patient "Rahul Sharma").
- **Entity Set:** A collection of similar entities (e.g., the `PATIENT` table).
- **Attribute:** A characteristic or property of an entity (e.g., `DOB`, `Sex`, `Price`).

#### Q5. What is Cardinality Ratio in ER modeling?
**Answer:**
Cardinality expresses the number of entity instances of one entity set that can be associated with instances of another:
- **1:1 (One-to-One):** Rarely used; e.g., one branch manager per pharmacy.
- **1:N (One-to-Many):** One Hospital employs many Doctors; one Pharmacy has many Pharmacists.
- **M:N (Many-to-Many):** A Prescription has many Medicines, and a Medicine is in many Prescriptions (resolved via `PRESCRIPTION_ITEM`).

#### Q6. What is the difference between Participation Constraints (Total vs. Partial)?
**Answer:**
- **Total Participation (Existence Dependency):** Every instance must participate in the relationship (indicated by a double line). For example, every `PRESCRIPTION_ITEM` must belong to an existing `PRESCRIPTION`.
- **Partial Participation:** Some instances may not participate. For example, a `MEDICINE` can exist in the formulary catalog without currently being prescribed in any prescription.

#### Q7. What is an Associative Entity (or Junction Table)?
**Answer:**
Relational databases cannot directly implement M:N relationships in a single relation without violating 1NF. An associative entity decomposes an M:N relationship into two 1:N relationships.
- *Examples in our project:* `PRESCRIPTION_ITEM` (Prescription ↔ Medicine), `SUPPLIER_MANUFACTURER` (Supplier ↔ Manufacturer), and `SUPPLIER_PHARMACY`.

#### Q8. What is a Weak Entity?
**Answer:**
An entity that cannot be uniquely identified by its own attributes alone and depends on the existence of an identifying owner entity. It has a partial discriminator key and total participation (e.g., `PATIENT_CONTACT` depends on `PATIENT`).

---

### PART 3: RELATIONAL KEYS & CONSTRAINTS

#### Q9. Distinguish between Super Key, Candidate Key, and Primary Key.
**Answer:**
- **Super Key:** Any set of attributes that uniquely identifies a row in a table.
- **Candidate Key:** A minimal super key (no extraneous attributes can be removed without losing uniqueness).
- **Primary Key (PK):** The candidate key chosen by the database architect to uniquely identify records; it cannot accept `NULL` values.

#### Q10. What is a Composite Key? Give examples from this project.
**Answer:**
A primary key consisting of two or more attributes combined to guarantee uniqueness.
- *Examples in our project:*
  - `PATIENT_CONTACT(Patient_ID, Contact_No)`
  - `SUPPLIER_MANUFACTURER(Supplier_ID, Manufacturer_ID)`
  - `SUPPLIER_WHOLESALE(Supplier_ID, GST_No)`
  - `SUPPLIER_PHARMACY(Supplier_ID, Pharmacy_ID)`

#### Q11. What is a Foreign Key and Referential Integrity?
**Answer:**
A Foreign Key (FK) is an attribute (or collection of attributes) in one table that references the Primary Key of another table. **Referential Integrity** guarantees that the FK value must either match an existing PK in the referenced table or be `NULL`. It prevents orphan child rows.

#### Q12. What is the difference between `ON DELETE CASCADE` and `ON DELETE RESTRICT`?
**Answer:**
- `ON DELETE CASCADE`: When the parent row is deleted, all referencing child rows are automatically deleted (used for dependent items: deleting a Prescription deletes its `PRESCRIPTION_ITEM` rows).
- `ON DELETE RESTRICT`: Prevents deletion of the parent row if any child row references it (prevents accidental deletion of a Patient who has existing financial `BILL` records).

---

### PART 4: NORMALIZATION (1NF to BCNF)

#### Q13. What is Normalization and why is it important?
**Answer:**
Normalization is a systematic technique for decomposing tables to minimize data redundancy and eliminate anomalies (Insertion, Update, and Deletion anomalies) while preserving dependencies and lossless join decomposition.

#### Q14. What are Insertion, Update, and Deletion anomalies?
**Answer:**
- **Insertion Anomaly:** Inability to record certain facts without adding unrelated data (e.g., cannot add a new Medicine unless someone prescribes it).
- **Update Anomaly:** Inconsistent data when updating redundant values in multiple rows (e.g., changing a doctor's qualification in 50 prescription rows).
- **Deletion Anomaly:** Loss of unintended data when deleting a record (e.g., deleting a patient's bill also deletes hospital details).

#### Q15. Explain First Normal Form (1NF). How is it achieved in your DA1/DA2 design?
**Answer:**
A relation is in 1NF if all domain attribute values are **atomic** (indivisible) and there are no repeating groups or multi-valued attributes.
- *In our project:* Multi-valued contact numbers (`PATIENT.Contact_No`) were decomposed into the separate table `PATIENT_CONTACT(Patient_ID, Contact_No)`, and composite addresses were split into atomic columns (`Street`, `City`, `State`).

#### Q16. Explain Second Normal Form (2NF).
**Answer:**
A relation is in 2NF if it is in 1NF and **every non-prime attribute is fully functionally dependent on the primary key** (no partial functional dependency).
- In our junction tables like `SUPPLIER_MANUFACTURER(Supplier_ID, Manufacturer_ID)`, all columns form the composite primary key; hence no partial dependency exists.

#### Q17. Explain Third Normal Form (3NF).
**Answer:**
A relation is in 3NF if it is in 2NF and **no non-prime attribute is transitively dependent on the candidate key** (if $X \to Y$ and $Y \to Z$, then $X \to Z$ is transitive).
- In `DOCTOR`, `Hospital_ID` is a foreign key. All doctor attributes (`First_Name`, `Qualification`, `Experience`) depend directly on `Doctor_ID`, not transitively on `Hospital_ID`.

#### Q18. Explain Boyce-Codd Normal Form (BCNF).
**Answer:**
A relation is in BCNF if for every non-trivial functional dependency $X \to Y$, the determinant $X$ **must be a superkey**. BCNF is a stricter version of 3NF that handles multiple overlapping candidate keys. All tables in our schema strictly satisfy BCNF.

---

### PART 5: SQL QUERIES, JOINS & AGGREGATIONS

#### Q19. What is the difference between `WHERE` and `HAVING`?
**Answer:**
- `WHERE` filters individual rows **before** any grouping or aggregation takes place.
- `HAVING` filters aggregated groups **after** the `GROUP BY` clause has been computed (e.g., `HAVING SUM(B.Amount) > 300.00` or `HAVING COUNT(P.Prescription_ID) >= 2`).

#### Q20. What is the difference between `INNER JOIN` and `LEFT OUTER JOIN`?
**Answer:**
- `INNER JOIN`: Returns only the rows where there is a matching key in both tables (e.g., Doctors with assigned Hospitals).
- `LEFT OUTER JOIN`: Returns all rows from the left table, and the matched rows from the right table; if no match exists, `NULL` values are returned for right-table columns (e.g., listing all Medicines even if they have never been prescribed).

#### Q21. What is a Correlated Subquery?
**Answer:**
A subquery that references a column from the outer query table. It cannot be executed independently because it is evaluated once for each candidate row in the outer query.
- *Example in our project (Query 16):* Finding doctors with experience higher than the average experience of doctors in their *own* specific hospital (`WHERE D1.Experience > (SELECT AVG(D2.Experience) FROM DOCTOR D2 WHERE D2.Hospital_ID = D1.Hospital_ID)`).

#### Q22. Explain `EXISTS` vs. `IN`. When is `EXISTS` preferred?
**Answer:**
- `IN` compares an attribute value against a list or a single-column subquery result set.
- `EXISTS` checks for the presence of at least one row matching the condition and returns a boolean (`TRUE`/`FALSE`).
- `EXISTS` is faster on large datasets because the query optimizer terminates evaluation upon encountering the first matching record (short-circuit evaluation).

---

### PART 6: TRANSACTIONS & ACID PROPERTIES

#### Q23. What are the ACID properties of a relational transaction?
**Answer:**
1. **Atomicity:** All operations in a transaction succeed completely or roll back completely ("all or nothing").
2. **Consistency:** The database transitions from one valid state to another, preserving all schema integrity constraints.
3. **Isolation:** Concurrent transactions execute without interfering with one another.
4. **Durability:** Once committed, data modifications persist permanently on disk even during system crashes.

#### Q24. Where is transaction control used in your project?
**Answer:**
Inside stored procedures like `generate_bill()` and `add_patient()`:
```sql
START TRANSACTION;
  INSERT INTO BILL (...) VALUES (...);
  UPDATE INVENTORY SET Quantity = Quantity - 1 ...;
  INSERT INTO STOCK_LOG (...) VALUES (...);
COMMIT;
```
If any statement fails, the entire transaction is rolled back, preventing orphaned bills or decremented stock without an invoice.

---

### PART 7: PL/SQL / STORED PROGRAMS (PROCEDURES, FUNCTIONS, TRIGGERS)

#### Q25. What is the difference between a Stored Procedure and a Stored Function?
**Answer:**
| Feature | Stored Procedure | Stored Function |
|---|---|---|
| **Return Value** | Does not return a value directly (uses OUT parameters). | Must return exactly one scalar value using `RETURNS`. |
| **Invocation** | Called using `CALL proc_name(...)`. | Called directly within SQL statements (e.g., `SELECT func_name(...)`). |
| **Side Effects** | Can perform DML operations (INSERT, UPDATE, DELETE). | Typically deterministic and read-only (`READS SQL DATA`). |
| **Transaction** | Can manage transactions (`START TRANSACTION`, `COMMIT`). | Cannot initiate or commit transactions. |

#### Q26. Why are MySQL Stored Programs considered equivalent to PL/SQL for this DA2 submission?
**Answer:**
PL/SQL is Oracle's proprietary procedural extension. MySQL implements the ANSI SQL/PSM (Persistent Stored Modules) standard, which provides identical database programming constructs: stored procedures, deterministic functions, cursor loops, conditional branching (`IF...THEN...ELSE`), automated triggers, and exception handling using `SIGNAL SQLSTATE`.

#### Q27. What is a Database Trigger? What are its components?
**Answer:**
A trigger is a procedural block stored in the database that executes automatically in response to a specified DML event (`INSERT`, `UPDATE`, `DELETE`) on a particular table.
- **Components:**
  1. **Timing:** `BEFORE` or `AFTER`.
  2. **Event:** `INSERT`, `UPDATE`, or `DELETE`.
  3. **Target Table:** e.g., `INVENTORY`, `BILL`.
  4. **Granularity:** `FOR EACH ROW` (row-level trigger).
  5. **Trigger Body:** Business rules checking `OLD` and `NEW` pseudo-records.

#### Q28. Explain the triggers you implemented in your project.
**Answer:**
1. `trg_before_inventory_update`: Enforces `NEW.Quantity >= 0`. If an update attempts to reduce inventory below zero, it throws `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Inventory quantity cannot be negative.'`.
2. `trg_after_inventory_update`: Calculates the delta (`NEW.Quantity - OLD.Quantity`) and automatically writes an immutable audit record into `STOCK_LOG` with movement type `RESTOCK` or `DISPENSE`.
3. `trg_validate_bill_amount`: Ensures invoiced bill amounts are strictly non-negative.
4. `trg_before_order_insert`: Enforces that `Arrival_Date >= Order_Date`.

#### Q29. What is `SIGNAL SQLSTATE '45000'`?
**Answer:**
In standard ANSI SQL and MySQL 8.x, `SQLSTATE '45000'` is the designated generic state representing an unhandled user-defined exception. Using `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...'` allows us to raise custom business exceptions that abort the executing statement and pass a clear error message to the client application.

#### Q30. What is a Database Cursor and when is it used?
**Answer:**
A cursor is a database pointer that enables row-by-row processing of a query result set. It is used in procedural logic when complex calculations or sequential row operations cannot be expressed in set-based SQL.

---

### PART 8: INVENTORY JUSTIFICATION & SYSTEM DESIGN

#### Q31. The DA1 diagram did not explicitly have an `INVENTORY` table. Why did you add it for DA2?
**Answer:**
In our DA1 conceptual model, `MEDICINE` describes the drug catalog metadata, and `ORDER` represents bulk purchases. However, because our project title is **"Pharmacy Inventory and Prescription Tracking System"**, tracking stock-on-hand at distinct physical pharmacy branches requires localized inventory state. 
We introduced `INVENTORY(Pharmacy_ID, Medicine_ID, Quantity, Reorder_Level)` and `STOCK_LOG` as documented **Implementation-Support Tables** that support real-world functionality without altering the original DA1 entities or relationships.

#### Q32. Why is `ORDER` enclosed in backticks (`` `ORDER` ``) in your SQL files?
**Answer:**
In ANSI SQL and MySQL, `ORDER` is a reserved keyword used in the `ORDER BY` clause. To preserve the exact table name from our approved DA1 schema without renaming it, we enclose it in backticks (`` `ORDER` ``), which tells MySQL to parse it as an identifier rather than a language keyword.

---

### PART 9: WEB APPLICATION, FLASK & SECURITY

#### Q33. Why did you use Flask instead of Django or React?
**Answer:**
Flask is a lightweight, micro-framework that keeps database code close to the surface. It allows us to execute pure, raw parameterized SQL queries and invoke native MySQL stored procedures without the abstraction layer of a heavyweight ORM (like Django ORM or Hibernate), making the relational concepts completely transparent and easy to explain during viva.

#### Q34. What is SQL Injection and how did you prevent it?
**Answer:**
SQL Injection occurs when malicious user input containing SQL fragments is concatenated directly into a query string, altering the execution logic.
- *Prevention:* We use **parameterized queries** (prepared statements) with placeholders (`?` or `%s`). User inputs are treated strictly as data literals, never as executable SQL.

#### Q35. Explain how the frontend talks to the database.
**Answer:**
1. User submits a form or triggers an action in the browser (e.g., click "Create Prescription").
2. Client-side JavaScript makes an asynchronous `fetch()` API request sending JSON payload to Flask.
3. Flask route validates inputs and calls the appropriate service method.
4. The service executes a parameterized query or invokes a stored procedure via `cursor.callproc()`.
5. MySQL executes the procedure, triggers fire, and results are returned to Flask.
6. Flask formats a JSON response (`{ success: true, message: ... }`), and the frontend displays a toast notification or updates charts.

---

### PART 10: RAPID-FIRE VIVA QUESTIONS

#### Q36. What is a View?
**Answer:** A virtual table based on the result-set of an SQL query. It does not store physical data (unless materialized), but simplifies complex queries and enhances data security.

#### Q37. What is an Index? How does it improve performance?
**Answer:** A data structure (typically a B-Tree) created on table columns that enables $O(\log N)$ search speed instead of an $O(N)$ full table scan.

#### Q38. What is the difference between `CHAR` and `VARCHAR`?
**Answer:** `CHAR(n)` is fixed-length (pads with spaces up to $n$ bytes), whereas `VARCHAR(n)` is variable-length (uses only the storage needed plus 1–2 prefix length bytes).

#### Q39. What is a Surrogate Key?
**Answer:** An artificial, system-generated identifier with no intrinsic business meaning (e.g., `Item_ID AUTO_INCREMENT` in `PRESCRIPTION_ITEM`), used for primary indexing efficiency.

#### Q40. What is lossless join decomposition?
**Answer:** A property of relational decomposition ensuring that decomposing relation $R$ into $R_1$ and $R_2$ allows $R$ to be reconstructed exactly ($R_1 \bowtie R_2 = R$) without introducing spurious rows.

---
*Be confident, speak clearly, and point to the live running application and SQL files to back up your answers!*
