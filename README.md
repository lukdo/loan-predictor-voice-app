
### FrontEnd Webapp and FastAPI-backaend Webapp

so we have 2 webapps. in the ```app_form``` folder is the frontend webform to enter the data
in ```backend``` is the Flask API

Here how to start both locally:
#### frontend app:
listens on 8000
``` bash
cd app_form
docker compose up -d --build
```
#### backend flaskapi app:
listens on 8001
``` bash
cd backend
docker compose up -d --build
```
## Loan Payback Prediction System
Build a predictive model that accurately classifies loan repayment likelihood using supervised learning techniques.

Feature Variables:
" Identifiers: id.
  * Financial Metrics:

 annual_income,
 debt_to_income_ratio,
  credit_score,
  loan_amount,
   interest_rate,
   grade_subgrade.
*  Demographics:
gender,
marital_status,
 education_level,
 employment_status
*  Loan Information:
loan_purpose,
*  Target Variable:
loan_paid_back (binary: 1 = repaid, 0 = default)



#### Working with github branches:

# Git Workflow for a Small Team (Remote Branching + Pull Requests)

## 1. Update your local main

``` bash
git checkout main
git pull origin main
```

## 2. Create a local feature branch

``` bash
git checkout -b feature/foo
```

Now you're on your isolated branch.

## 3. Do your work

``` bash
# edit files...
git add .
git commit -m "Implement feature foo"
```

## 4. Push your feature branch to GitHub (instead of merging locally)

Branches get synchronized remotely, and the merge is done via Pull
Request.

``` bash
git push -u origin feature/foo
```

### 4b. Open a Pull Request (PR)

-   Go to GitHub\
-   Click **"Compare & pull request"**\
-   Add description\
-   Assign reviewers

### 4c. Merge the PR on GitHub

When approved, press **"Merge Pull Request" → "Confirm merge"**.

## 5. Sync your local main after the merge

``` bash
git checkout main
git pull origin main
```

## 6. (Optional) Delete the feature branch

### Delete remote branch

``` bash
git push origin --delete feature/foo
```

### Delete local branch

``` bash
git branch -d feature/foo
```

## Summary of the Remote-Based Workflow

  Step              Local?   Remote?      Command
  ----------------- -------- ------------ ----------------------------------
  Create branch     local    ---          `git checkout -b feature/foo`.

  Work + commit     local    ---          `git add .`, `git commit`.

  Push branch       ---      remote       `git push -u origin feature/foo`.

  PR + review       ---      remote       GitHub UI.

  Merge to main     ---      remote       GitHub UI.

  Sync local main   local    via remote   `git pull origin main`.

  Cleanup           both     both         deletion commands
