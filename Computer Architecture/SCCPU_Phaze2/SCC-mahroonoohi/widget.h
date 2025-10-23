#ifndef WIDGET_H
#define WIDGET_H
#include"newwindow.h"
#include <QWidget>
#include<QPushButton>
#include<QVBoxLayout>
#include<QHBoxLayout>
#include<QGroupBox>
QT_BEGIN_NAMESPACE
namespace Ui { class Widget; }
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    newwindow  * FWindow;
    Widget(QWidget *parent = nullptr);
    ~Widget();
public slots:
      void FetchWindow();
      void closeWindow();
private:
    QVBoxLayout * MainLayout;
    QHBoxLayout *HLayout;
    QGroupBox *GroupBox;
    QPushButton *QP,*QPT;
};
#endif // WIDGET_H
