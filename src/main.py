from gencontent import generate_page, generate_page_recursive
from textnode import TextNode


def main():
    # text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    # print(text_node.__repr__())
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_page_recursive("content", "template.html", "public")


main()
