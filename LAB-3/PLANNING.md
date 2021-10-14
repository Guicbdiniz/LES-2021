# Planning

- REST API
    - We think it is easier.
    - We have never made any CLI app.
    
- Flask
    - We believe that the Flask framework is the simplest option to use.
    - We only need one route.
        - It must receive an issue title and return if it is a bug or not.
        - POST
        - Request body:
        ```json
        {
          "title": "title example"
        }
        ```
        - Response format:
        ```json
        {
          "type": "bug/non-bug" 
        } 
        ```