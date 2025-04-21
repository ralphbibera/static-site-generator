from markdown_blocks import markdown_to_html_node
import os


def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path, "r").read()
    template = open(template_path, "r").read()
    title = extract_title(md)
    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')
    open(dest_path, "w").write(template)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str
):
    for path in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, path)

        if os.path.isfile(full_path):
            generate_page(
                full_path,
                template_path,
                os.path.join(dest_dir_path, path).replace(".md", ".html"),
                base_path,
            )
        else:
            if not os.path.exists(os.path.join(dest_dir_path, path)):
                os.makedirs(os.path.join(dest_dir_path, path))

            generate_pages_recursive(
                full_path, template_path, os.path.join(dest_dir_path, path), base_path
            )


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no title found")
