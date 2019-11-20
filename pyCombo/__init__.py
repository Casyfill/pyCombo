__version__ = "0.1.0"
import os
from pathlib import Path
import subprocess
import pandas as pd
import networkx as nx
from typing import Union

comboPath = Path(__file__).parent / "combo" / "comboCPP"


def combo(
    network: nx.Graph,
    max_communities: Union[str, int] = "INF",
    resolution: int = 1,
    output_suffix: str = "tmp",
    clean: bool = True,
):

    nx.write_pajek(network, "./tmp.net")

    subprocess.run(
        args=[str(comboPath), "./tmp.net", max_communities, str(resolution),],
        capture_output=True,
        check=True,
    )

    with open(f"./tmp_comm_comboC++.txt") as f:
        nodes = network.nodes
        comms = f.read().splitlines()
        zone_comm = pd.DataFrame({"zone_id": nodes, "comm_id": comms}, dtype=int)

    if clean:
        try:
            os.remove("./tmp.net")
            os.remove(f"./tmp_comm_comboC++.txt")
        except:
            pass
    return zone_comm
