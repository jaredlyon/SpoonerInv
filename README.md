# SpoonerInv Flask/MySQL Project

This repo utilizes a boilerplate setup that generates 3 new unique containers: 
1. A MySQL 8 container
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers

This repository is already configured to properly build (independently of the one we did in class), i.e. we are commit ready!
1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 

test -Nick