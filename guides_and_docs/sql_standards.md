# SQL Standards
Writing clear, consistent SQL is something that gives our team the ability to move quickly and confidently. PR Reviews and debugging sessions are faster, and everyone is happier. The ultimate goal should be that we can never tell who wrote the code just by looking at it.

Please learn these rules and apply them when writing SQL. Note: this works better if you follow the rules from the beginning, instead of waiting until the end to do a pass through and "clean up the code".

* No subqueries - always use `with` clauses! The human brain struggles with maintaining context, especially when there are multiple levels of nesting. `with` clauses allow for logical breaks, and force you to specify the steps individually.

  Bad:

  ```sql
  SELECT * FROM (SELECT *, row_number() OVER (PARTITION BY truck_id) AS nth FROM taco_trucks WHERE city='San Francisco') WHERE nth=1;
  ```

  Good:

  ```sql
  WITH sf_taco_trucks AS (
    SELECT
      *
      , row_number() OVER (PARTITION BY truck_id) AS nth
    FROM taco_trucks
    WHERE city='San Francisco'
  )
  SELECT * FROM sf_taco_trucks WHERE nth=1
  ;
  ```

* Use descriptive names \(verbose is better than confusing\).

  Bad:

  ```sql
  WITH a AS (
    SELECT customer_id, taco_preference FROM customers
  )
  , b AS (
    SELECT topping_style, taco_type FROM taco_toppings
  )
  SELECT
    a.customer_id
    , b.topping_style
  FROM a
  LEFT JOIN b ON a.taco_preference = b.taco_type
  ```

  Good:

  ```sql
  WITH taco_preferences_by_customer AS (
    SELECT customer_id, taco_preference FROM customers
  )
  , taco_toppings_by_type AS (
    SELECT topping_style, taco_type FROM taco_toppings
  )
  SELECT
    preferences.customer_id
    , toppings.topping_style
  FROM taco_preferences_by_customer AS preferences
  LEFT JOIN taco_toppings_by_type AS toppings ON
    preferences.taco_preference = toppings.taco_type
  ```

* Avoid abbreviations and acronyms - they require the reader to maintain mappings between tables and names.

  Bad:

  ```sql
  SELECT
    tsc.company_id
    , guac.pounds_per_year
  FROM taco_shell_companies AS tsc
  LEFT JOIN guacamole_production AS guac ON tsc.company_id = guac.company_id
  ;
  ```

  Good:

  ```sql
  SELECT
    taco_shell_companies.company_id
    , guacamole_production.pounds_per_year
  FROM taco_shell_companies
  LEFT JOIN guacamole_production ON
    taco_shell_companies.company_id = guacamole_production.company_id
  ;
  ```

* Use `AS` to make it easier to distinguish between fields and aliases

  Bad:

  ```sql
  SELECT tacos_created_per_year tacos_created FROM taco_factories;
  ```

  Good:

  ```sql
  SELECT tacos_created_per_year AS tacos_created FROM taco_factories;
  ```

* Preserve indentation - use indentation to represent logical code blocks, and to help the reader understand what goes together.

  Bad:

  ```sql
  SELECT has_lettuce, has_tomatoes,
          ounces_of_protein
      FROM      crispy_taco_options
     WHERE has_cheese IS TRUE
  ```

  Good:

  ```sql
  SELECT
    has_lettuce
    , has_tomatoes
    , ounces_of_protein
  FROM crispy_taco_options
  WHERE has_cheese IS TRUE
  ```

* Line up your parentheses - this helps the reader quickly find where a block of code ends.

  Bad:

  ```sql
  WITH tacos_per_capita AS (
    SELECT COUNT(tacos) / COUNT(*) FROM tacos_log)
  ```

  Good:

  ```sql
  WITH tacos_per_capita AS (
    SELECT COUNT(tacos) / COUNT(*) FROM tacos_log
  )
  ```

