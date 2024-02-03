# FastAPI Simple Blog API

This project is a demonstration of building a simple RESTful API using FastAPI, featuring user authentication, authorization, CRUD operations for blogs, pagination, and sorting. The technology stack includes Python, FastAPI, Pydantic, MongoDB, and Docker.

## Project Overview

The primary objectives of this project were to showcase proficiency in FastAPI, implement user authentication and authorization with JWT, manage CRUD operations for blog data, and incorporate features such as pagination and sorting. The code adheres to best practices for code structure and API architecture.

## Technology Stack

- **Python:** The primary programming language.
- **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python.
- **Pydantic:** Used for data validation and settings management.
- **MongoDB:** A NoSQL database used for storing blog data.
- **Docker:** Containerization for easy deployment and scalability.

## API Endpoints

### Authentication

- **Register new users**
- **Login existing users**
- **Update user profiles**
- **Add/remove user tags (keywords or interests)**

### Blogs

- **Create new blogs**
- **Retrieve all blogs (with pagination)**
- **Retrieve a specific blog by ID**
- **Update existing blogs**
- **Delete blogs**

### Dashboard

- **Fetch all blogs matching user's followed tags (sorted by relevance)**
- **Implement sorting logic to prioritize blogs with tags the user likes**
- **Implement pagination**

## Deployment

The API is Dockerized for easy deployment. It has been deployed to [render.com](https://render.com/) for testing and evaluation.

- **Deployment URL:** [API on render.com](https://your-api-render-url.com)

## Brownie Points Achieved

- **Testing:** Unit and integration tests for API endpoints have been implemented.
- **Dockerization:** A Dockerfile is provided to containerize the API.

## Bonus Points

- **Additional Features:** (List any additional features implemented beyond core requirements)
- **Advanced FastAPI Features:** (Describe any exploration of advanced FastAPI features, e.g., background tasks, dependency injection)
- **Security and Performance Optimization:** (Highlight any best practices applied for security and performance optimization)

## Project Structure

- **`app/`:** Contains the main application code.
- **`tests/`:** Houses unit and integration tests.
- **`docker/`:** Docker-related files, including the Dockerfile.

## Getting Started

To run the project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your-repository
   ```

3. Build and run the Docker container:

   ```bash
   docker build -t fastapi-blog-api .
   docker run -p 8000:8000 fastapi-blog-api
   ```

4. Access the API at `http://localhost:8000`.

## Contribution Guidelines

If you'd like to contribute to the project, please follow the contribution guidelines outlined in the `CONTRIBUTING.md` file.

## Additional Notes

Feel free to reach out with any questions or feedback. Creativity and problem-solving skills are highly valued, so showcase your best work!

Happy coding!
