import os

from collection_importer import install_collection


collection_path = os.path.dirname(os.path.abspath(__file__))
install_collection(collection_path)
