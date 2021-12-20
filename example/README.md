使用方法
=====

Erlang
-----
    python -m cfg_exporter -s example -o example/out/erl --file_prefix cfg_ -t erl -r  --verbose --template_path example/template/erl --field_row 1 --type_row 3 --desc_row 4 --rule_row 5 --data_row 7 --erl_prefix cfg_ --erl_dir cfg --hrl_dir include

JSON
----
    python -m cfg_exporter -s example -o example/out/json --file_prefix cfg_ -t json -r --verbose --field_row 1 --type_row 3 --desc_row 4 --rule_row 5 --data_row 7