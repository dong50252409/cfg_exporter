import logging
import os
import glob
from abc import abstractmethod

from wheezy.template import Engine, FileLoader, CoreExtension, CodeExtension

from cfg_exporter.const import TEMPLATE_EXTENSION


class Export(object):
    def __init__(self, args, base_template_path, extend_template_type_list, global_vars=None):
        self.args = args
        self.output = self.args.output
        self.extend_templates = {}

        template_path = [base_template_path]
        if self.args.template_path is not None:
            for ext in extend_template_type_list:
                for template_file in search_extend_template(self.args.template_path, ext):
                    split = os.path.basename(template_file).split('.')
                    table_name, tmpl_type = split[-3], split[-2]
                    if tmpl_type in self.extend_templates:
                        self.extend_templates[tmpl_type].append(table_name)
                    else:
                        self.extend_templates[tmpl_type] = [table_name]
                    template_path.append(os.path.abspath(os.path.dirname(template_file)))

        logging.debug(f'render engine file loader {[os.path.abspath(file_path) for file_path in template_path]}.')

        self.engine = Engine(
            loader=FileLoader(template_path),
            extensions=[CoreExtension(), CodeExtension()]
        )
        if global_vars is not None:
            self.engine.global_vars.update(global_vars)

    def render(self, filename, template_name, ctx):
        logging.debug(f'render {filename} ...')
        full_filename = os.path.abspath(os.path.join(self.output, filename))
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        with open(full_filename, 'w', encoding='utf-8') as f:
            content = self.engine.get_template(template_name).render(ctx)
            logging.debug(f'render {filename} finished!')
            f.write(content)

    @abstractmethod
    def export(self, table_obj):
        ...


def search_extend_template(source, ext):
    source = os.path.join(source, f'*.{ext}.{TEMPLATE_EXTENSION}')
    return glob.iglob(source)


__all__ = 'Export',

if __name__ == '__main__':
    from wheezy.template import DictLoader

    template = r"""
    @require(l1,l2)
    @return{','.join('%s=%s'% t for t in zip(l1,l2))}
    """
    l1 = range(5)
    l2 = range(5)
    engine = Engine(
        loader=DictLoader({"template": template}),
        extensions=[CoreExtension(), CodeExtension()]
    )
    print(engine.get_template("template").render({"l1": l1, "l2": l2}))
