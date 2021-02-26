"""Utils for messages system"""

def render_template(template_name: str, *args) -> str:
    with open(f'./templates/{template_name}.md', 'r') as template_file:
        return (template_file.read()).format(*args)
