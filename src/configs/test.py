from yaml import safe_load

with open("./prompts.yml") as f:
    c = safe_load(f)

print(c)