# ROUTER
import asyncio, importlib, mimetypes, sys, os


class Router:
    def __init__(self, host: str = "localhost", port: int = 8000) -> None:
        self.host = host
        self.port = port
    async def runner(self) -> None:
        server = None  # Initialize server outside the try block
        try:
            server = await asyncio.start_server(self.handler, host=self.host, port=self.port)
            address = server.sockets[0].getsockname()
            print(f"\033[92mServing on {address[0]}:{address[1]}\033[0m")
            async with server:
                await server.serve_forever()
        except Exception as error:
            print(error)
        finally:
            if server:
                server.close()
                await server.wait_closed()
                print("\r\033[91mAll the connections closed!\033[0m")
    async def handler(self, reader, writer) -> None:
        data = await reader.read(100)
        message = data.decode()
        request_line = message.split("\r\n")[0]
        try:
            method, path, _ = request_line.split(" ")
        except ValueError:
            # Handle the case where there are not enough values in request_line
            method, path, _ = "", "", ""

        fileordir = os.path.splitext(path)[1] if os.path.splitext(path)[1] else None

        if fileordir is None:
            await self.handle_dynamic_page(path, writer)
        else:
            await self.handle_static_file(path, writer)
    async def handle_dynamic_page(self, path: str, writer) -> None:
        try:
            module_name = "application.online.pages.home.index" if path == "/" else f"application.online.pages.other.{'.'.join(path.strip('/').split('/'))}.index"
            module = importlib.import_module(module_name)
            # Check if the module is already in sys.modules
            if module_name in sys.modules:
                # Reload the module to apply changes
                module = importlib.reload(module)
            main_function = getattr(module, "main")
            response_content = main_function()
            await self.send_response(writer, 200, response_content, "text/html; charset=utf-8")
        except (ImportError, AttributeError):
            module_name = "application.online.pages.error.notfound"
            module = importlib.import_module(module_name)
            # Check if the module is already in sys.modules
            if module_name in sys.modules:
                # Reload the module to apply changes
                module = importlib.reload(module)
            main_function = getattr(module, "main")
            response_content = main_function()
            await self.send_response(writer, 404, response_content, "text/html; charset=utf-8")
    async def handle_static_file(self, path: str, writer) -> None:
        file_path = "application/online/public" + path
        if os.path.exists(file_path):
            try:
                # Use asyncio to read the file asynchronously
                response_content = await self.read_file_async(file_path)
                content_type = get_content_type_from_mime(mimetypes.guess_type(file_path)[0] or "application/octet-stream")
                # Decode the bytes content to string
                response_content = response_content.decode('utf-8')

                await self.send_response(writer, 200, response_content, content_type)
            except Exception as Error:
                print(Error)
                await self.send_response(writer, 500, "<h1>Internal Server Error</h1>", "text/html; charset=utf-8")
        else:
            await self.send_response(writer, 404, "<h1>404 Not Found</h1>", "text/html; charset=utf-8")
    async def read_file_async(self, file_path: str) -> bytes:
        # Read the file asynchronously using asyncio and run_in_executor
        loop = asyncio.get_event_loop()
        with open(file_path, "rb") as file:
            return await loop.run_in_executor(None, file.read)
    async def send_response(self, writer, status_code: int, response_content: str, content_type: str) -> None:
        status_line = f"HTTP/1.1 {status_code} {self.get_status_message(status_code)}\r\n"
        headers = f"Content-Type: {content_type}\r\nServer: Electron Beta\r\n"
        empty_line = "\r\n"
        response = status_line + headers + empty_line + str(response_content)
        writer.write(response.encode())
        await writer.drain()
        writer.close()
    def get_status_message(self, status_code: int) -> str:
        # Map common status codes to their messages
        status_messages = {
            200: "OK",
            404: "Not Found",
        }
        return status_messages.get(status_code, "Unknown Status")
def get_content_type_from_mime(mime: str) -> str:
    # Map file extensions to content types
    content_types = {
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".svg": "image/svg+xml; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".xml": "application/xml; charset=utf-8",
        ".pdf": "application/pdf; charset=utf-8",
        ".doc": "application/msword",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".bmp": "image/bmp",
        ".tiff": "image/tiff",
        ".ico": "image/x-icon",
        ".mp3": "audio/mpeg",
        ".ogg": "audio/ogg",
        ".wav": "audio/wav",
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".avi": "video/x-msvideo",
        ".mov": "video/quicktime",
        ".zip": "application/zip",
        ".txt": "text/plain; charset=utf-8",
        ".md": "text/markdown",
    }
    # get the file extention
    extension = mimetypes.guess_extension(mime)
    # Return the corresponding content type or default to text/plain
    return content_types.get(extension.lower(), "text/plain")
