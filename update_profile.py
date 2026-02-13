import requests
import os

USERNAME = "Fesisp"
URL = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=100"

def get_repos():
    response = requests.get(URL)
    return response.json() if response.status_code == 200 else []

def generate_content():
    repos = get_repos()
    project_list = ""
    detected_tags = set()

    for repo in repos:
        if not repo['fork'] and repo['name'] != USERNAME:
            name = repo['name']
            url = repo['html_url']
            desc = repo['description'] or "Projeto em desenvolvimento."
            topics = repo.get('topics', [])
            detected_tags.update(topics)
            project_list += f"* [**{name}**]({url}) - {desc}\n"

    skills_content = "| Categoria | Tecnologias Detectadas via GitHub Topics |\n| :--- | :--- |\n"
    skills_content += f"| **Stack Ativa** | {', '.join(sorted(detected_tags)) if detected_tags else 'Adicione Topics nos seus repositórios'} |\n"
    return project_list, skills_content

def update_readme(projects, skills):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    try:
        start_p, end_p = "", ""
        content = content.split(start_p)[0] + start_p + "\n" + projects + content.split(end_p)[1]
        start_s, end_s = "", ""
        content = content.split(start_s)[0] + start_s + "\n" + skills + content.split(end_s)[1]
    except: return
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    p, s = generate_content()
    update_readme(p, s)
