from typing import Collection

import numpy as np
from scipy.cluster import hierarchy


def _get_newick(node, parent_dist, leaf_names, newick='') -> str:
    if node.is_leaf():
        return "%s:%.2f%s" % (leaf_names[node.id], parent_dist - node.dist, newick)
    else:
        if len(newick) > 0:
            newick = "):%.2f%s" % (parent_dist - node.dist, newick)
        else:
            newick = ");"
        newick = _get_newick(node.get_left(), node.dist, leaf_names, newick=newick)
        newick = _get_newick(node.get_right(), node.dist, leaf_names, newick=",%s" % newick)
        newick = "(%s" % newick
        return newick


def dm_to_newick(arr: np.ndarray, labels: Collection[str]) -> str:
    """Convert a pairwise distance matrix into Newick format.

    Args:
        arr: The symmetrical pairwise distance matrix.
        labels: The labels of the leaf nodes.
    """
    Z = hierarchy.linkage(arr)
    tree = hierarchy.to_tree(Z, rd=False)
    newick = _get_newick(tree, tree.dist, labels)
    return newick
