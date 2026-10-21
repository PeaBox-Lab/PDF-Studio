import sys
from pathlib import Path
import pymupdf
from PySide6.QtCore import Qt,QRectF
from PySide6.QtGui import QAction,QColor,QIcon,QImage,QKeySequence,QPen,QPixmap
from PySide6.QtWidgets import *
import pdf_engine as engine

STYLE='''QMainWindow{background:#eef1f5}QToolBar{background:white;border-bottom:1px solid #d9dee7;padding:5px;spacing:5px}QPushButton{padding:9px 10px;border:1px solid #d9dee7;border-radius:7px;background:white;text-align:left}QPushButton:hover{background:#f2f5ff}QPushButton:checked{background:#e5ecff;color:#2448b8;border-color:#88a0eb}QListWidget{border:0;background:#f8f9fb;padding:4px}QGraphicsView{border:0;background:#292d34}QLabel#hint{color:#5f6877;background:#f2f4f7;padding:9px;border-radius:7px}QGroupBox{font-weight:600;border:1px solid #dfe3e8;border-radius:8px;margin-top:8px;padding-top:12px}'''

class SpanItem(QGraphicsRectItem):
 def __init__(self,span,callback,zoom):
  x0,y0,x1,y1=span['rect'];super().__init__(QRectF(x0*zoom,y0*zoom,(x1-x0)*zoom,(y1-y0)*zoom));self.span=span;self.callback=callback
  self.setPen(QPen(Qt.transparent));self.setBrush(Qt.transparent);self.setAcceptHoverEvents(True);self.setZValue(5);self.setToolTip('Double-click to edit this text')
 def hoverEnterEvent(self,e):self.setPen(QPen(QColor('#3d63dd'),2));self.setBrush(QColor(61,99,221,30))
 def hoverLeaveEvent(self,e):self.setPen(QPen(Qt.transparent));self.setBrush(Qt.transparent)
 def mouseDoubleClickEvent(self,e):self.callback(self.span);e.accept()

class TextDialog(QDialog):
 def __init__(self,title,initial='',size=14,parent=None,existing=False):
  super().__init__(parent);self.setWindowTitle(title);self.setMinimumWidth(480);v=QVBoxLayout(self)
  note=QLabel('Original font size is preserved. If replacement text cannot fit, PeaBox stops the edit instead of shrinking it.' if existing else 'Add short new text at the centre of the current page.');note.setWordWrap(True);note.setObjectName('hint');v.addWidget(note)
  f=QFormLayout();self.text=QLineEdit(initial);self.size=QDoubleSpinBox();self.size.setRange(6,72);self.size.setValue(size);f.addRow('Text',self.text)
  if existing:self.size.setDisabled(True)
  f.addRow('Font size',self.size);v.addLayout(f);box=QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel);box.accepted.connect(self.accept);box.rejected.connect(self.reject);v.addWidget(box);self.text.selectAll()

class ImageDialog(QDialog):
 def __init__(self,page,parent=None):
  super().__init__(parent);self.setWindowTitle('Add image or signature');self.path='';f=QFormLayout(self);pick=QPushButton('Choose PNG or JPG');pick.clicked.connect(self.choose);self.file=QLabel('No image selected');f.addRow(pick,self.file)
  self.x=QDoubleSpinBox();self.y=QDoubleSpinBox();self.w=QDoubleSpinBox();self.h=QDoubleSpinBox()
  for s in (self.x,self.y,self.w,self.h):s.setRange(0,5000)
  self.x.setValue(36);self.y.setValue(36);self.w.setValue(min(180,page.rect.width-50));self.h.setValue(80)
  for name,w in [('X',self.x),('Y',self.y),('Width',self.w),('Height',self.h)]:f.addRow(name,w)
  box=QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel);box.accepted.connect(self.accept);box.rejected.connect(self.reject);f.addRow(box)
 def choose(self):
  p,_=QFileDialog.getOpenFileName(self,'Choose image','','Images (*.png *.jpg *.jpeg)')
  if p:self.path=p;self.file.setText(Path(p).name)
 def accept(self):
  if not self.path:QMessageBox.warning(self,'Image required','Choose an image first.');return
  super().accept()

