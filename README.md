# Celery Tasks Usage Guide

This guide explains how to use the Celery tasks defined in our worker setup from other codebases.

## Setup

To use these Celery tasks in your project, you need to install Celery and set up a connection to our Redis instance.

1. Install Celery:
   ```
   pip install celery
   ```

2. In your project, create a Celery app that connects to our Redis instance:

   ```python
   from celery import Celery

   app = Celery('tasks',
                broker='redis://your-redis-url',
                backend='redis://your-redis-url')

   # Make sure the task names match those in our deployed tasks.py
   app.conf.task_routes = {
       'perplexity_clone_api_task': {'queue': 'default'},
   }
   ```

   Replace `'redis://your-redis-url'` with the actual URL of our Redis instance.

## Using the Tasks

Once you have set up the Celery app, you can send tasks to our worker:

    ```python
    #To send a task
    result = app.send_task('perplexity_clone_api_task',
    args=[main_url, user_message, query_id])
    #To get the result
    task_result = result.get()
    ```

Replace `main_url`, `user_message`, and `query_id` with your actual values.

## Available Tasks

Currently, we have the following task available:

- `perplexity_clone_api_task`: This task sends a query to the Perplexity Clone API and returns the response.

## Notes

- Ensure that your Redis URL is kept secure and not exposed in your code.
- The `task_result.get()` call is blocking. In a production environment, you might want to handle this asynchronously.
- If you encounter any issues or need to add new tasks, please contact the infrastructure team.

------------------------------------------------------------------------------------------------

To use this setup:
Deploy the celery_worker folder contents to Render using the render.yaml file inside it.
In your main project or any other codebase that needs to use these Celery tasks:

    ```python
    from celery import Celery

    app = Celery('tasks',
                broker='redis://your-redis-url',
                backend='redis://your-redis-url')

    # Make sure the task names match those in your deployed tasks.py
    app.conf.task_routes = {
        'perplexity_clone_api_task': {'queue': 'default'},
    }

    # To send a task
    result = app.send_task('perplexity_clone_api_task', 
                        args=[main_url, user_message, query_id])

    # To get the result
    task_result = result.get()
    task_result = result.get()
    ```

This setup allows you to:

- Keep your Celery worker code separate from your main project.
- Deploy the Celery worker independently on Render.
Use the Celery tasks from any project that has the correct Redis URL and task names.
Remember to secure your Redis instance and use environment variables for sensitive information like URLs and credentials.