# Modifier: @Lukhanyo Vena
# Date: June 2024

"""
The database loan.db consists of 3 tables: 
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data
    
You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)

"""


def question_1():    
    
    #Make use of a JOIN to find out the `AverageIncome` per `CustomerClass`

    qry = """SELECT d.CustomerClass, ROUND(AVG(c.Income), 2) AS AverageIncome FROM customers AS c
             INNER JOIN credit AS d
             ON d.CustomerID = c.CustomerID
             GROUP BY d.CustomerClass;
             """
    
    return qry








def question_2():    
    
    #Q2: Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'. 

    qry = """ 
         WITH provinces AS (
            SELECT full_form, short_form FROM (
                VALUES 
                    ('EasternCape', 'EC'),
                    ('Gauteng', 'GT'),
                    ('FreeState', 'FS'),
                    ('NorthWest', 'NW'),
                    ('Natal', 'NL'),
                    ('WesternCape', 'WC'),
                    ('NorthernCape', 'NC'),
                    ('Limpopo', 'LP'),
                    ('Mpumalanga', 'MP')
            ) AS t(full_form, short_form)
        ),    
    Region1 AS (
        SELECT p.full_form AS Province, COUNT(l.ApprovalStatus) AS RejectedApplications       
        FROM provinces AS p
        INNER JOIN customers AS c ON p.short_form = c.Region
        INNER JOIN loans AS l ON l.CustomerID = c.CustomerID AND l.ApprovalStatus = 'Rejected'
        GROUP BY p.full_form
    ),
    Region2 AS ( 
        SELECT p.full_form AS Province, COUNT(l.ApprovalStatus) AS RejectedApplications       
        FROM provinces AS p
        INNER JOIN customers AS c ON p.full_form = c.Region
        INNER JOIN loans AS l ON l.CustomerID = c.CustomerID AND l.ApprovalStatus = 'Rejected'
        GROUP BY p.full_form
    )
    SELECT r1.Province AS Province, COALESCE(r1.RejectedApplications, 0) + COALESCE(r2.RejectedApplications, 0) AS RejectedApplications 
    FROM Region1 AS r1
    FULL JOIN Region2 AS r2 ON r1.Province = r2.Province; 
    """

    return qry






def question_3():    
    
    # Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
        # `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`
    # Do not return the new table

    qry = """CREATE TABLE IF NOT EXISTS financing (
                CustomerID INTEGER NOT NULL,
                Income DECIMAL(18, 2),
                LoanAmount DECIMAL(18, 2),
                LoanTerm INTEGER, 
                InterestRate DECIMAL(10, 4),
                ApprovalStatus TEXT,
                CreditScore INTEGER
            );
            
    
        INSERT INTO financing (CustomerID, Income, LoanAmount, LoanTerm, InterestRate, ApprovalStatus, CreditScore)
        SELECT DISTINCT c.CustomerID, c.Income, l.LoanAmount, l.LoanTerm, l.InterestRate, l.ApprovalStatus, d.CreditScore
        FROM customers AS c
        INNER JOIN loans as l ON l.CustomerID = c.CustomerID
        INNER JOIN credit as d ON d.CustomerID = c.CustomerID;
        """
    return qry





# Question 4 and 5 are linked

def question_4():

    # Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarizes Repayments per customer per month.
    # Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    # Repayments should only occur between 6am (UTC -> 5am) and 6pm  (UTC -> 5pm) London Time.
    # Hint: there should be 12x CustomerID = 1.
    # Null values to be filled with 0.

    qry = """
    CREATE TABLE IF NOT EXISTS timeline (
                CustomerID INTEGER NOT NULL,
                MonthName TEXT,
                NumberOfRepayments INTEGER,
                AmountTotal DECIMAL(18, 4),
                PRIMARY KEY(CustomerID, MonthName)
            );

    WITH customerMonths as (SELECT c.CustomerID, m.MonthName, m.MonthID FROM customers AS c CROSS JOIN months AS m),
    
   theTimeline AS (
    SELECT c.CustomerID, c.MonthName,
    COALESCE( COUNT(r.RepaymentDate) , 0) AS NumberOfRepayments,
    COALESCE( SUM(r.Amount), 0) AS AmountTotal
    FROM customerMonths AS c
    LEFT JOIN repayments AS r ON r.CustomerID=c.CustomerID 
    AND strftime('%m', r.RepaymentDate) = c.MonthID
    AND strftime('%H', (r.RepaymentDate AT TIME ZONE r.TimeZone AT TIME ZONE 'UTC')) >= 5
    AND strftime('%H', (r.RepaymentDate AT TIME ZONE r.TimeZone AT TIME ZONE 'UTC')) < 17
    GROUP BY c.CustomerID, c.MonthName)
    
    INSERT INTO timeline (CustomerID, MonthName, NumberOfRepayments, AmountTotal)
    SELECT CustomerID, MonthName, NumberOfRepayments, AmountTotal FROM theTimeline ;
    """
    return qry




