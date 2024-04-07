In order to train a Q learning agent 
for either Tic Tac Toe or Connect 4.

In order to train a Q learning model, the following command can be run
with custom parameters. Please view argument definitions in 
file q_learning.py within the parse_cms_args() function.
> python q_learning.py --game-type ttt --logs-folder ./__logs --csv-filename q_learning --max-episodes 1e20 --gamma 0.99 --alpha 0.9 --max-minutes 6 --save-folder ./__q_tables

All experiments that were conducted as part of this assignment can be 
run using the following commands.
> python exp1.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./__q_tables/07042024034202ttt0.9alpha0.99gamma787736episodes4mins.json
> python exp2.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./__q_tables/07042024042415con40.9alpha0.99gamma195419episodes30mins.json
> python exp3.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./__q_tables/07042024034202ttt0.9alpha0.99gamma787736episodes4mins.json
> python exp4.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./__q_tables/07042024042415con40.9alpha0.99gamma195419episodes30mins.json
> python exp5.py --logs-folder ./__logs --logs-filename exp5_minimax_con4_30mins
> python exp6.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./__q_tables/07042024042415con40.9alpha0.99gamma195419episodes30mins.json
> python exp7.py --logs-folder ./__logs --csv-folder ./__run_results
> python exp8.py --logs-folder ./__logs --csv-folder ./__run_results