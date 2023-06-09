# SpoonerInv Flask/MySQL Project

This repo utilizes a boilerplate setup that generates 3 new unique containers: 
1. A MySQL 8 container
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers

This repository is already configured to properly build:
1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`.
1. To completely reset the database, `docker compose down`, then `docker compose up` may help.

## Project Overview

This app is designed to manage customer orders, stock orders, and ingredient production across multiple boba stores organized by region. An app was created via AppSmith - it contains two sample pages for use from a barista's standpoint as well as a manager's standpoint. This app can be found [here](https://github.com/jaredlyon/SpoonerApp).

## Database Design

The `db/` folder generates a custom MySQL database within a MySQL 8 container - this database is then populated using seed data also found in the `db/` folder. Its design follows this relational diagram:
<img width="1193" alt="Screen Shot 2023-04-17 at 8 25 24 PM" src="https://user-images.githubusercontent.com/29807461/232638201-9c0df65e-2b19-4968-a3d3-36dc70a1d94f.png">


... and results in the following database diagram:
<img width="1169" alt="Screen Shot 2023-04-17 at 8 35 32 PM" src="https://user-images.githubusercontent.com/29807461/232639294-1d159d51-69b8-4f59-a973-0f61f78bb84c.png">

