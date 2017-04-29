
class cb_client:
    def __init__(this,  action):
        this.action = action

    def perform(this, command_name):
        this.command_name = command_name
        return this.action(this.command_name)