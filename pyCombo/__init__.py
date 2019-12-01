__version__ = "0.1.0"
from .Graph import Graph
from .Main import runCombo

__all__ = ["runCombo", "Graph"]

# import os
# from pathlib import Path
# import subprocess
# import pandas as pd
# import networkx as nx
# from typing import Union

# comboPath = Path(__file__).parent / "combo" / "comboCPP"


# def _run_combo(
#     path,
#     max_communities: Union[str, int] = "INF",
#     resolution: int = 1,
#     output_suffix: str = "tmp",
# ):

#     subprocess.run(
#         args=[str(comboPath), path], capture_output=True, check=True,
#     )


# def combo(
#     network: nx.Graph,
#     max_communities: Union[str, int] = "INF",
#     resolution: int = 1,
#     output_suffix: str = "tmp",
#     clean: bool = True,
# ):
#     temp_path = "./tmp.net"
#     nx.write_pajek(network, temp_path)
#     _run_combo(temp_path)

#     with open(temp_path.replace(".net", "comm_comboC++.txt")) as f:
#         nodes = network.nodes
#         comms = f.read().splitlines()
#         zone_comm = pd.DataFrame({"zone_id": nodes, "comm_id": comms}, dtype=int)

#     if clean:
#         try:
#             os.remove("./tmp.net")
#             os.remove(f"./tmp_comm_comboC++.txt")
#         except:
#             pass
#     return zone_comm
