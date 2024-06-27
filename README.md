# my-assessment

This repository contains the completed tasks for the Qtx/Chisl technical assesment.
It consists of two distinct tasks, these being:

- [ ] SQL (Task 1)
- [ ] Python (Task 2)

## Getting Started
The assessment must be completed in a Docker contrainer to ensure that the envrionment you work in is the same as our testing environment.

1. Install Docker on your system from https://www.docker.com
2. Build and run the docker image from the Dockerfile using the following terminal commands:
    - `docker build -t assessment .`
    - `docker run -it -p 8888:8888 -v "${PWD}:/app" assessment` 
3. A unique URL will apear in the terminal similar to the one seen in the image below. Enter this URL in your browser and complete the assessment there.
## ![Alt text](<jupyter URL.png>)

4. Any changes made in the docker container should reflect locally. Ensure that this is the case.
5. When you close jupyter in your browser, be sure to also close the container by using `Ctrl + c` in the terminal.
6. To remove any dangling images/stopped containers, you can use the following command:
    - `docker system prune`

    NOTE: You are able to work in VS Code, however, this is not recomended when working with jupyter notebooks, especially within a container. If you still wish to do so, restart VS Code each time you exit the Docker container to avoid any errors.

## Tasks:
### Task 1 - SQL
- The `SQL.py` and `Advanced_SQL.py` files, found in the `Task_1` folder, contain all of the SQL related questions in the assessment.  **These are the only Task 1 files that will be considered in the grading of your assessment.**
- Task 1 questions are in the form of python functions that simply return a string of your SQL query. The returned SQL query will be run by duckdb's python client as seen in the `Check_your_SQL.ipynb` notebook.
- To verify that your SQL queries are structured as intended, you can run the question functions or any other SQL queries within the `Check_your_SQL.ipynb` notebook to return a result set in the form of a dataframe.


### Task 2 - Python
- The `Python.py` file, found in the `Task_2` folder, contains the python related questions in the assessment. **This is the only Task 2 file that will be considered in the grading of your assessment.**
- The `.csv` files located in the `Task_2/data` folder contain the datasets required to answer the python questions.


