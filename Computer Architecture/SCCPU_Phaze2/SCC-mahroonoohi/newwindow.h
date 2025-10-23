#ifndef NEWWINDOW_H
#define NEWWINDOW_H
#include<QDialog>
#include<QGroupBox>
#include <QWidget>
#include<QMenuBar>
#include<QMenu>
#include<QAction>
#include<QVBoxLayout>
#include<QPushButton>
#include<QHBoxLayout>
class newwindow  :public QDialog
{
     Q_OBJECT
public:
    newwindow();
    ~newwindow(){};
    QPushButton * pb;
    QVBoxLayout * MainLayout,*Registers,*Memory;
    QHBoxLayout * layout,*Layout;
    QMenuBar *mnubar;
    QMenu * File,*Simulate, *Help;
    QAction * actiono,*actiontwo,*actiont,*actionf;
    QPushButton * ppc,*ins,*R0,*R1,*R2,*R3,*R4,*R5,*R6,*R7,*R8,*R9,*R10,*R11,*R12,*R13,*R14,*R15;
    QPushButton *Mem0,*Mem1,*Mem2,*Mem3,*Mem4,*Mem5,*Mem6,*Mem7,*Mem8,*Mem9,*Mem10,*Mem11,*Mem12
    ,*Mem13,*Mem14,*Mem15,*Mem16,*Mem17,*Mem18,*Mem19,*ALU,*RS,*RD,*RT,*Imm,*Opcode;
public slots:
    void ReloadFile();
    void exit();
    void run();
};

#endif // NEWWINDOW_H
