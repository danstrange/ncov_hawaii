#!/usr/bin/env bash
nextstrain build . --configfile my_profiles/local/builds_2022b.yaml
wait
nextstrain build . --configfile my_profiles/local/builds_2022a.yaml
wait
nextstrain build . --configfile my_profiles/local/builds_2021.yaml
