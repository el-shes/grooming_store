[![Coverage Status](https://coveralls.io/repos/github/el-shes/grooming_store/badge.svg?branch=master)](https://coveralls.io/github/el-shes/grooming_store?branch=master)
# grooming_store

#Grooming Store
App for convenient grooming store visits

### This app has 3 roles:
Client, Master and Admin. 
That have different level of access and so different set of actions

### Authorization 
As a unique identifier we used phone number, so to create an account u should go to login page and from it click on sign up.
App creates unique token for each user that stores in user’s browser cookies and used to check role of the user and it’s authentication

## Available actions by role
### Client
- Create reservation
- Review reservations (only reservations that belongs to this user)
- Remove reservation (same rule as for review)
- Set marks for master (in development)

### Master
- Review reservations for it per date (in development)

### Admin
- CRUD for Breed
- CRUD for Procedure
- CRUD for users with different roles registrations
- Set working hours for Masters
- Manage set of Procedures for Masters (in development)
- Create Reservations (in development)
