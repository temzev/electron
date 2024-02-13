from typing import Any

class html:
    def __init__(self, *children: Any, attributes: dict = None) -> None:
        self.attributes = attributes
        self.children = children

    def __str__(self) -> str:
        content = "".join(map(str, self.children))
        if self.attributes:
            attributesstring = " ".join([f'{key}="{value}"' for key, value in self.attributes.items()])
            result = f"<html {attributesstring}>\n{content}\n</html>\n"
        else:
            result = f"<html>\n{content}\n</html>\n"
        result = "\n".join(line for line in result.split("\n") if line.strip())
        html = result.split("\n")
        current_indentation = 0
        indentation = 4
        output = ""
        #
        dumbtags = ["meta", "link"]
        #
        for line in html:
            start = line[0:2]
            if start.startswith("<") and f"{line.split()[0][1:]}" in dumbtags:
                output += " " * indentation * current_indentation + line + "\n"
            else:
                if start.startswith("<") and start[1] != "/":
                    output += " " * indentation * current_indentation + line + "\n"
                    current_indentation += 1
                elif start.startswith("<") and start[1] == "/":
                    current_indentation -= 1
                    output += " " * indentation * current_indentation + line + "\n"
                else:
                    output += " " * indentation * current_indentation + line + "\n"
        return f"<!DOCTYPE html>\n{output}"




def complextag(tagname: str):
    def decorator(*children: Any, attributes: dict = None) -> str:
        content = "\n".join(map(str, children))
        if attributes:
            attributesstring = " ".join([f'{key}="{value}"' for key, value in attributes.items()])
            return f"<{tagname} {attributesstring}>\n{content}\n</{tagname}>\n"
        else:
            return f"<{tagname}>\n{content}\n</{tagname}>\n"
    return decorator


def simpletag(tagname: str):
    def decorator(attributes: dict = None) -> str:
        if attributes:
            attributesstring = " ".join([f'{key}="{value}"' for key, value in attributes.items()])
            return f"<{tagname} {attributesstring}>\n"
        else:
            return f"<{tagname}>\n"
    return decorator


head = complextag("head")
title = complextag("title")
metadata = simpletag("meta")
link = simpletag("link")
body = complextag("body")
paragraph = complextag("p")
division = complextag("div")
header = complextag("h1")
hyperlink = complextag("a")
