def undirected_edge_name(u, v) -> str:
    """
    :return The name of an undirected edge as "(u,v)" with u <= v.
    """
    u_i, v_i = int(u), int(v)
    if u_i > v_i:
        u_i, v_i = v_i, u_i
    return f"({u_i},{v_i})"
