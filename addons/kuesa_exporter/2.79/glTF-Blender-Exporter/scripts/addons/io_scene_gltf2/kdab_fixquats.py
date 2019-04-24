# (C) 2018 KDAB
#
# This tries to ensure animated quaternions stay continuous.
# If we animate continuous rotations and these are converted to quaternions there can be
# overruns which result in saw tooth animation curves. When those later are
# interpolated in the engine this results in hick-ups.
# This tries which quaternion fits best to the previous one, q or -q,
# which both is the same rotation wise.


import mathutils


class FixQuat (object):

    SEPARATOR = ".."

    id = None
    last = None

    @staticmethod
    def generateId(node_name, action_name):
        return "{}{}{}".format(node_name, FixQuat.SEPARATOR, action_name)

    def __init__(self, node_name, action_name):
        self.id = FixQuat.generateId(node_name, action_name)
        self.last = None

    def __repr__(self):
        return "{} {{{}}}".format(self.__class__.__name__, self.id)

    def __call__(self, quat):
        r = quat.copy()
        if self.last is not None:
            d  = self.last - quat
            d_ = self.last + quat
            if d.magnitude > d_.magnitude:
                r = -r
        self.last = r
        #print("{}: {} -> {}".format(str(self), quat, r))
        return r


class FixQuats (object):

    fixquats = None

    @staticmethod
    def reset():
        #print("{} RESET".format("FixQuat"))
        FixQuats.fixquats = {}

    @staticmethod
    def debug():
        r = "{} {{".format("FixQuats")
        for k in FixQuats.fixquats:
            r += "\n    {}".format(str(FixQuats.fixquats[k]))
        r += "\n}"
        print(r)

    @staticmethod
    def get(node_name, action_name):
        id = FixQuat.generateId(node_name, action_name)
        if id in FixQuats.fixquats:
            return FixQuats.fixquats[id]
        q = FixQuat(node_name, action_name)
        FixQuats.fixquats[id] = q
        return q

    @staticmethod
    def len():
        return len(FixQuats.fixquats)
