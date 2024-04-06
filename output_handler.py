import os
import json

class OutputHandler:
    """
    Defines a class that manages output generation and
    formatting.
    """

    def __init__(self, logs_folder:str, csv_folder:str):
        """
        Constructor.
        @param logs_folder: Path to location where logs are
                           to be saved.
        @param csv_folder: Path to location where the csv
                           containing run data shall be 
                           present.
        """
        self.folders = {'logs': logs_folder, 'csv': csv_folder}
        for dst in self.folders.values():
            if not os.path.exists(dst):
                os.makedirs(dst)

    def print_start_status(self, 
        world_type:str, 
        session_id:str, 
        game_num:int=None
    ):
        """ 
        Prints a status message. 
        """
        out_str = "\nPlaying " 
        out_str += "Game: " if game_num else "Session: "
        out_str += f"World '{world_type}', "
        out_str += f"Session '{session_id}'"
        if game_num is not None:
            out_str += f", Game '{game_num}'"
        out_str += ")"
        print(out_str)

    def print_metrics(self, 
        world_type:str, 
        session_id:str, 
        metrics:dict,
        game_num:int=None,
    ):
        """ 
        Prints a run metrics. 
        """
        out_str = "\nMetrics (" 
        out_str += f"World '{world_type}', "
        out_str += f"Session '{session_id}'"
        if game_num is not None:
            out_str += f", Game '{game_num}'"
        out_str += "): "
        out_str += json.dumps(metrics, indent=4)
        print(out_str)

    def print_out(self,
        out_str:str, 
    ):
        """ 
        Prints any generic message starting
        with a new line.
        """
        print(f"\n{out_str}")
        
    def log_start_status(self, 
        world_type:str, 
        session_id:str, 
        session_timestamp:str,
        game_num:int=None,
        filename:str=None
    ):
        """ 
        Logs a run outcome. 
        """
        if filename is None:
            filename = f"{world_type}_{session_id}_{session_timestamp}" 
        out_str = "\nPlaying " 
        out_str += "Game: " if game_num else "Session: "
        out_str += f"World '{world_type}', "
        out_str += f"Session '{session_id}'"
        if game_num is not None:
            out_str += f", Game '{game_num}'"
        out_str += ")"
        self.append_to_logs(filename, out_str)

    def log_metrics(self, 
        world_type:str, 
        session_id:str, 
        metrics:dict,
        session_timestamp:str,
        game_num:int=None
    ):
        """ 
        Logs a run metrics to a file called
        "{world_type}_{session_id}_{session_timestamp}" in the 
        configured folder.
        """
        filename = f"{world_type}_{session_id}_{session_timestamp}" 
        out_str = "\nMetrics (" 
        out_str += f"World '{world_type}', "
        out_str += f"Session '{session_id}'"
        if game_num is not None:
            out_str += f", Game '{game_num}'"
        out_str += "): "
        out_str += json.dumps(metrics, indent=4)
        self.append_to_logs(filename, out_str)

    def log_world_state(self, 
        world_type:str, 
        session_id:str,
        session_timestamp:str,
        world_str:str
    ):
        """ 
        Adds given world state string
        to a log file called
        "{world_type}_{session_id}_{session_timestamp}"  
        in the configured folder.
        """
        filename = f"{world_type}_{session_id}_{session_timestamp}" 
        world_str = "\n" + world_str
        self.append_to_logs(filename=filename, out_str=world_str)
        
    def append_to_logs(self, filename:str, out_str:str):
        """
        Adds any string to the log file 
        with an added new line at the start.
        """
        dst = f"{self.folders['logs']}/{filename}.log"
        with open(dst, 'a') as f:
            f.write("\n"+out_str)

    def append_to_csv(self, 
        world_type:str, player1:str, player2:str, outcome:int,
        avg_seconds_per_move_player1:float, 
        avg_seconds_per_move_player2:float,
        num_moves:int, session_id:str, session_timestamp:str, 
        game_num:int, moves_visited:int=None, filename:str=None
    ):
        """
        Saves metrics into a file.
        """
        if filename is None:
            filename = world_type
        
        dst = f"{self.folders['csv']}/{filename}.csv"
        if not os.path.exists(dst):
            with open(dst, 'w') as f:
                f.write(
                    "world_type,player1,player2,outcome,"
                    + "avg_seconds_per_move_player1,"
                    + "avg_seconds_per_move_player2,"
                    + "num_moves,session_id,session_timestamp,"
                    + "game_num,moves_visited\n"
                )
        to_save = (
            f"{world_type},{player1},{player2},{outcome},"
            + f"{avg_seconds_per_move_player1},"
            + f"{avg_seconds_per_move_player2},"
            + f"{num_moves},{session_id},"
            + f"{session_timestamp},{game_num},"
        )
        if moves_visited is not None:
            to_save += f"{moves_visited}"
        to_save += "\n"

        with open(dst, "a") as f:
            f.write(to_save)