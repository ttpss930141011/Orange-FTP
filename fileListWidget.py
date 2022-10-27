import os, posixpath
from collections import defaultdict

from PyQt5.QtWidgets import QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSignal

from pyqt_files_already_exists_dialog import FilesAlreadyExistDialog
from pyqt_tooltip_list_widget import ToolTipListWidget


class FileListWidget(ToolTipListWidget):
    added = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__exists_dialog_not_ask_again_flag = False
        self.__duplicate_flag = True

        self.__extensions = []
        self.__basename_absname_dict = defaultdict(str)
        self.__show_filename_only_flag = False

    def __initUi(self):
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)

    def isDuplicateEnabled(self) -> bool:
        return self.__duplicate_flag

    def setDuplicateEnabled(self, f: bool):
        self.__duplicate_flag = f

    def setExtensions(self, extensions: list):
        self.__extensions = extensions

    def addFilename(self, filename: str):
        basename = os.path.basename(filename)
        self.__basename_absname_dict[basename] = filename
        if self.isFilenameOnly():
            self.addItem(basename)
        else:
            self.addItem(filename)

    def __addFilenames(self, filenames: list, cur_filename: str = ''):
        self.added.emit(filenames)
        for filename in filenames:
            self.addFilename(filename)
        self.__setCurrentFilename(filenames, cur_filename)

    def __setCurrentFilename(self, filenames: list, cur_filename: str = ''):
        cur_filename = filenames[0] if cur_filename == '' else cur_filename
        items = self.findItems(cur_filename, Qt.MatchFixedString)
        if items:
            r = self.row(items[0])
            self.setCurrentRow(r)

    def __execDuplicateFilenamesDialog(self, duplicate_filenames: list):
        dialog = FilesAlreadyExistDialog()
        dialog.setDontAskAgainChecked(self.__exists_dialog_not_ask_again_flag)
        dialog.setExistFiles(duplicate_filenames)
        reply = dialog.exec()

    def __getFilenamesInDirectory(self, dirname: str) -> list:
        filenames = [os.path.join(dirname, filename).replace(os.path.sep, posixpath.sep) for filename in
                     os.listdir(dirname)]
        return filenames

    def setDirectory(self, dirname: str, cur_filename: str = ''):
        filenames = self.__getFilenamesInDirectory(dirname)
        self.setFilenames(filenames, cur_filename)

    def addDirectory(self, dirname: str, cur_filename: str = ''):
        filenames = self.__getFilenamesInDirectory(dirname)
        self.addFilenames(filenames, cur_filename)

    def setFilenames(self, filenames: list, cur_filename: str = ''):
        self.clear()
        self.addFilenames(filenames, cur_filename=cur_filename)

    def addFilenames(self, filenames: list, cur_filename: str = ''):
        filenames = self.__getExtFilteredFiles(filenames)
        if self.isDuplicateEnabled():
            self.__addFilenames(filenames, cur_filename)
        else:
            duplicate_filenames, not_duplicate_filenames = self.__getDuplicateItems(filenames)
            if duplicate_filenames:
                self.__execDuplicateFilenamesDialog(duplicate_filenames)
                self.__addFilenames(not_duplicate_filenames)
            else:
                self.__addFilenames(filenames)

    def setFilenameOnly(self, f: bool):
        self.__show_filename_only_flag = f
        self.__execShowingBaseName(f)

    def remove(self, item: QListWidgetItem):
        filename = item.text()
        self.takeItem(self.row(item))
        self.__basename_absname_dict.pop(os.path.basename(filename))

    def getSelectedFilenames(self) -> list:
        items = self.selectedItems()
        filenames = [item.text() for item in items]
        return filenames

    #----- add new method -----
    def getAllFilenames(self) -> list:
        basename_absname_list = list(self.__basename_absname_dict.values())
        return basename_absname_list
    #----- add new method -----
    
    def removeSelectedRows(self):
        items = self.selectedItems()
        if items:
            removed_start_idx = self.row(items[0])
            cur_idx = removed_start_idx - 1
            if removed_start_idx == 0:
                cur_idx = 0
            items = list(reversed(items))
            for item in items:
                self.remove(item)
            self.setCurrentRow(cur_idx)

    def clear(self):
        for i in range(self.count() - 1, -1, -1):
            self.remove(self.item(i))
        super().clear()

    def isFilenameOnly(self) -> bool:
        return self.__show_filename_only_flag

    # refactoring needed
    def __getDuplicateItems(self, filenames: list):
        exists_file_lst = []
        not_exists_file_lst = []
        filenames_to_find = filenames
        for filename_to_find in filenames_to_find:
            if self.isFilenameOnly():
                items = self.findItems(os.path.basename(filename_to_find), Qt.MatchFixedString)
            else:
                items = self.findItems(filename_to_find, Qt.MatchFixedString)
            if items:
                exists_file_lst.append(filename_to_find)
            else:
                not_exists_file_lst.append(filename_to_find)
        return exists_file_lst, not_exists_file_lst

    def getAbsFilename(self, basename: str):
        return self.__basename_absname_dict[basename]

    def getFilenameFromRow(self, r: int) -> str:
        if self.isFilenameOnly():
            return self.getAbsFilename(self.item(r).text())
        else:
            return self.item(r).text()

    def __getExtFilteredFiles(self, lst):
        if len(self.__extensions) > 0:
            return list(filter(None, map(lambda x: x if os.path.splitext(x)[-1] in self.__extensions else None, lst)))
        else:
            return lst

    def __getUrlsFilenames(self, urls):
        return list(map(lambda x: x.path()[1:], urls))

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()

    def dragMoveEvent(self, e):
        pass

    def dropEvent(self, e):
        filenames = [file for file in self.__getExtFilteredFiles(
            self.__getUrlsFilenames(e.mimeData().urls())) if file]
        self.addFilenames(filenames)
        super().dropEvent(e)

    def __execShowingBaseName(self, f: bool):
        self.__show_filename_only_flag = f
        items = [self.item(i) for i in range(self.count())]
        if f:
            for item in items:
                absname = item.text()
                basename = os.path.basename(absname)
                item.setText(basename)
        else:
            for item in items:
                basename = item.text()
                absname = self.__basename_absname_dict[basename]
                item.setText(absname)
