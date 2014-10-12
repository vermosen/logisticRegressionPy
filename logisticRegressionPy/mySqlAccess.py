####################################
#                                  #
# This class has been designed to  #
# download data from yahoo finance #
#                                  #
####################################

import logging
from dateutil import parser
import pandas as pd
from datetime import datetime
from matplotlib import finance as fi

class mySqlAccess(object):
    
    description = "this class is used to load data from a mysql database"
    author = "Jean-Mathieu Vermosen"

    # empty ctor
    def __init__(self, debug=False):

        return
 
    