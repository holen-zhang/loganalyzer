import os
from jpype import *


def close_jvm():
    shutdownJVM()


class Gumtree:
    gumtree = None
    GUMTREE_HOME = "/Users/sense/Degree/GumTreeDiff/gumtree/dist/build/distributions/gumtree-2.1.3-SNAPSHOT/lib/"

    def __init__(self, class_name='com.sense.gumtreeapi.GumTreeApi'):
        gumtree_jar = f'{str.join(":", [Gumtree.GUMTREE_HOME + name for name in os.listdir(Gumtree.GUMTREE_HOME)])}'
        java_class_path = ".:/Users/sense/eclipse-workspace/GumTreeApi/bin:" + gumtree_jar
        if Gumtree.gumtree is None:
            # class path
            jvm_arg = "-Djava.class.path=" + java_class_path
            startJVM(getDefaultJVMPath(), '-d64', jvm_arg)
            # initial class and object
            gumtree_api = JClass(class_name)
            Gumtree.gumtree = gumtree_api()

    def get_gumtree_json_diff_actions(self):
        json_diff_list = Gumtree.gumtree.getJsonDiffActions()
        return json_diff_list


gumtree = Gumtree()
# print(gumtree.get_gumtree_json_diff_actions())
