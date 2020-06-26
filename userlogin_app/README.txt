Technical Craft Demonstration Instructions:
Design and develop a RESTful web service that enables the creation of a
new user, login an existing user with username/password and the ability to keep
track of successful/failed login events. A successful solution should include
the software that enables a running solution to this problem (preferably
available on github.com). Also, for a successful craft demonstration, the
candidate should be able to describe the following for the solution: the key
entities and relationships, a well-defined RESTful API, appropriate persistence
mechanism and the software components that implement the solution.

Key Entities:
- Base page -- this is just going to be the landing page from where either yo
- User:
   - userid
   - email
   - password (encrypted/hash)
   - other stats
Relationships:

RESTful APIs:
 * PROVIDE CRUD interface for api endpoints -- wherever applicable.
- /api/<version-num>/users/ GET -- lists the users (only for admins (or if there's some
                           feature in the future which shows community etc.
- /api/<version-num>/users/ POST -- creates a new user
- /api/<version-num>/users/ DELETE -- delete all users (only for admins)
- /api/<version-num>/users/<id> GET -- gets info for user with user-id <id>
- /api/<version-num>/users/<id> PATCH - update information for user with user-ide <id>
- /api/<version-num>/users/<id> DELETE - deletes information for user with user-id <id>


Persistence Mechanism
 - Using postgres as our database (we'll upgrade to a distributed postgres once
   the basic app is complete). Since we are using flask framework for this,
   we will be needing a [container] service which runs postgres, and we'd be
   needing some library which can interact/interface with postgres from flask.
   flask-sqlalchemy is such a library/package which interacts with the database
   using object like semantics with psycopg2 as the middleware.

Code layout:
- config & instance directories at top level is something required by flask
  these contains settings.py which will have configuration parameters for the
  app.
- user-login directory will contain the source code etc. we'll mostly add more
  source code here.
  - we have added a few more folders:
      - blueprints -- will contain different resource handling (for now we only
        have one user and we'll have html pages/route end point redirect etc.)
      - static -- should contain static information like images/scripts
      - templates -- any base templates which the whole application could
        inherit.
      - API -- contains the implementation of our APIs -- we will define class
        based views for different API endpoints.

Steps to build this app:
1. Let's build a basic web app with flask, running as a micro service.
  - This app for now will only implement the bringing up of the webs server
    that will serve the landing page.

    To Run: docker-compose up --build

2. Simple login/signup form. Shamelessly took from:
   https://codepen.io/colorlib/full/rxddKy

3. Using flask-classful, we got our first API plumbing done. i.e., from the
   login page, the post request comes to the back-end. A few additional things
   that were done were to have specified a jinja based form template so we
   the API call plumbing can work without writing lot of html code. From this
   point on, hoping that there's less frontend and more backend. :-)

4. Let's integrate a DB, have an admin user and make sure that the login works
   since we already have login API. We'll be using:
   - postgres as our DB (running in a separate container)
   - flask-sqlalchemy & psycopg as the adapter and middleware for the db. the
     advantage of using this is so that we can write python code (logical
     statements), rather than using actual SQL queries for interacting with our
     db.
5. Create User model and hook up the DB to the app. Also create a CLI to
   interact with the db. We'll extend this CLI to interact/test our APIs as well.
   One issue I faced while doing this is the DB container comes up but the
   POSTGRES_USER/POSTGRES_DB were never created even though we specified that
   as environment variables as per the documentation. To work around this issue
   we just got into the postgres container and created the user and the db used
   manually for now. We'll have to find a way to add this either as a dependency
   or do it programtically somehow. XXX (TODO) for now.

6. Add User login/authorization. Since we already have a seed user, we can test
   with that. TODO: Add settings page where user details can be seen.

7. Now that one API has been added. Add the rest. Now, we have added APIs for:
- /api/<version-num>/users/ GET -- lists the users (only for admins (or if there's some
                           feature in the future which shows community etc.
- /api/<version-num>/users/ DELETE -- delete all users (only for admins)
- /api/<version-num>/users/<id> GET -- gets info for user with user-id <id>
- /api/<version-num>/users/<id> PATCH - update information for user with user-ide <id>
- /api/<version-num>/users/<id> DELETE - deletes information for user with user-id <id>

8. Next step is to review each of these APIs and add security/validation/role-check
  etc. For example, list users should be allowed by user with admin role or the
  logged in user for his own data.
  Among the things to add:
  1. endpoint authentication
  2. request liveliness
  3. unauthorized endpoint access.

  For this, let's first start with users.get call. Only authenticated user or admin
  user is allowed.

9. User delete should be allowed only by admin or the user themselves.
   User update should only be allowed by the user themselves and not admin. (In
  theory we may see the need for admin to also be allowed to change the info,
  but for the sake of this, we'll keep things like this.

  
