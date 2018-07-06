# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Comprar
                                 A QGIS plugin
 Comprar
                             -------------------
        begin                : 2018-06-14
        copyright            : (C) 2018 by João Ricardo
        email                : joao_e4@hotmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Comprar class from file Comprar.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .Comprar import Comprar
    return Comprar(iface)
