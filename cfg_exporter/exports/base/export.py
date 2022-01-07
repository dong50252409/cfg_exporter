import glob
import logging
import os
import re
import typing
from abc import abstractmethod

from wheezy.template import Engine, FileLoader, CoreExtension, CodeExtension
from wheezy.template.ext.core import rvalue_token
from wheezy.template.typing import LexerRule

from cfg_exporter.const import TEMPLATE_EXTENSION


class ExpressionExtension:
    def __init__(self):
        self.lexer_rules: typing.Dict[int, LexerRule] = {
            201: (re.compile(r"@`(.*?)`"), rvalue_token)
        }


class BaseExport(object):
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
            extensions=[CoreExtension(), CodeExtension(), ExpressionExtension()]
        )
        if global_vars is not None:
            self.engine.global_vars.update(global_vars)

    def render(self, filename: str, template_name: str, ctx: dict) -> None:
        """
        渲染模板
        """
        filename = f'{self.args.file_prefix}{filename}'
        logging.debug(f'render {filename} ...')
        full_filename = os.path.abspath(os.path.join(self.output, filename))
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        with open(full_filename, 'w', encoding='utf-8') as f:
            content = self.engine.get_template(template_name).render(ctx)
            logging.debug(f'render {filename} finished!')
            f.write(content)

    @abstractmethod
    def export(self, table_obj) -> None:
        """
        需要实现的导出方法
        """
        ...


def search_extend_template(source, ext):
    source = os.path.join(source, f'*.{ext}.{TEMPLATE_EXTENSION}')
    return glob.iglob(source)


__all__ = 'BaseExport',
