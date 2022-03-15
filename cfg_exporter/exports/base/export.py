import glob
import logging
import os
import re
import traceback
import typing
from abc import ABC, abstractmethod

from wheezy.template import Engine, FileLoader, CoreExtension, CodeExtension
from wheezy.template.ext.core import rvalue_token

import cfg_exporter.util as util
from cfg_exporter.const import TEMPLATE_EXTENSION
from cfg_exporter.lang_template import load


class ExpressionExtension:
    def __init__(self):
        self.lexer_rules = {
            201: (re.compile(r"@`(.*?)`"), rvalue_token)
        }


class BaseExport(ABC):

    def __init__(self, args, base_template_path, extend_template_type_list, global_vars=None):
        self.args = args
        self.output = self.args.output

        if self.args.lang_template is not None:
            load(self.args.lang_template)

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

        if global_vars is None:
            global_vars = {}
        global_vars.update({'util': util})
        self.engine.global_vars.update(global_vars)

    def render(self, filename: str, template_name: str, ctx: dict) -> typing.NoReturn:
        """
        渲染模板
        """
        filename = f'{self.args.file_prefix}{filename}'
        full_filename = os.path.abspath(os.path.join(self.output, filename))
        if not os.path.exists(self.output):
            os.makedirs(self.output)
        with open(full_filename, 'w', encoding='utf-8') as f:
            try:
                content = self.engine.get_template(template_name).render(ctx)
                f.write(f'{self.file_desc()}{content}')
            except:
                logging.error(traceback.print_exc())

    @abstractmethod
    def file_desc(self) -> str:
        """
        文件顶部描述
        """
        return ""

    @abstractmethod
    def export(self, table_obj) -> typing.NoReturn:
        """
        导出方法
        """
        ...

    @staticmethod
    def naming_convention():
        """
        名目约定
        """
        return lambda s: s


def search_extend_template(source, ext):
    source = os.path.join(source, f'*.{ext}.{TEMPLATE_EXTENSION}')
    return glob.iglob(source)


__all__ = ('BaseExport',)
