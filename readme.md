# Python Web Framework - Preliminary Alpha

This Python code implements a HTTP server using the asyncio library.

The server includes a router capable of handling both dynamic pages and static files.

## Bug
**Not functioning correctly on Windows**

**Can't be stopped after running on Windows**

## Usage

1. **Initialization:**
   - Instantiate the `Router` class with optional `host` and `port` parameters (default: "localhost", 8000).

    ```python
    server = Router(host="localhost", port=8000)
    ```

2. **Running the Server:**
   - To start the server, call the `runner` method.

    ```python
    asyncio.run(main = server.runner())
    ```

   This will print the server address (e.g., "Serving on 127.0.0.1:8000") and serve incoming requests indefinitely.

3. **Dynamic Pages:**
   - Dynamic pages are handled through the `handle_dynamic_page` method. You can create modules representing different pages under the `application.online.pages` package.

   Example dynamic page module structure:
    ```
    application/
    └── online/
        └── pages/
            ├── home/
            │   └── index.py
            └── other/
                └── page_name/
                    └── index.py
    ```

4. **Static Files:**
   - Static files are served from the "application/online/public" directory. Make sure to organize your static files within this directory.

    Example static file structure:
    ```
    application/
    └── online/
        └── public/
            ├── css/
            ├── js/
            └── other/
    ```

## Important Considerations

1. **Error Handling:**
   - The code includes basic error handling, but you may want to enhance it for better diagnostics.

2. **Security:**
   - Ensure proper input validation and data sanitization, especially for dynamic pages.

3. **Logging:**
   - Consider implementing logging to capture errors and facilitate debugging.


4. **Cross-Origin Resource Sharing (CORS):**
   - If your application is accessed by clients from different origins, consider adding CORS headers to responses.

## Customization

1. **Content-Type Handling:**
   - The `get_content_type` method is provided for mapping file extensions to content types. Adjust it according to your needs.

2. **Logging:**
   - Add more detailed logging statements throughout the code for better traceability.

3. **Testing:**
   - Write unit tests to ensure the correctness of the server's behavior, especially for handling dynamic pages and static files.

4. **Portability:**
   - If cross-platform compatibility is essential, consider using a library like `colorama` for colored output.

Feel free to customize the code based on your specific use case and requirements.
