# k_nn_gui.py
import io
import base64

import flet as ft
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder