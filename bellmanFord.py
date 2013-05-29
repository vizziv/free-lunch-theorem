class Vertex:
    def __init__(self):
        self.distance = float("inf")
    __hash__ = object.__hash__

class Edge:
    def __init__(self, tail, head, weight):
        self.tail = tail
        self.head = head
        self.weight = weight

def verts(edges):
    return set(vert for e in edges for vert in (e.tail, e.head))

# Returns True if graph has a negative cycle or isn't strongly connected.
def bellmanFord(edges):
    # For us, the start vertex is arbitrary.
    edges[0].tail.distance = 0
    # Find minimum length from the start vertex to each other vertex.
    for i in range(len(verts(edges)) - 1):
        for e in edges:
            newDistance = e.tail.distance + e.weight
            if newDistance < e.head.distance:
                e.head.distance = newDistance
    # Find triangle inequality failures, which are caused by negative cycles.
    # Also detect disconnectedness to confirm we've searched the whole graph.
    for e in edges:
        if e.tail.distance + e.weight < e.head.distance:
            return True
    return False

# Throughout, we use 0 instead of -1 for s_i(p), correcting for it when needed.

# Checks if mu_i(p,q) is compatible with the definition of a sector.
def validVert(mu1):
    (p0, p1, s1, s2, q0, q1, t1, t2) = mu1
    return (p0==s1 if p0==p1 else s1==s2) and (q0==t1 if q0==q1 else t1==t2)

# Checks if u can be followed by v.
def validEdge(mu1, mu2):
    (p0a, p1a, s1a, s2a, q0a, q1a, t1a, t2a) = mu1
    (p1b, p2b, s2b, s3b, q1b, q2b, t2b, t3b) = mu2
    return p1a==p1b and q1a==q1b and s2a==s2b and t2a==t2b

# Calculates M_{i}(p,q)
def weight(mu1):
    (p0, p1, s1, s2, q0, q1, t1, t2) = mu1
    return (2*s1-1)*(p1-q0) + (2*t1-1)*(q1-p0) - abs(s1-s2) - abs(t1-t2)

bits = {x : tuple((x // 2**i) % 2 for i in range(8)) for x in range(2**8)}
vs = {bits[i]: Vertex() for i in range(2**8) if validVert(bits[i])}
G = [Edge(vs[u], vs[v], weight(u)) for u in vs for v in vs if validEdge(u, v)]

# And Theorem 5.1 is...
print(not bellmanFord(G))
