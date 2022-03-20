from app.todo import manager


def fill_db():
    manager.add_task('A')
    manager.add_task('B')
    manager.add_task('C')
    manager.add_task('D')
    manager.finish_task(3)
    manager.finish_task(4)
