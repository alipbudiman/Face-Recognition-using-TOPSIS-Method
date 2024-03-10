from .mechine_cv2 import OpenCV2
from .mechine_facer import Face_Reco
from .topsis import Spk 
from .my_database import DatabaseManager, LocalDatabaseManager, Database

__copyright__       = 'Copyright 2023 by Alif Budiman Wahabbi'
__version__         = '1.0.0'
__content__         = "SPK (SISTEM PENUNJANG KEPUTUSAN)"
__license__         = 'Private Lisence'
__author__          = 'Alif Budiman Wahabbi'
__author_email__    = 'alifbudimanwahabbi@gmail.com'

__all__ = [
    'OpenCV2',
    'Face_Reco',
    'Spk',
    'DatabaseManager',
    'LocalDatabaseManager',
    'Database',
]