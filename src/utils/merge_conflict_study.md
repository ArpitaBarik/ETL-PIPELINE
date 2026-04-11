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

## 5. Final Code

```python
params = {
    "get": "NAME," + ",".join(variables) if variables else "NAME,B23025_001E,B23025_002E",
    "for": "metropolitan statistical area/micropolitan statistical area:*",
    "key": CENSUS_API_URL
}
```

## 6. Conclusion

This resolution balances performance and scalability, making the API caller more flexible and robust.
