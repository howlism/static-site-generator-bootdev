from textnode import TextNode, TextType


def main():
    my_node = TextNode("textopolis", TextType.LINK, "https://www.google.com")
    print(my_node)


if __name__ == "__main__":
    main()
