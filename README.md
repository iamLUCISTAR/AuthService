# Multi-tenant Saas authentication system
Api's for handling multi-tenant saas backend operations for handling the below scenarios.
- Creating a user and assigning a role for him in a organization.
- Inviting members from different organizations.
- Updating and deleting the role of the members in the organization.
- Sending alert mails for each action performed.
- Retrieving number of users based on organization and roles with filters such as from and to date.

**Django REST framework** along with **sqlite3** was used to develop the project to keep the application scalable and maintainable.

## DB design
4 tables as mentioned in the requirements with necessary contstraint and keys have been modeled. A 5th table **Invitation** is included to keep track of sent invitations.

![Database Schema](https://github.com/iamLUCISTAR/AuthService/blob/master/Screenshot%202024-09-14%20at%2012.14.31%20PM.png?raw=true)


## Code

Running the python manage.py hosts the dev server for the application in local instance. 
Endpoints for each api's can be found in the urls.py file.

Postman export JSON file is included in the main repo to browse the api's.

Code respository is defined in the below structure,

- api (main application)
  - auth (hosts auth services)
  - stats (hosts stats services)

## Use cases covered

1. **Sign Up**
   - Users can be created with orgainization details and role specification.
2. **Sign In**
   - Verifies user encrypted password from the user table and returns a JWT Token(Access token and Refresh token).
3. **Reset Password**
   - User can reset his account password if he is already a user and send password change alert.
4. **Update and Delete member**
   - Members role can be updated and deleted.
5. **Send and Accept Invite**
   - Existing members can invite another user using an invite-member mail with a token with some expiry time.
   - Upon invite acceptance the user will added with the invited role in the system, if he accepts before the token expiration.
6. **Email alert for every actions**
   - Sign up
   ![Sign up](https://github.com/iamLUCISTAR/AuthService/blob/master/Screenshot%202024-09-14%20at%2011.49.23%20AM.png?raw=true)

   - Sign in
   ![Sign in](https://github.com/iamLUCISTAR/AuthService/blob/master/Screenshot%202024-09-14%20at%2011.49.32%20AM.png?raw=true)

   - Password update
   ![Password change](https://github.com/iamLUCISTAR/AuthService/blob/master/Screenshot%202024-09-14%20at%2011.49.43%20AM.png?raw=true)

   - Invite member
   ![Invite member](https://github.com/iamLUCISTAR/AuthService/blob/master/Screenshot%202024-09-14%20at%2011.49.52%20AM.png?raw=true)

7. **Stats of users**
   The api's expect JWT token as part of the request header. Requests without the JWT token will not be served.
   - Get the count of users role wise.
   - Get the count of users organization wise.
   - Get the count of users based on roles and the organization.
   - Each stats request can take three filters and display the filtered results.
     - Created before
     - Created after
     - Status

## Author

- [Sharath Bhadrinath](https://github.com/iamLUCISTAR)
