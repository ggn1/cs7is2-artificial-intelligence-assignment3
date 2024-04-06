In order to train a Q learning agent 
for either Tic Tac Toe or Connect 4.

In order to train a Q learning model, the following command can be run
with custom parameters. Please view argument definitions in 
file q_learning.py within the parse_cms_args() function.
> python q_learning.py --game-type ttt --logs-folder ./__logs --csv-filename q_learning --max-episodes 1e20 --gamma 0.99 --alpha 0.9 --max-minutes 6 --save-folder ./__q_tables