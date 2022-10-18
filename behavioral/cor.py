# Chain of Responsibility Design Pattern
# Example: API Request Handler
# Author: Noxtal
# Reference: https://refactoring.guru/design-patterns/chain-of-responsibility


from __future__ import annotations

from typing import Optional
import re


class RequestHandler:
    """
    Abstract class for a request handler and its chaining mechanism
    """

    def __init__(self):
        self.next_handler = None

    def _handle(self, request: str) -> Optional[str]:
        return None

    def handle(self, request: str) -> Optional[str]:
        """
        Handle a given request
        :param request: An HTTP request
        :return: The original request or None if it was not handled
        """
        result = self._handle(request)
        return result if self.next_handler is None else self.next_handler.handle(result)

    def next(self, handler: RequestHandler) -> RequestHandler:
        """
        Set the next handler in the chain
        :param handler: The next handler
        :return: The given next handler (for chaining)
        """
        self.next_handler = handler
        return handler


class VerbHandler(RequestHandler):
    """
    A request handler for a specific HTTP verb
    """

    def __init__(self, verb: str):
        super().__init__()
        self.verb = verb

    def _handle(self, request: str) -> Optional[str]:
        if request is not None:
            m = re.search("^([A-Z]{2,})", request)
            if m is not None:
                if m.group(1) == self.verb:
                    return request
        return None


class RouteHandler(RequestHandler):
    """
    A request handler for a specific HTTP route
    """
    def __init__(self, route: str):
        super().__init__()
        self.route = route

    def _handle(self, request: str) -> Optional[str]:
        if request is not None:
            m = re.search("^[A-Z]{2,} (/[^ ]*)", request)
            if m is not None:
                if m.group(1) == self.route:
                    return request
        return None


class CookieHandler(RequestHandler):
    """
    A request handler for a specific cookie, such as an API key
    """
    def __init__(self, key: str, expected: str):
        super().__init__()
        self.key = key
        self.expected = expected

    def _handle(self, request: str) -> Optional[str]:
        if request is not None:
            m = re.search(f"cookie:.+{self.key}=([^ ;,]+);", request)
            if m is not None:
                if m.group(1) == self.expected:
                    return request
        return None


if __name__ == "__main__":
    # Build the chain
    handler = VerbHandler("GET")
    handler.next(RouteHandler("/api/key")).next(CookieHandler("KEY", "Pa$$w0rd"))

    request = """GET /api/key HTTP/1.1
Host: localhost:8080
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36
cookie: KEY=Pa$$w0rd;
    """

    print("Request 1 (should be true)", handler.handle(request) is not None)

    request = """POST /api/key HTTP/1.1
Host: localhost:8080
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36
cookie: KEY=Pa$$w0rd;
    """

    print("Request 2 (should be false)", handler.handle(request) is not None)

    request = """GET /api/nope HTTP/1.1
Host: localhost:8080
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36
cookie: KEY=Pa$$w0rd;
        """

    print("Request 3 (should be false)", handler.handle(request) is not None)

    request = """GET /api/key HTTP/1.1
Host: localhost:8080
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36
cookie: KEY=wrong;
        """

    print("Request 4 (should be false)", handler.handle(request) is not None)