import requests
import os

# Configurações
USERNAME = "Fesisp"
URL = f"https://api.github.com/users/{USERNAME}/repos?sort=updated"

def get_repos():
    response = requests.get(URL)
    return response.json()

def generate_markdown():
    repos = get_repos()
    project_list = ""
    all_tags = set()

    for repo in repos:
        if not repo['fork'] and repo['name'] != USERNAME:
            name = repo['name']
            url = repo['html_url']
            desc = repo['description'] or "Sem descrição."
            tags = repo['topics']
            all_tags.update(tags)
            
            project_list += f"* [**{name}**]({url}) - {desc}\n"

    # Criando a tabela de habilidades baseada em tags
    skills_table = "| Categoria | Tags Detectadas |\n| :--- | :--- |\n"
    skills_table += f"| **Tecnologias** | {', '.join(sorted(all_tags))} |\n"

    return project_list, skills_table

def update_readme(projects, skills):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Injeção dos Projetos
    start_p = ""
    end_p = ""
    new_content = content.split(start_p)[0] + start_p + "\n" + projects + content.split(end_p)[1]

    # Injeção das Habilidades
    start_s = ""
    end_s = ""
    final_content = new_content.split(start_s)[0] + start_s + "\n" + skills + new_content.split(end_s)[1]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(final_content)

if __name__ == "__main__":
    p_list, s_table = generate_markdown()
    update_readme(p_list, s_table)
