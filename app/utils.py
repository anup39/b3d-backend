from .models import Project

def handle_delete_request(id, model):

    if model == "Project":
        project = Project.objects.get(id=id)
        print(project)

    pass