class Main(QMainWindow):
 def __init__(self):
  super().__init__();self.setWindowTitle('PeaBox PDF Studio Desktop v1.3.0');self.resize(1460,900);self.doc=None;self.path=None;self.page=0;self.zoom=1.25;self.dirty=False;self.undo_stack=[];self.redo_stack=[];self.mode='edit'
  self.build_toolbar();self.build_ui();self.setStatusBar(QStatusBar());self.statusBar().showMessage('Open a PDF to begin')
 def action(self,bar,name,key,fn):
  a=QAction(name,self);a.setShortcut(QKeySequence(key));a.triggered.connect(fn);bar.addAction(a);return a
 def build_toolbar(self):
  b=QToolBar();b.setMovable(False);self.addToolBar(b);self.action(b,'Open','Ctrl+O',self.open);self.action(b,'Save As','Ctrl+Shift+S',self.save);b.addSeparator();self.undo_action=self.action(b,'Undo','Ctrl+Z',self.undo);self.redo_action=self.action(b,'Redo','Ctrl+Y',self.redo);b.addSeparator();self.action(b,'Zoom Out','Ctrl+-',lambda:self.set_zoom(self.zoom-.15));self.action(b,'Zoom In','Ctrl++',lambda:self.set_zoom(self.zoom+.15));self.action(b,'Fit Page','Ctrl+0',self.fit);self.action(b,'100%','Ctrl+1',lambda:self.set_zoom(1.0));b.addSeparator();self.title=QLabel('No document open');b.addWidget(self.title);self.update_history()
 def build_ui(self):
  root=QSplitter();self.setCentralWidget(root)
  tools=QWidget();tools.setFixedWidth(220);v=QVBoxLayout(tools);head=QLabel('TOOLS');head.setStyleSheet('font-weight:700');v.addWidget(head)
  for label,fn in [('Edit existing text',lambda:self.set_mode('edit')),('Highlight text',lambda:self.set_mode('highlight')),('Underline text',lambda:self.set_mode('underline')),('Strike out text',lambda:self.set_mode('strikeout')),('Permanently redact text',lambda:self.set_mode('redact')),('Add comment to page',self.add_comment),('Add new text',self.add_text),('Add image or signature',self.add_image),('Rotate current page',self.rotate),('Duplicate current page',self.duplicate),('Extract selected pages',self.extract),('Insert blank page',self.blank),('Insert PDF after page',self.insert_pdf),('Delete current page',self.delete),('Merge PDF files',self.merge)]:
   btn=QPushButton(label);btn.clicked.connect(fn);v.addWidget(btn)
  v.addStretch();hint=QLabel('Existing text: double-click the exact text. PeaBox preserves its size and rejects replacements that do not fit.');hint.setWordWrap(True);hint.setObjectName('hint');v.addWidget(hint);root.addWidget(tools)
  self.thumbs=QListWidget();self.thumbs.setFixedWidth(190);self.thumbs.setSelectionMode(QAbstractItemView.ExtendedSelection);self.thumbs.setDragDropMode(QAbstractItemView.InternalMove);self.thumbs.setDefaultDropAction(Qt.MoveAction);self.thumbs.currentRowChanged.connect(self.goto);self.thumbs.model().rowsMoved.connect(self.pages_reordered);root.addWidget(self.thumbs)
  center=QWidget();cv=QVBoxLayout(center);cv.setContentsMargins(0,0,0,0);nav=QHBoxLayout();self.prev=QPushButton('Previous');self.next=QPushButton('Next');self.page_label=QLabel('Page 0 of 0');self.zoom_label=QLabel('100%');self.prev.clicked.connect(lambda:self.goto(max(0,self.page-1)));self.next.clicked.connect(lambda:self.goto(min(self.doc.page_count-1,self.page+1)) if self.doc else None)
  for w in (self.prev,self.next,self.page_label,self.zoom_label):nav.addWidget(w)
  nav.addStretch();cv.addLayout(nav);self.scene=QGraphicsScene();self.view=QGraphicsView(self.scene);self.view.setDragMode(QGraphicsView.ScrollHandDrag);cv.addWidget(self.view);root.addWidget(center);root.setStretchFactor(2,1)
  side=QWidget();side.setFixedWidth(270);sv=QVBoxLayout(side);g=QGroupBox('Document');gl=QVBoxLayout(g);self.info=QLabel('Open a PDF to see details.');self.info.setWordWrap(True);gl.addWidget(self.info);sv.addWidget(g);g2=QGroupBox('Editing model');g2l=QVBoxLayout(g2);m=QLabel('Short corrections are safest. Existing text keeps its detected size, baseline and colour. Long replacements are rejected rather than squeezed into the page.');m.setWordWrap(True);g2l.addWidget(m);sv.addWidget(g2);sv.addStretch();root.addWidget(side)
 def open(self):
  p,_=QFileDialog.getOpenFileName(self,'Open PDF','','PDF files (*.pdf)')
  if p:self.load(p)
 def load(self,p):
  try:
   if self.doc:self.doc.close()
   self.doc=engine.open_document(p);self.path=p;self.page=0;self.dirty=False;self.undo_stack=[];self.redo_stack=[];self.title.setText(Path(p).name);self.refresh_thumbs();self.thumbs.setCurrentRow(0);self.fit();self.update_history()
  except Exception as e:QMessageBox.critical(self,'Cannot open PDF',str(e))
 def snapshot(self):
  if not self.doc:return
  self.undo_stack.append(self.doc.tobytes(garbage=4,deflate=True));self.undo_stack=self.undo_stack[-20:];self.redo_stack.clear();self.update_history()
 def restore(self,data):
  if self.doc:self.doc.close()
  self.doc=pymupdf.open(stream=data,filetype='pdf');self.page=min(self.page,self.doc.page_count-1);self.refresh_thumbs();self.thumbs.setCurrentRow(self.page);self.render()
 def undo(self):
  if not self.undo_stack or not self.doc:return
  self.redo_stack.append(self.doc.tobytes(garbage=4,deflate=True));self.restore(self.undo_stack.pop());self.dirty=True;self.update_history();self.statusBar().showMessage('Undo complete')
 def redo(self):
  if not self.redo_stack or not self.doc:return
  self.undo_stack.append(self.doc.tobytes(garbage=4,deflate=True));self.restore(self.redo_stack.pop());self.dirty=True;self.update_history();self.statusBar().showMessage('Redo complete')
 def update_history(self):
  if hasattr(self,'undo_action'):self.undo_action.setEnabled(bool(self.undo_stack));self.redo_action.setEnabled(bool(self.redo_stack))
 def refresh_thumbs(self):
  self._refreshing=True;self.thumbs.blockSignals(True);self.thumbs.clear()
  for i in range(self.doc.page_count):
   data,_,_=engine.render_page(self.doc,i,.18);item=QListWidgetItem(QIcon(QPixmap.fromImage(QImage.fromData(data))),f'Page {i+1}');item.setData(Qt.UserRole,i);item.setSizeHint(item.sizeHint()*1.35);self.thumbs.addItem(item)
  self.thumbs.blockSignals(False);self._refreshing=False
 def render(self):
  if not self.doc:return
  data,w,h=engine.render_page(self.doc,self.page,self.zoom);self.scene.clear();self.scene.setSceneRect(0,0,w,h);self.scene.addPixmap(QPixmap.fromImage(QImage.fromData(data)))
  for s in engine.text_spans(self.doc[self.page]):self.scene.addItem(SpanItem(s,self.activate_span,self.zoom))
  self.page_label.setText(f'Page {self.page+1} of {self.doc.page_count}');self.zoom_label.setText(f'{round(self.zoom*100)}%');self.info.setText(f'{Path(self.path).name}\n\nPages: {self.doc.page_count}\nCurrent page: {self.page+1}\nZoom: {round(self.zoom*100)}%\nMode: {self.mode.capitalize()}')
 def goto(self,i):
  if self.doc and 0<=i<self.doc.page_count:self.page=i
  if self.doc and self.thumbs.currentRow()!=i:self.thumbs.blockSignals(True);self.thumbs.setCurrentRow(i);self.thumbs.blockSignals(False)
  if self.doc:self.render()
 def set_mode(self,mode):
  self.mode=mode
  labels={'edit':'Double-click existing text to edit','highlight':'Double-click text to highlight','underline':'Double-click text to underline','strikeout':'Double-click text to strike out','redact':'Double-click text to permanently redact'}
  self.statusBar().showMessage(labels.get(mode,'Ready'));self.render()
 def edit_mode(self):self.set_mode('edit')
 def activate_span(self,span):
  if self.mode=='edit':self.replace(span);return
  if self.mode=='redact' and QMessageBox.warning(self,'Permanent redaction','This permanently removes the selected text. Continue?',QMessageBox.Yes|QMessageBox.No)!=QMessageBox.Yes:return
  self.snapshot()
  try:engine.annotate_span(self.doc,self.page,span,self.mode);self.changed(self.mode.capitalize()+' applied')
  except Exception as e:self.undo_stack.pop();self.update_history();QMessageBox.warning(self,'Annotation failed',str(e))
 def add_comment(self):
  if not self.doc:return
  text,ok=QInputDialog.getMultiLineText(self,'Add comment','Comment text:')
  if not ok or not text.strip():return
  self.snapshot();r=self.doc[self.page].rect;engine.add_comment(self.doc,self.page,(r.width-36,36),text);self.changed('Comment added at top-right')

 def replace(self,s):
  d=TextDialog('Replace existing text',s['text'],s['size'],self,True)
  if d.exec()!=QDialog.Accepted:return
  self.snapshot()
  try:size=engine.replace_span(self.doc,self.page,s,d.text.text());self.changed(f'Text replaced at original {size:.1f} pt size')
  except Exception as e:self.undo_stack.pop();self.update_history();QMessageBox.warning(self,'Text not changed',str(e))
 def add_text(self):
  if not self.doc:return
  d=TextDialog('Add new text','',14,self,False)
  if d.exec()!=QDialog.Accepted or not d.text.text().strip():return
  self.snapshot();r=self.doc[self.page].rect;engine.add_text(self.doc,self.page,(r.width*.35,r.height*.5),d.text.text(),d.size.value());self.changed('New text added near page centre')
 def add_image(self):
  if not self.doc:return
  d=ImageDialog(self.doc[self.page],self)
  if d.exec()!=QDialog.Accepted:return
  self.snapshot();engine.add_image(self.doc,self.page,d.path,(d.x.value(),d.y.value(),d.x.value()+d.w.value(),d.y.value()+d.h.value()));self.changed('Image or signature added')
 def rotate(self):
  if self.doc:self.snapshot();engine.rotate_pages(self.doc,[self.page],90);self.changed('Page rotated')
 def delete(self):
  if not self.doc:return
  if QMessageBox.question(self,'Delete page',f'Delete page {self.page+1}?')!=QMessageBox.Yes:return
  self.snapshot()
  try:engine.delete_pages(self.doc,[self.page]);self.page=min(self.page,self.doc.page_count-1);self.changed('Page deleted')
  except Exception as e:self.undo_stack.pop();self.update_history();QMessageBox.warning(self,'Cannot delete page',str(e))

 def pages_reordered(self,*args):
  if not self.doc or getattr(self,'_refreshing',False):return
  order=[]
  for i in range(self.thumbs.count()):order.append(self.thumbs.item(i).data(Qt.UserRole))
  if sorted(order)!=list(range(self.doc.page_count)):return
  self.snapshot();engine.reorder_pages(self.doc,order);self.page=self.thumbs.currentRow();self.changed('Pages reordered')
 def duplicate(self):
  if not self.doc:return
  self.snapshot();engine.duplicate_page(self.doc,self.page);self.page+=1;self.changed('Page duplicated')
 def extract(self):
  if not self.doc:return
  indexes=sorted({self.thumbs.row(x) for x in self.thumbs.selectedItems()}) or [self.page]
  out,_=QFileDialog.getSaveFileName(self,'Extract selected pages','extracted-pages.pdf','PDF files (*.pdf)')
  if not out:return
  try:engine.extract_pages(self.doc,indexes,out);QMessageBox.information(self,'Pages extracted',f'Saved {len(indexes)} page(s) to\n{out}')
  except Exception as e:QMessageBox.warning(self,'Extract failed',str(e))
 def blank(self):
  if not self.doc:return
  self.snapshot();engine.insert_blank_page(self.doc,self.page);self.page+=1;self.changed('Blank page inserted')
 def insert_pdf(self):
  if not self.doc:return
  path,_=QFileDialog.getOpenFileName(self,'Insert PDF after current page','','PDF files (*.pdf)')
  if not path:return
  self.snapshot()
  try:engine.insert_pdf_after(self.doc,self.page,path);self.changed('PDF inserted after current page')
  except Exception as e:self.undo_stack.pop();self.update_history();QMessageBox.warning(self,'Insert failed',str(e))

 def merge(self):
  paths,_=QFileDialog.getOpenFileNames(self,'Choose PDFs to merge','','PDF files (*.pdf)')
  if len(paths)<2:return
  out,_=QFileDialog.getSaveFileName(self,'Save merged PDF','merged.pdf','PDF files (*.pdf)')
  if out:engine.merge_paths(paths,out);QMessageBox.information(self,'Merge complete',f'Saved to\n{out}')
 def changed(self,msg):
  self.dirty=True;self.refresh_thumbs();self.thumbs.setCurrentRow(self.page);self.render();self.update_history();self.statusBar().showMessage(msg)
 def fit(self):
  if not self.doc:return
  r=self.doc[self.page].rect;self.set_zoom(min((self.view.viewport().width()-34)/r.width,(self.view.viewport().height()-34)/r.height))
 def set_zoom(self,z):
  self.zoom=max(.25,min(4.0,z));self.render()
 def save(self):
  if not self.doc:return
  p,_=QFileDialog.getSaveFileName(self,'Save edited PDF',str(Path(self.path).with_name(Path(self.path).stem+'-edited.pdf')),'PDF files (*.pdf)')
  if p:
   try:engine.save_copy(self.doc,p);self.dirty=False;QMessageBox.information(self,'Saved',f'Saved to\n{p}')
   except Exception as e:QMessageBox.critical(self,'Save failed',str(e))
 def closeEvent(self,e):
  if self.dirty and QMessageBox.question(self,'Unsaved changes','Close without saving?')!=QMessageBox.Yes:e.ignore();return
  if self.doc:self.doc.close()
  e.accept()

def main():
 app=QApplication(sys.argv);app.setApplicationName('PeaBox PDF Studio');app.setStyleSheet(STYLE);w=Main();w.show();sys.exit(app.exec())
if __name__=='__main__':main()
