In order to train a Q learning model for either game, 
the following command can be run with custom parameters. 
Please view argument definitions in file q_learning.py 
within the parse_cms_args() function.

To train a Q Learning agent on the Tic Tac Toe game from scratch:
> python q_learning.py --game-type ttt --logs-folder ./__logs --csv-filename q_learning --max-episodes 1e20 --gamma 0.99 --alpha 0.9 --max-minutes 6 --save-folder ./q_tables

To train a Q Learning agent on the Connect 4 game from scratch:
> python q_learning.py --game-type con4 --logs-folder ./__logs --csv-filename q_learning --max-episodes 1e20 --gamma 0.99 --alpha 0.9 --max-minutes 30 --save-folder ./q_tables

To train a Q Learning agent on the Connect 4 game starting from a pre-saved Q table:
> python q_learning.py --game-type con4 --logs-folder ./__test --csv-filename q_learning --max-episodes 1e20 --gamma 0.99 --alpha 0.9 --max-minutes 30 --save-folder ./q_tables --load-path ./q_tables/07042024145514con40.9alpha0.99gamma107264episodes15mins.json

All experiments that were conducted as part of this assignment can be 
run using the following commands.

To run experiment 1:
> python exp1.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./q_tables/07042024034202ttt0.9alpha0.99gamma787736episodes4mins.json

To run experiment 2:
> python exp2.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./q_tables/07042024151222con40.9alpha0.99gamma87319episodes30mins.json

To run experiment 3:
> python exp3.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./q_tables/07042024034202ttt0.9alpha0.99gamma787736episodes4mins.json

To run experiment 4:
> python exp4.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./q_tables/07042024151222con40.9alpha0.99gamma87319episodes30mins.json

To run experiment 5: [please stop this manually through keyboard interrupt]
> python exp5.py --logs-folder ./__logs --logs-filename exp5_minimax_con4_30mins

To run experiment 6:
> python exp6.py --logs-folder ./__logs --csv-folder ./__run_results --q-table ./q_tables/07042024151222con40.9alpha0.99gamma87319episodes30mins.json

To run experiment 7:
> python exp7.py --logs-folder ./__logs --csv-folder ./__run_results

To run experiment 8:
> python exp8.py --logs-folder ./__logs --csv-folder ./__run_results