import numpy as np

#TASK1(a)
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
num_nodes = len(nodes)
edges = [
    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('A', 'H'), ('A', 'I'),
    ('B', 'C'), ('B', 'H'),
    ('C', 'D'), ('C', 'E'),
    ('D', 'G'),
    ('E', 'F'),
    ('F', 'G'), ('F', 'H'),
    ('G', 'H'),
    ('H', 'I')
]

A = np.zeros((num_nodes, num_nodes), dtype=int)
for u, v in edges:
    i, j = nodes.index(u), nodes.index(v)
    A[i, j] = 1
    A[j, i] = 1  

degrees = np.sum(A, axis=1)
D = np.diag(degrees)

print("Adjacency Matrix (A):")
print(A)
print("\nDegree Matrix (D):")
print(D)

#TASK1(c)
L = D - A
eigenvalues, eigenvectors = np.linalg.eigh(L)

eigenvalues_clean = np.round(eigenvalues, 4)
eigenvectors_clean = np.round(eigenvectors, 4)

print("--- Task 1(c) Output ---")
print("\nLaplacian Matrix (L):")
print(L)

print("\nEigenvalues (Sorted):")
print(eigenvalues_clean)

print("\nEigenvectors (Each column corresponds to the sorted eigenvalues):")
print(eigenvectors_clean)