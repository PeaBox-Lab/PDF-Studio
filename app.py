from __future__ import annotations
import os, sys, tempfile
from pathlib import Path
from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QAction, QColor, QIcon, QImage, QKeySequence, QPainter, QPen, QPixmap, QShortcut
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QGridLayout,QLabel,QPushButton,QFileDialog,QListWidget,QListWidgetItem,QGraphicsView,QGraphicsScene,QGraphicsPixmapItem,QGraphicsRectItem,QDialog,QDialogButtonBox,QFormLayout,QLineEdit,QDoubleSpinBox,QColorDialog,QMessageBox,QToolBar,QStatusBar,QInputDialog,QSplitter,QGroupBox,QScrollArea,QFrame)
import pdf_engine as engine

STYLE='''QMainWindow{background:#eef1f5} QToolBar{background:white;border-bottom:1px solid #d9dee7;padding:5px;spacing:6px} QPushButton{padding:8px 10px;border:1px solid #d9dee7;border-radius:7px;background:white;text-align:left} QPushButton:hover{background:#eef3ff;border-color:#8da4ef} QPushButton:checked{background:#e5ecff;color:#2448b8;border-color:#7b96e8} QListWidget{border:0;background:#f8f9fb;padding:5px} QGraphicsView{border:0;background:#292d34} QGroupBox{font-weight:600;border:1px solid #dfe3e8;border-radius:8px;margin-top:8px;padding-top:12px} QGroupBox::title{subcontrol-origin:margin;left:9px;padding:0 4px} QLabel#hint{color:#667085;background:#f2f4f7;padding:9px;border-radius:7px}'''

class SpanItem(QGraphicsRectItem):
    def __init__(self,rect,span,callback,scale):
        super().__init__(QRectF(rect[0]*scale,rect[1]*scale,(rect[2]-rect[0])*scale,(rect[3]-rect[1])*scale));self.span=span;self.callback=callback
        self.setPen(QPen(QColor(0,0,0,0),1));self.setBrush(QColor(61,99,221,0));self.setAcceptHoverEvents(True);self.setZValue(5)
    def hoverEnterEvent(self,e):self.setPen(QPen(QColor('#3d63dd'),1));self.setBrush(QColor(61,99,221,25))
    def hoverLeaveEvent(self,e):self.setPen(QPen(QColor(0,0,0,0),1));self.setBrush(QColor(61,99,221,0))
    def mouseDoubleClickEvent(self,e):self.callback(self.span);e.accept()

class ReplaceDialog(QDialog):
    def __init__(self,span,parent=None):
        super().__init__(parent);self.setWindowTitle("Replace existing text");self.setMinimumWidth(480)
        lay=QVBoxLayout(self);hint=QLabel("The original characters in this exact area will be removed. The replacement must fit the same area. Surrounding layout will not be moved.");hint.setWordWrap(True);hint.setObjectName('hint');lay.addWidget(hint)
        form=QFormLayout();self.original=QLineEdit(span['text']);self.original.setReadOnly(True);self.edit=QLineEdit(span['text']);self.edit.selectAll();form.addRow("Original",self.original);form.addRow("Replacement",self.edit);lay.addLayout(form)
        box=QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel);box.accepted.connect(self.accept);box.rejected.connect(self.reject);lay.addWidget(box)
    def value(self):return self.edit.text()

class AddTextDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent);self.setWindowTitle("Add new text");form=QFormLayout(self);self.text=QLineEdit();self.size=QDoubleSpinBox();self.size.setRange(6,72);self.size.setValue(14);form.addRow("Text",self.text);form.addRow("Font size",self.size);box=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel);box.accepted.connect(self.accept);box.rejected.connect(self.reject);form.addRow(box)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__();self.setWindowTitle("PeaBox PDF Studio Desktop");self.resize(1440,900);self.doc=None;self.path=None;self.page=0;self.scale=1.35;self.tool='edit';self.dirty=False
        self.build_toolbar();self.build_ui();self.setStatusBar(QStatusBar());self.statusBar().showMessage("Open a PDF to begin")
    def build_toolbar(self):
        bar=QToolBar();bar.setMovable(False);self.addToolBar(bar)
        for text,shortcut,slot in [("Open PDF","Ctrl+O",self.open_pdf),("Save As","Ctrl+Shift+S",self.save_as),("Undo reload","Ctrl+Z",self.reload_document)]:
            a=QAction(text,self);a.setShortcut(QKeySequence(shortcut));a.triggered.connect(slot);bar.addAction(a)
        bar.addSeparator();self.title=QLabel("No document open");bar.addWidget(self.title)
    def build_ui(self):
        root=QSplitter(Qt.Horizontal);self.setCentralWidget(root)
        tools=QWidget();tools.setFixedWidth(190);tv=QVBoxLayout(tools);tv.setContentsMargins(10,10,10,10);tv.addWidget(QLabel("TOOLS"))
        self.buttons={}
        specs=[('edit','Edit existing text',self.enable_edit),('add','Add new text',self.enable_add),('image','Add image or signature',self.add_image),('rotate','Rotate current page',self.rotate_page),('delete','Delete current page',self.delete_page),('merge','Merge PDF files',self.merge_files)]
        for key,label,fn in specs:
            b=QPushButton(label);b.setToolTip(label);b.setCheckable(key in ('edit','add'));b.clicked.connect(fn);tv.addWidget(b);self.buttons[key]=b
        self.buttons['edit'].setChecked(True);tv.addStretch();help=QLabel("Editing existing text\n\n1. Choose Edit existing text.\n2. Double-click the exact text.\n3. Enter a short replacement.\n4. Save As when finished.");help.setWordWrap(True);help.setObjectName('hint');tv.addWidget(help);root.addWidget(tools)
        self.thumbs=QListWidget();self.thumbs.setFixedWidth(170);self.thumbs.currentRowChanged.connect(self.goto_page);root.addWidget(self.thumbs)
        center=QWidget();cv=QVBoxLayout(center);cv.setContentsMargins(0,0,0,0);nav=QHBoxLayout();
        self.prev=QPushButton("Previous page");self.next=QPushButton("Next page");self.fit=QPushButton("Fit page");self.actual=QPushButton("100%");self.pageLabel=QLabel("Page 0 of 0")
        self.prev.clicked.connect(lambda:self.goto_page(max(0,self.page-1)));self.next.clicked.connect(lambda:self.goto_page(min(self.doc.page_count-1,self.page+1)) if self.doc else None);self.fit.clicked.connect(self.fit_page);self.actual.clicked.connect(lambda:self.set_zoom(1.0))
        for w in (self.prev,self.next,self.pageLabel,self.fit,self.actual):nav.addWidget(w)
        nav.addStretch();cv.addLayout(nav)
        self.scene=QGraphicsScene();self.view=QGraphicsView(self.scene);self.view.setRenderHint(QPainter.Antialiasing);self.view.setDragMode(QGraphicsView.ScrollHandDrag);cv.addWidget(self.view);root.addWidget(center)
        inspector=QWidget();inspector.setFixedWidth(260);iv=QVBoxLayout(inspector);head=QLabel("DOCUMENT");head.setStyleSheet('font-weight:700');iv.addWidget(head);self.info=QLabel("Open a PDF to see document details.");self.info.setWordWrap(True);iv.addWidget(self.info);g=QGroupBox("Safe editing model");gl=QVBoxLayout(g);msg=QLabel("PeaBox replaces only the selected text rectangle. It does not reflow or move nearby PDF content. Long text is rejected rather than damaging the layout.");msg.setWordWrap(True);gl.addWidget(msg);iv.addWidget(g);iv.addStretch();root.addWidget(inspector);root.setStretchFactor(2,1)
    def open_pdf(self):
        path,_=QFileDialog.getOpenFileName(self,"Open PDF","","PDF files (*.pdf)")
        if not path:return
        try:self.load_path(path)
        except Exception as e:QMessageBox.critical(self,"Cannot open PDF",str(e))
    def load_path(self,path):
        if self.doc:self.doc.close()
        self.doc=engine.open_document(path);self.path=path;self.page=0;self.dirty=False;self.title.setText(Path(path).name);self.populate_thumbs();self.thumbs.setCurrentRow(0);self.render();self.statusBar().showMessage("Double-click existing text to replace it")
    def populate_thumbs(self):
        self.thumbs.clear()
        for i in range(self.doc.page_count):
            data,_,_=engine.render_page(self.doc,i,.2);item=QListWidgetItem(QIcon(QPixmap.fromImage(QImage.fromData(data))),f"Page {i+1}");item.setSizeHint(item.sizeHint()*1.4);self.thumbs.addItem(item)
    def render(self):
        if not self.doc:return
        data,w,h=engine.render_page(self.doc,self.page,self.scale);pix=QPixmap.fromImage(QImage.fromData(data));self.scene.clear();self.scene.setSceneRect(0,0,w,h);self.scene.addItem(QGraphicsPixmapItem(pix))
        if self.tool=='edit':
            for span in engine.text_spans(self.doc[self.page]):self.scene.addItem(SpanItem(span['rect'],span,self.replace_text,self.scale))
        self.pageLabel.setText(f"Page {self.page+1} of {self.doc.page_count}");self.info.setText(f"{Path(self.path).name}\n\nPages: {self.doc.page_count}\nCurrent page: {self.page+1}\nMode: {'Edit existing text' if self.tool=='edit' else 'Add new text'}")
    def goto_page(self,row):
        if not self.doc or row<0:return
        self.page=row
        if self.thumbs.currentRow()!=row:self.thumbs.setCurrentRow(row)
        self.render()
    def enable_edit(self):self.tool='edit';self.buttons['edit'].setChecked(True);self.buttons['add'].setChecked(False);self.view.setDragMode(QGraphicsView.ScrollHandDrag);self.render();self.statusBar().showMessage("Double-click the exact existing text you want to replace")
    def enable_add(self):self.tool='add';self.buttons['edit'].setChecked(False);self.buttons['add'].setChecked(True);self.view.setDragMode(QGraphicsView.NoDrag);self.statusBar().showMessage("Double-click a blank position on the page to add new text");self.view.mouseDoubleClickEvent=self.add_text_at
    def replace_text(self,span):
        d=ReplaceDialog(span,self)
        if d.exec()!=QDialog.Accepted:return
        try:engine.replace_span(self.doc,self.page,span,d.value());self.dirty=True;self.refresh_after_edit("Existing text replaced without moving surrounding content")
        except Exception as e:QMessageBox.warning(self,"Replacement not applied",str(e))
    def add_text_at(self,event):
        if self.tool!='add':return
        pos=self.view.mapToScene(event.position().toPoint());d=AddTextDialog(self)
        if d.exec()==QDialog.Accepted and d.text.text().strip():engine.add_text(self.doc,self.page,(pos.x()/self.scale,pos.y()/self.scale),d.text.text(),d.size.value());self.dirty=True;self.refresh_after_edit("New text added")
    def add_image(self):
        if not self.doc:return
        path,_=QFileDialog.getOpenFileName(self,"Choose image or signature","","Images (*.png *.jpg *.jpeg)")
        if not path:return
        page=self.doc[self.page];engine.add_image(self.doc,self.page,path,(36,36,min(236,page.rect.width-20),min(156,page.rect.height-20)));self.dirty=True;self.refresh_after_edit("Image added at top-left; precise placement is planned")
    def rotate_page(self):
        if self.doc:engine.rotate_pages(self.doc,[self.page],90);self.dirty=True;self.refresh_after_edit("Page rotated")
    def delete_page(self):
        if not self.doc:return
        if QMessageBox.question(self,"Delete page",f"Delete page {self.page+1}?")!=QMessageBox.Yes:return
        try:engine.delete_pages(self.doc,[self.page]);self.page=min(self.page,self.doc.page_count-1);self.populate_thumbs();self.thumbs.setCurrentRow(self.page);self.dirty=True;self.render()
        except Exception as e:QMessageBox.warning(self,"Cannot delete",str(e))
    def merge_files(self):
        paths,_=QFileDialog.getOpenFileNames(self,"Choose PDFs to merge","","PDF files (*.pdf)")
        if len(paths)<2:return
        out,_=QFileDialog.getSaveFileName(self,"Save merged PDF","merged.pdf","PDF files (*.pdf)")
        if out:engine.merge_paths(paths,out);QMessageBox.information(self,"Merge complete",f"Saved to\n{out}")
    def save_as(self):
        if not self.doc:return
        out,_=QFileDialog.getSaveFileName(self,"Save edited PDF",str(Path(self.path).with_name(Path(self.path).stem+'-edited.pdf')),"PDF files (*.pdf)")
        if out:
            try:engine.save_copy(self.doc,out);self.dirty=False;QMessageBox.information(self,"Saved",f"Saved to\n{out}")
            except Exception as e:QMessageBox.critical(self,"Save failed",str(e))
    def reload_document(self):
        if self.path and QMessageBox.question(self,"Discard edits","Reload the original PDF and discard unsaved edits?")==QMessageBox.Yes:self.load_path(self.path)
    def refresh_after_edit(self,msg):self.render();self.populate_thumbs();self.thumbs.setCurrentRow(self.page);self.statusBar().showMessage(msg)
    def fit_page(self):
        if not self.doc:return
        r=self.doc[self.page].rect;vw=max(200,self.view.viewport().width()-30);vh=max(200,self.view.viewport().height()-30);self.set_zoom(min(vw/r.width,vh/r.height))
    def set_zoom(self,z):self.scale=max(.3,min(3,z));self.render()
    def closeEvent(self,e):
        if self.dirty and QMessageBox.question(self,"Unsaved edits","Close without saving?")!=QMessageBox.Yes:e.ignore();return
        if self.doc:self.doc.close();e.accept()

def main():
    app=QApplication(sys.argv);app.setStyleSheet(STYLE);w=MainWindow();w.show();sys.exit(app.exec())
if __name__=='__main__':main()
