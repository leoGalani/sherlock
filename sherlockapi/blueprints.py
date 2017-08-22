def register_bprints(app):
    from sherlockapi.views.users import user
    from sherlockapi.views.projects import project
    from sherlockapi.views.scenarios import scenario
    from sherlockapi.views.dashboard import dashboard
    from sherlockapi.views.testcases import test_case
    from sherlockapi.views.cycles import cycle
    
    app.register_blueprint(dashboard, url_prefix='/api/dashboard')
    app.register_blueprint(user, url_prefix='/api/user')
    app.register_blueprint(project, url_prefix='/api/project')
    app.register_blueprint(cycle, url_prefix='/api/projects/<int:project_id>/cycle')
    app.register_blueprint(scenario, url_prefix='/api/scenario')
    app.register_blueprint(test_case,
                           url_prefix='/api/scenarios/<int:scenario_id>/tst_case')
