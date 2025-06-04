import numpy as np

def patch_numpy():
    """Ensure deprecated numpy aliases exist for packages that still require them."""
    if not hasattr(np, 'bool'):
        np.bool = np.bool_
    if not hasattr(np, 'object'):
        np.object = np.object_
    if not hasattr(np, 'int'):
        np.int = np.int_
    if not hasattr(np, 'float'):
        np.float = np.float_
    if not hasattr(np, 'complex'):
        np.complex = np.complex_
    if not hasattr(np, 'bool8'):
        np.bool8 = np.bool_
    if not hasattr(np, 'product'):
        np.product = np.prod