* Reserved SQL gets ALL-CAPS, table/column names get lower-case

  Bad:

  ```sql
  select * from taco_types where shell = 'crispy';
  SELECT * FROM TACO_TYPES WHERE SHELL = 'crispy';
  ```

  Good:

  ```sql
  SELECT * FROM taco_types WHERE shell = 'crispy';
  ```

* If your `where` clause has more than 1 comparison, use the `1=1` trick to get each comparison on its own line with an `and` at the front of the line. This allows you to turn off each filter when debugging, and keeps changes scoped to the line that actually needs to change.

  Bad:

  ```sql
  SELECT
    *
  FROM breakfast_tacos
  WHERE con_papas IS TRUE AND con_chorizo IS TRUE
  ;
  ```

  Good:

  ```sql
  SELECT
    *
  FROM breakfast_tacos
  WHERE 1=1
    AND con_papas IS TRUE
    AND con_chorizo IS TRUE
  ;
  ```

* For `join` clauses that join on more than one condition, each condition should go on its own line \(indented\)

  Bad:

  ```sql
  SELECT
    *
  FROM taco_shells
  LEFT JOIN taco_fillings ON taco_shells.taco_type = taco_fillings.taco_type AND taco_shells.is_crispy IS TRUE
  ```

  Good:

  ```sql
  SELECT
    *
  FROM taco_shells
  LEFT JOIN taco_fillings ON
    taco_shells.taco_type = taco_fillings.taco_type
    AND taco_shells.is_crispy IS TRUE
  ;
  ```

* Every `when` clause in a `case` statement gets its own line \(indented\)

  Bad:

  ```sql
  SELECT
    CASE WHEN has_tomatoes IS TRUE THEN 'tomato-filled' WHEN has_cheese IS TRUE THEN 'cheese-filled' ELSE 'boring' END
  FROM taco_types
  ```

  Good:

  ```sql
  SELECT
    CASE
      WHEN has_tomatoes IS TRUE THEN 'tomato-filled'
      WHEN has_cheese IS TRUE THEN 'cheese-filled'
      ELSE 'boring'
    END
  FROM taco_types
  ```

* Commas go in front, with a space after them. Putting commas in front allows changes in PRs to reflect only the lines that are changing \(think when you have to add a comma to the end of a line that didn't previously have one\).

  Bad:

  ```sql
  SELECT
    con_papas,
    con_queso,
    con_chile
  FROM taco_types
  ```

  Good:

  ```sql
  SELECT
    con_papas
    , con_queso
    , con_chile
  FROM taco_types
  ```

* Semicolons always go on their own line - this helps the reader identify where a query ends.

  Bad:

  ```sql
  SELECT
    *
  FROM taco_trucks;
  ```

  Good:

  ```sql
  SELECT
    *
  FROM taco_trucks
  ;
  ```

* When doing a `union`, include a blank line above and below `union`. This helps the reader identify that there are multiple queries being joined together.

  Bad:

  ```sql
  SELECT
    *
  FROM usa_taco_types
  UNION
  SELECT
    *
  FROM mexico_taco_types
  ;
  ```

  Good:

  ```sql
  SELECT
    *
  FROM usa_taco_types

  UNION

  SELECT
    *
  FROM mexico_taco_types
  ;
  ```

* Use line breaks to make SQL readable. 120 characters per line is a good limit. This will be easy to achieve if you follow the other rules in this guide.
* Multi-sql files should have 2 line spacings between each sql statement.
* Use [ANSI standard SQL functions](https://docs.oracle.com/cd/E57185_01/IRWUG/ch12s04s05.html) over database specific wherever possible.

  Bad:

  ```sql
  NVL(taco_type, 'boring') AS taco_type
  ```

  Good:

  ```sql
  COALESCE(taco_type, 'boring') AS taco_type
  ```

* Don't use `SELECT *`, prefer to explicitly list out only the columns needed. This is especially important when working with views as new columns get added and removed. Listing out the columns serves to prevent against view compliation exceptions and allows for auditing for where columns are being used.
