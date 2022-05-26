# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class MetabolicNetwork (MyGraph):
    '''
    Classe que representa as redes metabólicas
    '''
    
    def __init__(self, network_type = "metabolite-reaction", split_rev = False):
        '''
        Armazena as variáveis globais da classe
        Inputs:
            :network_type: Tipo de rede metabólica
            :split_rev: Se a reação for reversível retorna true
        '''
        MyGraph.__init__(self, {})
        self.net_type = network_type
        self.node_types = {}
        if network_type == "metabolite-reaction":
            self.node_types["metabolite"] = []
            self.node_types["reaction"] = []
        self.split_rev =  split_rev

    def add_vertex_type(self, v, nodetype):
        '''
        Adiciona nós
        Inputs:
            :v: Nó que é adionado á nossa rede metabólica
            :param nodetype: O tipo de nó que é adicionado que neste caso ou é (reaction) ou (metabolite)
        '''
        self.add_vertex(v)
        self.node_types[nodetype].append(v)
    
    def get_nodes_type(self, node_type):
        '''
        Obtemos os tipos de nós
        Inputs:
            :node_type: Tipo de nó
        Returns: Devolve os nós do tipo que escolhemos
        '''
        if node_type in self.node_types:
            return self.node_types[node_type]
        else: return None
    
    def load_from_file(self, filename):
        '''
        Esta função cria uma rede metabólica ”metabolite-reaction” (grafo bipartido),através do ficheiro que
        disponibilizamos, em que cada reação é definida numa linha
        Inputs:
            :filename: Nome do Ficheiro
        '''
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
            self.convert_metabolite_network(gmr, "metabolite")
        elif self.net_type == "reaction-reaction": 
            self.convert_metabolite_network(gmr, "reaction")
        else: self.graph = {}
        
        
    def convert_metabolite_network(self, gmr, tipo):
        '''
        Converte a rede metabólica (metabolite-reaction) para (metabolite-metabolite) ou (reaction-reaction)
        Inputs:
            gmr: Rede Metabólica
            tipo: O tipo de nó é reaction ou metabolite
        '''
        for tipo_de_no in gmr.node_types[tipo]: #Obtém todos os metabolitos ou reações
            self.add_vertex(tipo_de_no) #Adiciona o metabolito ou reação á rede
            successors = gmr.get_successors(tipo_de_no) #Se o tipo de nó for (metabolite) obtém as reações de cada metabolito, Exemplo: M1 -> R1
            for s in successors:
                succesors_tipo_de_no = gmr.get_successors(succ)  #Obtém os metabolitos de cada reação, Exemplo: R2 -> M3
                for s2 in succesors_tipo_de_no: #Obtém o metabolito resultante da reação
                    if tipo_de_no != s2: # Se o metabolito for diferente do metabolito da reação:
                        self.add_edge(tipo_de_no, s2) #Adiciona a ligação

    def active_reactions(self, substrates):
        """
        Determina todas as reações ativas dado uma lista de metabolitos
        Inputs:
            :substrates: Lista de metabolitos existentes
        Returns:
            :return list: Lista com as reações ativas
            :rtype list: list
        """
        active_reactions = [] #Criamos a lista "active_reactions" para adicionar as reações ativas
        if self.net_type != "metabolite-reaction" or not self.split_rev: #Se o tipo da rede metabólica for diferente de (metabolite-reaction)
            return None #Retorna "vazio"
        for reaction in self.node_types["reaction"]: #Obtém todas as reações
            predecessors = self.get_predecessors(reaction) #Obtém os metabolitos predecessores  das reações
            if all(metabolite in predecessors for metabolite in substrates): #Se todos os metabolitos resultantes estiverem na lista de metabolitos 'substrates':
                active_reactions.append(reaction) #Adicionamos essa reação á nossa lista 'active_reactions'
        return active_reactions

    def produced_metabolites(self, active_reactions):
        """
        Determina os metabolitos que podem ser produzidos dada uma lista de reações ativas
        Inputs:
            :active_reactions: Lista de Reações Ativas
        Returns:
            :return list: Lista com os metabolitos produzidos
            :rtype list: list
        """
        produced_metabolites = [] #Criamos a lista "produced_metabolites" para adicionar os metabolitos
        for reaction in active_reactions: #Percorremos a lista de reações ativas
            succesors = self.get_successors(reaction) #Obtém os metabolitos de cada reação ativa
            for s in succesors:
                produced_metabolites.append(s) #Adiciona o metabolito á lista
        return set(produced_metabolites)

    def final_metabolites(self, initial_metabolites: list):
        """
        Determina todos os metabolitos finais que poderão ser produzidos dada uma lista de metabolitos iniciais
        Inputs:
            initial_metabolites: Lista de Metabolitos Iniciais
        Outputs:
            final_metabolites: Devolve a lista dos metabolitos finais
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

