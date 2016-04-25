
This is an implementation (for Modularity maximization) of the community detection algorithm called "Combo" described in the paper "General optimization technique for high-quality community detection in complex networks" by Stanislav Sobolevsky, Riccardo Campari, Alexander Belyi and Carlo Ratti.
Please, send your feedback, bug reports and questions to:

alexander.belyi@gmail.com

If you use this code, please, cite:
Sobolevsky S., Campari R., Belyi A., and Ratti C. "General optimization technique for high-quality community detection in complex networks" Phys. Rev. E 90, 012811

--------------------------
In order to compile, type:

make

-------------------------
To run the program, type:

./comboCPP path_to_network_file.net [max_number_of_communities]


path_to_network_file - path to the file in Pajek .net format

max_number_of_communities - maximal number of communities to be found (INF by defaul)

Example:
./comboCPP karate.net

-------------------- Output ---------------------------

Program outputs one file named path_to_network_file_comm_comboC++.txt containing numbers of communities for each vertex on separete line.
And it writes achieved modularity score to standart output.