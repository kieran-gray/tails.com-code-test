## Coding test for Tails.com by Kieran Gray

### Running the application
To start:

`sudo docker compose up --build`

This command:

    - builds the application image
    - pulls the postgresql image
    - starts the postgresql and application containers
    - runs the database population script

The postgres container is running on port 5432 but is exposed on port 5433 so it should run alongside a postgres
instance running on your machine.

If not then it may be necessary to run the following command on your machine:

`service postgresql stop`

#### Using the application

The application will be available at http://localhost:5000

There are 3 different view types:

    - list
    - map
    - api

They can each be accessed as follows:

    - http://localhost:5000/{view_type}/
    
    - http://localhost:5000/{view_type}/filter/?postcode={postcode}&radius={radius}