"""
`ActionHandler` and default actions classes.

The `ActionHandler`, available through `obj.actions`  once installed,
can be used to create actions with various priorities.  The `AwareStorage`
script is used to store actions and retain priority orders.

"""

from evennia import ScriptDB
from evennia.utils.create import create_script
from evennia.contrib.aware.scripts import AwareStorage

class ActionHandler(object):

    """
    Action handler accessible through `obj.actions`.

    This handler allows to add actions per priority, get current
    actions, and remove an action from this priority list.

    """

    def __init__(self, obj):
        self.obj = obj

    def all(self):
        """
        Return the sorted list of all actions on this object.

        Note:
            The list is already sorted by priorities.  The element
            of indice 0 is always the current action.  This list can
            be empty if no action has been set on this object.

        Returns:
            actions (list): the list of actions.

        """
        script = AwareStorage.instance
        if script is None:
            return []

        actions = script.db.actions.get(self.obj, [])
        ret = []
        for action in actions:
            name = action["name"]
            args = action["args"]
            kwargs = action["kwargs"]
            ret.append(Action(name, *args, **kwargs))

        return ret

    def add(self, signal, *args, **kwargs):
        script = AwareStorage.instance
        if script is None:
            return False

        return script.add_action(signal, self.obj, *args, **kwargs)

    def remove(self):
        pass

