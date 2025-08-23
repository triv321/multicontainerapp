# **Project: Multi-Container Application with a Persistent Database**

A multi-container web application featuring a Python Flask API and a persistent PostgreSQL database, fully orchestrated with Docker Compose. This project demonstrates how to build and manage stateful applications using Docker Volumes.

## **Table of Contents**

1. [Overview](https://www.google.com/search?q=%23overview)  
2. [Core Features](https://www.google.com/search?q=%23core-features)  
3. [Architecture](https://www.google.com/search?q=%23architecture)  
4. [Prerequisites](https://www.google.com/search?q=%23prerequisites)  
5. [Quickstart](https://www.google.com/search?q=%23quickstart)  
6. [Project Details](https://www.google.com/search?q=%23project-details)  
7. [Development](https://www.google.com/search?q=%23development)

## **Overview**

This project is the capstone for the "Deep Dive into Docker" module. It addresses the most critical challenge in containerizing real-world applications: **data persistence**. While stateless services are simple to containerize, any application that needs to save data—like a database—requires a robust strategy to ensure that data is not lost when a container is stopped or removed.

This application simulates a simple visit tracker. A Python **Flask** application serves as an API that connects to a **PostgreSQL** database. The entire system is defined and orchestrated using a single **docker-compose.yml** file. The key innovation in this project is the use of a **Docker Named Volume** to provide a permanent, safe storage location for the PostgreSQL database, completely separate from the container's ephemeral lifecycle.

## **Core Features**

* **Stateful Multi-Service Architecture:** A complete application with a stateless API container and a stateful database container.  
* **Guaranteed Data Persistence:** Utilizes a Docker Named Volume to ensure that all database data is safely preserved, even after containers are removed and recreated.  
* **Declarative Orchestration:** The entire application stack, including services, networks, and volumes, is defined in a single docker-compose.yml file.  
* **Environment Variable Configuration:** The application is configured using environment variables passed from Docker Compose, a best practice for separating configuration from code.

## **Architecture**

The application consists of two services running in isolated containers on a shared virtual network. The PostgreSQL container's data directory is mounted to a persistent Docker Volume managed on the host.

      \+-----------------------------+  
      |      User's Web Browser     |  
      \+-----------------------------+  
                  |  
                  | (HTTP Request on localhost:5000)  
                  |  
\+-----------------V----------------------------------------------------+  
| Host Machine (Your Laptop)                                           |  
|                                                                      |  
|  \+-----------------------+         \+-------------------------------+  |  
|  |   app (Flask API)     |         |   db (PostgreSQL)             |  |  
|  |                       |--(Network Communication using hostname)--\>|  |  
|  |  Container            |         |   Container                   |  |  
|  \+-----------------------+         \+-------------------------------+  |  
|                                                ^                       |  
|                                                | (Data Persistence)    |  
|                                                |                       |  
|                                     \+--------------------------+       |  
|                                     | Docker Managed Volume    |       |  
|                                     |    (postgres\_data)       |       |  
|                                     \+--------------------------+       |  
\+----------------------------------------------------------------------+

## **Prerequisites**

* **Git:** To clone the project repository.  
* **Docker & Docker Compose:** The Docker engine must be installed and running.

## **Quickstart**

1. **Clone the repository:**  
   git clone https://github.com/triv321/multi-container-docker\_app.git  
   cd multi-container-docker\_app

2. Launch the application:  
   This command will build the Flask application image, pull the PostgreSQL image, create the named volume, and start both containers. The \--build flag ensures the image is rebuilt if you've made changes.  
   docker compose up \--build

3. Access the application:  
   Open your web browser and navigate to http://localhost:5000. You should see a JSON response showing the first visit.  
4. **Test for Persistence:**  
   * Refresh the page several times to add more visits.  
   * Go to your terminal and shut down the application completely: docker compose down.  
   * Relaunch the application: docker compose up.  
   * Refresh your browser. You will see that **all your previous visits are still there**, proving that the data was safely persisted in the volume.

## **Project Details**

### **Design Decisions**

#### **Named Volumes vs. Bind Mounts**

The most critical architectural decision in this project was how to handle the database's data.

* **Bind Mounts** (like .:/app) are a "window" into the host's filesystem. They are perfect for mounting source code during development but are not ideal for production data, as they are tied to the host's directory structure.  
* **Named Volumes** (like postgres\_data) are the professional standard for persisting container data. They are like a dedicated, managed "filing cabinet" that Docker creates and protects. The data's lifecycle is completely decoupled from the container's, which is the key to building stateful applications.

The docker-compose.yml file uses both: a bind mount for the app service's code (for development) and a named volume for the db service's data (for persistence).

#### **Configuration via Environment Variables**

The Python application does not contain any hardcoded database credentials. Instead, it reads its configuration from environment variables:

DB\_USER \= os.getenv("POSTGRES\_USER")  
DB\_PASSWORD \= os.getenv("POSTGRES\_PASSWORD")

These variables are securely passed into the container from the docker-compose.yml file, a best practice for separating configuration from application code.

services:  
  app:  
    environment:  
      \- POSTGRES\_USER=myuser  
      \- POSTGRES\_PASSWORD=mypassword

## **Development**

The project is set up for a smooth development workflow. The bind mount on the app service ensures that any changes saved to app.py on the local machine are instantly reflected in the running container, with Flask's debug mode automatically reloading the server.