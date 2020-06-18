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
- user-login/users/ GET -- lists the users (only for admins (or if there's some
                           feature in the future which shows community etc.
- user-login/users/ PUT -- creates a new user
- user-login/users/ DELETE -- delete all users (only for admins)
- user-login/users/<id> GET -- gets info for user with user-id <id>
- user-login/users/<id> PATCH - update information for user with user-ide <id>
- user-loging/users/<id> DELETE - deletes information for user with user-id <id>


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
-

Steps to build this app:
1. Let's build a basic web app with flask, running as a micro service.
  - This app for now will only implement the bringing up of the webs server
    that will serve the landing page.

    To Run: docker-compose up --build
