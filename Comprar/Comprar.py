# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Comprar
                                 A QGIS plugin
 Comprar
                              -------------------
        begin                : 2018-06-14
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João Ricardo
        email                : joao_e4@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from datetime import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Comprar_dialog import ComprarDialog
import os.path
import processing

class Comprar:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgisInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Comprar_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ComprarDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Comprar')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Comprar')
        self.toolbar.setObjectName(u'Comprar')

        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_input_file)

        self.dlg.lineEdit_2.clear()
        self.dlg.pushButton_2.clicked.connect(self.select_input_file_2)

        self.dlg.lineEdit_3.clear()
        self.dlg.pushButton_3.clicked.connect(self.select_input_file_3)

        self.dlg.lineEdit_4.clear()
        self.dlg.pushButton_4.clicked.connect(self.select_input_file_4)

        self.dlg.lineEdit_7.clear()
        self.dlg.pushButton_6.clicked.connect(self.select_output_file)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Comprar', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Comprar/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Comprar'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Comprar'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_input_file(self):
        openfile = QFileDialog.getOpenFileName(self.dlg, "Open:","", '*.shp')
        self.dlg.lineEdit.setText(openfile)

    def select_input_file_2(self):
        openfile_2 = QFileDialog.getOpenFileName(self.dlg, "Open:","", '*.shp')
        self.dlg.lineEdit_2.setText(openfile_2)

    def select_input_file_3(self):
        openfile_3 = QFileDialog.getOpenFileName(self.dlg, "Open:","", '*.shp')
        self.dlg.lineEdit_3.setText(openfile_3)

    def select_input_file_4(self):
        openfile_4 = QFileDialog.getOpenFileName(self.dlg, "Open:","", '*.shp')
        self.dlg.lineEdit_4.setText(openfile_4)

    def select_output_file(self):
        foldername = QFileDialog.getExistingDirectory(self.dlg, "Folder:","",QFileDialog.ShowDirsOnly)
        self.dlg.lineEdit_7.setText(foldername)

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            bairro = self.dlg.lineEdit.text()
            local_1 = self.dlg.lineEdit_2.text()
            local_2 = self.dlg.lineEdit_3.text()
            local_3 = self.dlg.lineEdit_4.text()
            saida = self.dlg.lineEdit_7.text()

            bairro_selecionado = self.dlg.lineEdit_5.text()

            dist_1 = self.dlg.spinBox.value()
            dist_2 = self.dlg.spinBox_2.value()
            dist_3 = self.dlg.spinBox_3.value()

            buffer_1 = saida +'/'+"buffer_1.shp"
            buffer_2 = saida +'/'+"buffer_2.shp"
            buffer_3 = saida +'/'+"buffer_3.shp"

            inters_1 = saida +'/'+"insersect_1.shp"
            inters_2 = saida +'/'+"insersect_2.shp"
            inters_3 = saida +'/'+"insersect_3.shp"

            bairro_escolhido = saida +'/'+ bairro_selecionado + '.shp'

            clip = saida +'/'+"area_de_interesse.shp"
            clip_2 = saida +'/'+"area_de_interesse.kml"

        processing.runalg("qgis:fixeddistancebuffer",local_1,dist_1*1000,5,False,buffer_1)
        processing.runalg("qgis:fixeddistancebuffer",local_2,dist_2*1000,5,False,buffer_2)
        processing.runalg("qgis:fixeddistancebuffer",local_3,dist_3*1000,5,False,buffer_3)

        processing.runalg("qgis:intersection",buffer_1,buffer_2,inters_1)
        processing.runalg("qgis:intersection",inters_1,buffer_3,inters_2)

        processing.runalg("qgis:saveselectedfeatures",(processing.runalg("qgis:selectbyattribute",bairro,"NOME",0,bairro_selecionado))['OUTPUT'],bairro_escolhido)

        processing.runalg("qgis:intersection",inters_2,bairro_escolhido,inters_3)

        processing.runalg("qgis:clip",bairro_escolhido,inters_3,clip)
        processing.runalg("qgis:clip",bairro_escolhido,inters_3,clip_2)

        print(bairro)
        print(local_1)
        print(local_2)
        print(local_3)
        print(bairro_escolhido)
        print(dist_1)
        print(dist_2)
        print(dist_3)
        print(buffer_1)
        print(buffer_2)
        print(buffer_3)
        print(inters_1)
        print(inters_2)
        print(inters_3)
        print(bairro_escolhido)
        print(clip)

