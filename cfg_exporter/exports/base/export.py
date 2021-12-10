import os
from abc import abstractmethod

from wheezy.template import Engine, FileLoader, CoreExtension, CodeExtension


class Export(object):
    def __init__(self, table_obj, args, template_path_list, global_vars=None):
        self.table_obj = table_obj
        self.args = args
        self.engine = Engine(
            loader=FileLoader(template_path_list),
            extensions=[CoreExtension(), CodeExtension()]
        )
        if global_vars is not None:
            self.engine.global_vars.update(global_vars)
        pass

    @abstractmethod
    def export(self):
        ...

    def render(self, path, filename, template_name, ctx):
        full_filename = os.path.join(path, filename)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(full_filename, 'w', encoding='utf-8') as f:
            content = self.engine.get_template(template_name).render(ctx)
            f.write(content)


if __name__ == '__main__':
    from wheezy.template import Engine, DictLoader, CoreExtension, CodeExtension

    template = r"""
    @require(l1,l2)
    @{','.join('{}=\{}'.format(*t) for t in zip(l1,l2))}
    """
    l1 = range(5)
    l2 = range(5)
    engine = Engine(
        loader=DictLoader({"template": template}),
        extensions=[CoreExtension(), CodeExtension()]
    )
    print(engine.get_template("template").render({"l1": l1, "l2": l2}))
