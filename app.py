import sys
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage,QPixmap
from PySide6.QtWidgets import *
import pdf_engine as e
class App(QMainWindow):
 def __init__(self):
  super().__init__();self.setWindowTitle('PeaBox PDF Studio Desktop v1.5.0');self.resize(1250,820);self.doc=None;self.path=None
  w=QWidget();h=QHBoxLayout(w);self.setCentralWidget(w);left=QVBoxLayout();h.addLayout(left);self.tools=[]
  for name,fn in [('Open PDF',self.open),('Document properties',self.props),('Add watermark',self.watermark),('Header and footer',self.hf),('Add page numbers',self.numbers),('Create protected copy',self.protect),('Save As',self.saveas)]:
   b=QPushButton(name);b.setMinimumHeight(38);b.clicked.connect(fn);left.addWidget(b);self.tools.append(b)
  left.addStretch();self.image=QLabel('Open a PDF to begin');self.image.setAlignment(Qt.AlignCenter);self.scroll=QScrollArea();self.scroll.setWidgetResizable(True);self.scroll.setWidget(self.image);h.addWidget(self.scroll,1);self.statusBar().showMessage('Ready')
 def render(self):
  if not self.doc:return
  pix=self.doc[0].get_pixmap(matrix=__import__('pymupdf').Matrix(1.25,1.25),alpha=False);q=QImage.fromData(pix.tobytes('png'));self.image.setPixmap(QPixmap.fromImage(q));self.image.resize(q.size())
 def open(self):
  p,_=QFileDialog.getOpenFileName(self,'Open PDF','','PDF (*.pdf)')
  if p:
   if self.doc:self.doc.close()
   self.doc=e.open_document(p);self.path=p;self.render();self.statusBar().showMessage(f'Opened {Path(p).name} - {self.doc.page_count} pages')
 def props(self):
  if not self.doc:return
  m=self.doc.metadata or {};d=QDialog(self);d.setWindowTitle('Document properties');f=QFormLayout(d);title=QLineEdit(m.get('title') or '');author=QLineEdit(m.get('author') or '');subject=QLineEdit(m.get('subject') or '');keys=QLineEdit(m.get('keywords') or '');f.addRow('Format',QLabel(m.get('format') or 'PDF'));f.addRow('Pages',QLabel(str(self.doc.page_count)));f.addRow('Title',title);f.addRow('Author',author);f.addRow('Subject',subject);f.addRow('Keywords',keys);box=QDialogButtonBox(QDialogButtonBox.Save|QDialogButtonBox.Cancel);box.accepted.connect(d.accept);box.rejected.connect(d.reject);f.addRow(box)
  if d.exec()==QDialog.Accepted:e.set_metadata(self.doc,title.text(),author.text(),subject.text(),keys.text());self.statusBar().showMessage('Metadata updated')
 def watermark(self):
  if not self.doc:return
  t,ok=QInputDialog.getText(self,'Watermark','Text:',QLineEdit.Normal,'CONFIDENTIAL')
  if ok and t.strip():e.add_watermark(self.doc,t);self.render();self.statusBar().showMessage('Watermark added to all pages')
 def hf(self):
  if not self.doc:return
  h,ok=QInputDialog.getText(self,'Header','Header text:');
  if not ok:return
  f,ok=QInputDialog.getText(self,'Footer','Footer text:');
  if ok:e.add_header_footer(self.doc,h,f);self.render();self.statusBar().showMessage('Header/footer added')
 def numbers(self):
  if not self.doc:return
  p,ok=QInputDialog.getText(self,'Page numbers','Prefix:',QLineEdit.Normal,'Page ')
  if not ok:return
  n,ok=QInputDialog.getInt(self,'Page numbers','Start:',1,0,999999)
  if ok:e.add_page_numbers(self.doc,p,n);self.render();self.statusBar().showMessage('Page numbers added')
 def protect(self):
  if not self.doc:return
  owner,ok=QInputDialog.getText(self,'Protected copy','Owner password:',QLineEdit.Password)
  if not ok:return
  user,ok=QInputDialog.getText(self,'Protected copy','Open password (optional):',QLineEdit.Password)
  if not ok:return
  out,_=QFileDialog.getSaveFileName(self,'Save protected copy','protected.pdf','PDF (*.pdf)')
  if out:
   try:e.save_encrypted(self.doc,out,owner,user,True,False);QMessageBox.information(self,'Done',f'Protected copy saved to\n{out}')
   except Exception as x:QMessageBox.warning(self,'Failed',str(x))
 def saveas(self):
  if not self.doc:return
  out,_=QFileDialog.getSaveFileName(self,'Save As',str(Path(self.path).with_name(Path(self.path).stem+'-edited.pdf')),'PDF (*.pdf)')
  if out:e.save(self.doc,out);self.statusBar().showMessage('Saved')
def main():
 a=QApplication(sys.argv);w=App();w.show();sys.exit(a.exec())
if __name__=='__main__':main()
