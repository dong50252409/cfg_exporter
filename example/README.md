使用方法
=====

Erlang
-----

    python -m cfg_exporter -s example/tables -o example/out/erl --file_prefix cfg_ -e erl -r  --verbose --template_path example/template/erl --field_row 1 --type_row 2 --desc_row 3 --rule_row 4 --data_row 6 --erl_prefix cfg_ --erl_dir cfg --hrl_dir include

Lua
----

    python -m cfg_exporter -s example/tables -o example/out/lua --file_prefix cfg_ -e lua -r --verbose --template_path example/template/lua  --field_row 1 --type_row 2 --desc_row 3 --rule_row 4 --data_row 6

JSON
----

    python -m cfg_exporter -s example/tables -o example/out/json --file_prefix cfg_ -e json -r --verbose --field_row 1 --type_row 2 --desc_row 3 --rule_row 4 --data_row 6

CSV
----

    python -m cfg_exporter -s example/tables -o example/out/csv --file_prefix cfg_ -e csv -r --verbose --field_row 1 --type_row 2 --desc_row 3 --rule_row 4 --data_row 6

XLSX
----

    python -m cfg_exporter -s example/tables -o example/out/xlsx --file_prefix cfg_ -e csv -r --verbose --field_row 1 --type_row 2 --desc_row 3 --rule_row 4 --data_row 6