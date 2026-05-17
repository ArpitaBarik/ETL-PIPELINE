# Merge Conflict

## 1. Scenario

A merge conflict occurred in the API parameter construction logic in `api_caller.py`.

## 2. Cause

if Two developers modified the same part of the code:

* Developer A used static variables for performance optimization.
* Developer B introduced dynamic variables for scalability.

## 3. Conflict

Git could not decide which implementation to keep because both changes affected the same line.

## 4. solution

A hybrid solution was implemented:

* Uses dynamic variables when provided
* Falls back to static variables otherwise

## Step-by-Step Process
1.First, I switched to the `dev` branch
(git checkout dev)

2.Then I created a new feature branch called merge-conflict-demo from the dev branch.
(git checkout -b merge-conflict-demo)

3.In the merge-conflict-demo branch, I modified the API parameter logic inside src/utils/api_caller.py using static variables.
("get": "NAME,B23025_001E,B23025_002E")

4.After making the changes, I committed and pushed the branch to GitHub.
(git add .
git commit -m "Added static API handling"
git push origin merge-conflict-demo)

5.Then I switched back to the dev branch.
(git checkout dev)

6.In the dev branch, I modified the same line differently using dynamic variables.
("get": "NAME," + ",".join(variables))

7.After that, I committed and pushed the changes.

8.Then I created a Pull Request in GitHub using:
.Base branch: dev
.Compare branch: merge-conflict-demo

9.GitHub displayed:
Can't automatically merge

10.This happened because both branches modified the same line differently in the same file.

11.To check the conflict locally, I used:
.git status
.git diff

12.During another merge operation, I also faced a practical modify/delete conflict.
(git merge main)

13.Git displayed:
(CONFLICT (modify/delete): task.py deleted in main and modified in HEAD.)

14.This happened because:
(the main branch deleted task.py,
while the dev branch modified task.py.)

15.To resolve the conflict, I decided to keep task.py.
(git add task.py)

16.Then I completed the merge resolution.
(git commit -m "Resolved modify/delete merge conflict by keeping task.py")

17.Finally, I pushed the resolved changes to GitHub.

18.For the API conflict, instead of selecting only one implementation, I combined both static and dynamic approaches.
Final solution:
("get": "NAME," + ",".join(variables) if variables else "NAME,B23025_001E,B23025_002E",)

The final implementation:
.uses dynamic variables when available,
.Falls back to static variables otherwise,
.And makes the solution more scalable, reliable, and production-friendly.