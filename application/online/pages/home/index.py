from ....engine.html import html, head, title, metadata, link, body, division, header, paragraph



def main():
    return html(
        head(
            title("Python Website"),
            metadata({"charset": "utf-8"}),
            metadata({"name": "viewport", "content": "width=device-width, initial-scale=1.0"}),
            link({"rel": "icon", "href": "favicon.svg", "sizes": "any", "type": "image/svg+xml"}),
            link({"rel": "stylesheet", "href": "style.css"}),
        ),
        body(
            division(
                header("This is the Home Page"),
                paragraph("Try go to a page that does not exists."),
                attributes = {"class": "container"},
            ),
        ),
        attributes = {"lang": "en", "dir": "auto"}
    )