def question_5():

    # Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
        # CustomerID, JanuaryRepayments, JanuaryTotal,...,DecemberRepayments, DecemberTotal,...etc
    # MonthRepayments columns (e.g JanuaryRepayments) should be integers
    # Hint: there should be 1x CustomerID = 1

    qry = """ 
        WITH part1 AS (
        SELECT CustomerID, CAST(January AS INT) AS JanuaryRepayments, CAST(February AS INT) AS FebruaryRepayments, 
        CAST(March AS INT) AS MarchRepayments, CAST(April AS INT )AS AprilRepayments, 
        CAST(May AS INT) AS MayRepayments, CAST(June AS INT) AS JuneRepayments, CAST(July AS INT) AS JulyRepayments, 
        CAST(August AS INT) AS AugustRepayments, CAST(September AS INT) AS SeptemberRepayments, 
        CAST(October AS INT) AS OctoberRepayments, CAST(November AS INT) AS NovemberRepayments, 
        CAST(December AS INT) AS DecemberRepayments
        FROM (
            SELECT CustomerID, MonthName, NumberOfRepayments
            FROM timeline
        ) AS mySourceTable
        PIVOT (
            SUM(NumberOfRepayments)
            FOR MonthName IN (January, February, March, April, May, June, July, August, September, October, November, December)
            
        ) AS PivotTable1
        ),

         part2 AS( 
         SELECT CustomerID, January AS JanuaryTotal, February AS FebruaryTotal, March AS MarchTotal, 
         April AS AprilTotal, May AS MayTotal, June AS JuneTotal, July AS JulyTotal, August AS AugustTotal, 
         September AS SeptemberTotal, October AS OctoberTotal, November AS NovemberTotal, December AS DecemberTotal
        FROM (
            SELECT CustomerID, MonthName, AmountTotal 
            FROM timeline
        ) AS mySourceTable
        PIVOT (
            SUM(AmountTotal)
            FOR MonthName IN (January, February, March, April, May, June, July, August, September, October, November, December)
            
        ) AS PivotTable2)
        

        SELECT p1.CustomerID, JanuaryRepayments, JanuaryTotal, FebruaryRepayments, FebruaryTotal, MarchRepayments, MarchTotal
        AprilRepayments, AprilTotal, MayRepayments, MayTotal, JuneRepayments, JuneTotal, JulyRepayments, JulyTotal, AugustRepayments,
        AugustTotal, SeptemberRepayments, SeptemberTotal, OctoberRepayments, OctoberTotal, NovemberRepayments, NovemberTotal,
        DecemberRepayments, DecemberTotal
        FROM part1 AS p1 
        INNER JOIN part2 AS p2 
        ON p1.CustomerID =  p2.CustomerID;
        
    """

    return qry





#QUESTION 6 and 7 are linked

def question_6():

    # The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    # Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    # relation to the corresponding CustomerID.

    # Utilize a window function to correct this mistake in a new `CorrectedAge` column.
    # Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender` 
    # Also return a result set for this table
    # Null values can be input manually

    qry = """
         CREATE TABLE IF NOT EXISTS corrected_customers (
                CustomerID INTEGER PRIMARY KEY NOT NULL,
                Age INTEGER,
                CorrectedAge INTEGER,
                Gender TEXT
        );
        
        WITH remove_duplicates AS(
        SELECT DISTINCT (CustomerID), Age, Gender
        FROM customers)

        INSERT INTO corrected_customers (CustomerID, Age, CorrectedAge , Gender)
        SELECT CustomerID, Age, LAG(Age, 2) OVER(PARTITION BY Gender ORDER BY CustomerID), Gender 
        FROM remove_duplicates;
        
        SELECT * FROM corrected_customers;
    
    """

    return qry


def question_7():

    # Create a column called 'AgeCategory' that categorizes customers by age 
    # Age categories should be as follows:
        # Teen: x < 20
        # Young Adult: 20 <= x < 30
        # Adult: 30 <= x < 60
        # Pensioner: x >= 60
    # Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    # The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6 
    # Customers with no repayments should be included as 0 in the result.

    qry = """
        WITH age_categorized AS (
            SELECT CustomerID, Age, CorrectedAge,
                CASE 
                WHEN CorrectedAge < 20 THEN 'Teen'
                WHEN CorrectedAge >= 20 AND CorrectedAge<30 THEN 'Young Adult'
                WHEN CorrectedAge >= 30 AND  CorrectedAge<60 THEN 'Adult'
                WHEN CorrectedAge >= 60 THEN 'Pensioner'
                ELSE 'No Category'
                END AS AgeCategory,
                Gender
            FROM corrected_customers
        ),

        group_payments AS ( 
        SELECT a.CustomerID, COUNT(r.RepaymentDate) OVER (PARTITION BY a.AgeCategory) AS TotalGroupPayments 
        FROM age_categorized AS a
        INNER JOIN repayments AS r ON r.CustomerID = a.CustomerID)


        SELECT a.CustomerID, a.CorrectedAge, a.AgeCategory,  g.TotalGroupPayments,
        DENSE_RANK() OVER(ORDER BY g.TotalGroupPayments DESC) AS Rank
        FROM age_categorized AS a
        INNER JOIN repayments AS r ON r.CustomerID = a.CustomerID
        INNER JOIN group_payments AS g ON g.CustomerID = a.CustomerID;
    """

    return qry
