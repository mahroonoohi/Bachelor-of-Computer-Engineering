#include "widget.h"
#include "ui_widget.h"
#include<QDialog>
#include"newwindow.h"
Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
    MainLayout =new QVBoxLayout();
    HLayout = new QHBoxLayout();
    GroupBox= new QGroupBox("Miniature Single Cycle CPU");
    GroupBox->setLayout(HLayout);
    QP=new QPushButton("Start");
    QPT= new QPushButton("Cancle");
    HLayout->addWidget(QP);
    HLayout->addWidget(QPT);
    MainLayout->addWidget(GroupBox);
    setLayout(MainLayout);
    connect(QP,SIGNAL(clicked()),this,SLOT(FetchWindow()));
    connect(QPT,SIGNAL(clicked()),this,SLOT(closeWindow()));
}
void Widget::FetchWindow()
{
    FWindow=new newwindow();
    FWindow->show();
   this->close();
}
void Widget::closeWindow()
{
   this->~Widget();
}
Widget::~Widget()
{
     this->close();
}

