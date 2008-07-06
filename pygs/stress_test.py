from stress_utils import get_mem_usage
from structures import *

"""
print get_mem_usage()

g = Graph()
for i in xrange(1000000):
    v = Vertex("bogus")
    del v
    
print get_mem_usage()
"""

def test_state_destroy():
    """State picks up after itself"""
    mperc, m0 = get_mem_usage()

    g = Graph()
    for i in xrange(1000000):
        s = State(0)
        s.destroy()
        
    mperc, m1 = get_mem_usage()
    
    print m0, m1
    assert m1 <= m0+4
    
def test_simple_vertex_destroy():
    """A simple Vertex object picks up after itself"""
    mperc, m0 = get_mem_usage()

    g = Graph()
    for i in xrange(1000000):
        s = Vertex("bogus")
        s.destroy()
        
    mperc, m1 = get_mem_usage()
    
    print m0, m1
    assert m1 <= m0+4
    
def test_street_destroy():
    """Street.destroy() completely destroys Street"""
    mperc, m0 = get_mem_usage()

    for i in xrange(1000000):
        s = Street("bogus", 1.1)
        s.destroy()
        
    mperc, m1 = get_mem_usage()
    
    print m0, m1
    assert m1 <= m0+4
    
def test_link_destroy():
    """Link.destroy() completely destroys Link"""
    mperc, m0 = get_mem_usage()

    for i in xrange(1000000):
        s = Link()
        s.destroy()
        
    mperc, m1 = get_mem_usage()
    
    print m0, m1
    assert m1 <= m0+4

rawhops = [(0,     1*3600,'Foo to Bar'),
            (1*3600,2*3600,'Bar to Cow'),
            (2*3600,3*3600,'four score and seven years'),
            (3*3600,4*3600,'hoombacha')]
cal = CalendarDay(0, 1*3600*24, [1,2], 0)

def test_ths_destroy():
    """TripHopSchedule.destroy() completely destroys TripHopSchedule"""
    mperc, m0 = get_mem_usage()

    for i in xrange(100000):
        s = TripHopSchedule(hops=rawhops, service_id=1, calendar=cal, timezone_offset=0)
        s.destroy()
        
    mperc, m1 = get_mem_usage()
    
    print m0, m1
    assert m1 <= m0+4
    
def test_minimal_graph_delete():
    """Graph.destroy() completely destroys minimal Graph"""
    mperc, m0 = get_mem_usage()

    for i in xrange(1000000):
        s = Graph()
        s.destroy()
        
    mperc, m1 = get_mem_usage()
    
    print m0, m1
    assert m1 <= m0+4
    
def test_min_vertex_graph_delete():
    """Graph.destroy() completely destroys Graph with vertices"""
    mperc, m0 = get_mem_usage()

    for i in xrange(100000):
        s = Graph()
        s.add_vertex("A")
        s.add_vertex("B")
        s.destroy()
        
    mperc, m1 = get_mem_usage()
    
    print m0, m1
    assert m1 <= m0+4
    
def test_min_edge_graph_delete():
    """Graph.destroy() completely destroys Graph with a smattering of edge payloads"""
    mperc, m0 = get_mem_usage()

    for i in xrange(100000):
        s = Graph()
        s.add_vertex("A")
        s.add_vertex("B")
        s.add_vertex("C")
        s.add_edge("A","B",Link())
        s.add_edge("A","B",Street("1",1.1))
        s.add_edge("A","B",Street("2",2.2))
        s.add_edge("A","B",Street("3",3.3))
        s.add_edge("B","A",Link())
        s.add_edge("B","C",TripHopSchedule(hops=rawhops, service_id=1, calendar=cal, timezone_offset=0))
        s.add_edge("B","C",TripHopSchedule(hops=rawhops, service_id=1, calendar=cal, timezone_offset=0))
        s.destroy()
        
    mperc, m1 = get_mem_usage()
    
    print m0, m1
    assert m1 <= m0+4
    
def test_minimal_spt_delete():
    """Graph.destroy_as_spt() completely destroys the spt for a minimal tree"""
    mperc, m0 = get_mem_usage()


    s = Graph()
    s.add_vertex("A")
    s.add_vertex("B")
    s.add_vertex("C")
    s.add_edge("A","B",Street("1", 1.1))
    s.add_edge("B","A",Street("1", 1.1))
    s.add_edge("B","C",Street("2", 2.2))
    
    for i in xrange(100000):
        spt = s.shortest_path_tree("A", "C", State(0))
        spt.destroy_as_spt()
        
    mperc, m1 = get_mem_usage()
    
    print m0, m1
    assert m1 <= m0+4

from random import randint
def random_graph(nvertices, nedges):
    """generates random graph. useful for stress testing"""
    
    vertices = [str(x) for x in range(nvertices)]
    
    g = Graph()
    
    for vertex in vertices:
        g.add_vertex(vertex)
        
    for i in range(nedges):
        a = vertices[ randint( 0, len(vertices)-1 ) ]
        b = a
        while b==a:
            b = vertices[ randint( 0, len(vertices)-1 ) ]
            
        g.add_edge(a,b,Link())
    
    return g
    
if __name__=='__main__':
    test_state_destroy()
    test_simple_vertex_destroy()
    test_street_destroy()
    test_link_destroy()
    test_ths_destroy() #this tends to pass despite not cleaning up the triphop's trip_ids
    test_minimal_graph_delete()
    test_min_vertex_graph_delete()
    test_min_edge_graph_delete()
    test_minimal_spt_delete()