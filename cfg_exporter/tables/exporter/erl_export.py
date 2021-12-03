from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import DictLoader

template = """\
@require(table_obj)
-module(@table_obj.table_name).
-compile(export_all).

"""


class ErlExport(object):
    def __init__(self):
        self.engine = Engine(
            loader=DictLoader({"erl_template": template}),
            extensions=[CoreExtension()]
        )
        pass

    def export(self, table_obj):
        template = self.engine.get_template("erl_template")
        print(template.render({"table_obj": table_obj}))


if __name__ == '__main__':
    obj = ErlExport()
    obj.export({"name": "item"})
