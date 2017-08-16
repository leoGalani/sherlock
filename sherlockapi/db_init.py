def check_first_run(db):
    db.create_all()

    from sherlockapi.data.model import User, SherlockSettings

    user = User.query.filter_by(id=1).first()
    if user == None:
        initial_user = User(name='Admin',
                            email='admin@admin.xpto',
                            password='admin',
                            profile='admin')
        db.session.add(initial_user)
        db.session.commit()

    # SherlockSettings
    open_register_setting = SherlockSettings.query.filter_by(setting='OPEN_USER_REGISTER').first()
    if not open_register_setting:
        open_user_register = SherlockSettings('OPEN_USER_REGISTER', 'True', 'Anyone can register?')
        db.session.add(open_user_register)
        db.session.commit()
