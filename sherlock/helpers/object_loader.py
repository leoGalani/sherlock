"""Load Objects to be displayed on the sherlock application."""
from flask import g
from sherlock import cache


@cache.memoize(50)
def project_loader(Project):
    """Get all projects and retrive to the global flask G."""
    g.projects = Project.query.all()
