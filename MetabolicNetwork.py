# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class MetabolicNetwork (MyGraph):
    
    def __init__(self, network_type = "metabolite-reaction", split_rev = False):
        MyGraph.__init__(self, {})
        self.net_type = network_type
        self.node_types = {}
        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = []
            self.node_types["reaction"] = []
        self.split_rev =  split_rev

    def add_vertex_type(self, v, nodetype):
        self.add_vertex(v)
        self.node_types[nodetype].append(v)
    
    def get_nodes_type(self, node_type):
        if node_type in self.node_types:
            return self.node_types[node_type]
        else: return None
    
    def load_from_file(self, filename):
        rf = open(filename)
        gmr = MetabolicNetwork("metabolite-reaction")
        for line in rf:
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
            else: raise Exception("Invalid line:")                
            if "<=>" in rline:
                left, right = rline.split("<=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id+"_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id+"_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id+"_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
            elif "=>" in line:
                left, right = rline.split("=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
            else: raise Exception("Invalid line:")    

        
        if self.net_type == "metabolite-reaction": 
            self.graph = gmr.graph
            self.node_types = gmr.node_types
        elif self.net_type == "metabolite-metabolite":
            self.convert_metabolite_net(gmr, "metabolite")
        elif self.net_type == "reaction-reaction": 
            self.convert_metabolite_net(gmr, "reaction")
        else: self.graph = {}
        
        
    def convert_metabolite_net(self, gmr, tipo):
        '''
        Cria rede de metabolitos e reações
        '''
        for metabolite in gmr.node_types[tipo]: #Obtém todos os metabolitos
            self.add_vertex(metabolite) #Adiciona o metabolito á rede
            successors = gmr.get_successors(metabolite) #Obtém as reações de cada metabolito, Exemplo: M1 -> R1
            for succ in successors:
                last_metabolite = gmr.get_successors(succ)  #Obtém os metabolitos de cada reação, Exemplo: R2 -> M3
                for reaction_to_metabolite in last_metabolite: #Obtém o metabolito resultante da reação
                    if metabolite != reaction_to_metabolite: # Se o metabolito for diferente do metabolito da reação, adiciona a ligação
                        self.add_edge(metabolite, reaction_to_metabolite)

    def active_reactions(self, substrates: list):
        """
        Determina todas as reações ativas dado uma lista de metabolitos
        """
        active_reactions = [] #Criamos a lista "active_reactions" para adicionar as reações ativas
        for reaction in self.node_types["reaction"]: #Obtém todas as reações
            predecessors = self.get_predecessors(reaction) #Obtém os metabolitos predecessores  das reações
            if all(metabolite in predecessors for metabolite in substrates): #Se todos os metabolitos resultantes estiverem na lista de metabolitos 'substrates':
                active_reactions.append(reaction) #Adicionamos essa reação á nossa lista 'active_reactions'
        return active_reactions

    def produced_metabolites(self, active_reactions: list):
        """
        Determina os metabolitos que podem ser produzidos dada uma lista de reações ativas
        """
        produced_metabolites = [] #Criamos a lista "produced_metabolites" para adicionar os metabolitos
        for reactions in active_reactions: #Percorremos a lista de reações ativas
            produced_metabolites.extend(self.graph[reactions]) #Adicionamos as reações á lista que criamos
        return set(produced_metabolites)  #Eliminar os metabolitos repetidos

    def final_metabolites(self, initial_metabolites: list):
        """
        Determina todos os metabolitos finais que poderão ser produzidos dada uma lista de metabolitos iniciais
        """
        final_metabolites = []
        metabolites = initial_metabolites
        while True: # Foi criado um ciclo infinito para adicionar os metabolitos produzidos aos metabolitos finais
            active_reactions = self.active_reactions(initial_metabolites)
            produced_metabolites = self.produced_metabolites(active_reactions)
            if not all(produced_metabolites) in final_metabolites:
                for metabolite in produced_metabolites:
                    if metabolite not in final_metabolites:
                        final_metabolites.append(metabolite)
                        metabolites.extend(final_metabolites)  #
            else:
                break
        print("Metabolitos finais:\n")
        print(final_metabolites)
        return final_metabolites


def test1():
    m = MetabolicNetwork("metabolite-reaction")
    m.add_vertex_type("R1","reaction")
    m.add_vertex_type("R2","reaction")
    m.add_vertex_type("R3","reaction")
    m.add_vertex_type("M1","metabolite")
    m.add_vertex_type("M2","metabolite")
    m.add_vertex_type("M3","metabolite")
    m.add_vertex_type("M4","metabolite")
    m.add_vertex_type("M5","metabolite")
    m.add_vertex_type("M6","metabolite")
    m.add_edge("M1","R1")
    m.add_edge("M2","R1")
    m.add_edge("R1","M3")
    m.add_edge("R1","M4")
    m.add_edge("M4","R2")
    m.add_edge("M6","R2")
    m.add_edge("R2","M3")
    m.add_edge("M4","R3")
    m.add_edge("M5","R3")
    m.add_edge("R3","M6")
    m.add_edge("R3","M4")
    m.add_edge("R3","M5")
    m.add_edge("M6","R3")
    m.print_graph()
    print("Reactions: ", m.get_nodes_type("reaction") )
    print("Metabolites: ", m.get_nodes_type("metabolite") )

        
def test2():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("example-net.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction") )
    print("Metabolites: ", mrn.get_nodes_type("metabolite") )
    print()
    
    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("redeMetabolitos.txt")
    mmn.print_graph()
    print("Metabolites: ", mrn.get_nodes_type("metabolite"))
    print("Metabolites: ", mrn.get_nodes_type("metabolite"))
    print()
    
    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("example-net.txt")
    rrn.print_graph()
    print()
    
    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("example-net.txt")
    mrsn.print_graph()
    print()
    
    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("example-net.txt")
    rrsn.print_graph()
    print()

def teste_ecoli():
    graph = MetabolicNetwork("metabolite-reaction")
    graph.load_from_file("ecoli.txt")
    print(f"Média de graus:", graph.mean_degree())
    print(graph.prob_degree())
    print("MeanGraphInicio")
    #Entra em loop "infinito" print(graph.mean_distances())
    print("MeanGraphFim")
    print("graph")
    print(graph.print_graph())
    graph.final_metabolites(graph.node_types)

test1()
print("#############################################")
test2()
print("#############################################")
teste_ecoli()

