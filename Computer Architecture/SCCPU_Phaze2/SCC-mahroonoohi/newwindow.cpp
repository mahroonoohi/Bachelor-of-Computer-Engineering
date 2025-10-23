#include "newwindow.h"
#include<QVBoxLayout>
#include<QFile>
#include<QDialog>
#include<QMessageBox>
#include<QTextStream>
#include<QFileDialog>
#include<QRandomGenerator64>
#include "C.h"
INstruction inst[15];int randomm[16],memory[20];
newwindow::newwindow()
{
    MainLayout=new QVBoxLayout;
    //menu
    mnubar=new QMenuBar;
    MainLayout->setMenuBar(mnubar);
    File=new QMenu("File");
    mnubar->addMenu(File);
    Simulate=new QMenu("Simulator");
    mnubar->addMenu(Simulate);
    actiono=new QAction("Reinitialize and Load File");
    File->addAction(actiono);
    actiontwo=new QAction("Exit");
    actiontwo->setShortcut(tr("Ctrl+W"));
    File->addAction(actiontwo);
    actionf=new QAction("Run Step By Step");
    actionf->setShortcut(tr("F10"));
    Simulate->addAction(actionf);
    this->setFixedSize(1280,720);
    connect(actiono,SIGNAL(triggered()),this,SLOT(ReloadFile()));
    connect(actiontwo,SIGNAL(triggered()),this,SLOT(exit()));
    layout=new QHBoxLayout;
    Layout=new QHBoxLayout;
    ppc=new QPushButton("PC");
    R0=new QPushButton("Registre 0= 0");
    R1=new QPushButton("Register 1=");
    R2=new QPushButton("Register 2=");
    R3=new QPushButton("Register 3=");
    R4=new QPushButton("Register 4=");
    R5=new QPushButton("Register 5=");
    R6=new QPushButton("Register 6=");
    R7=new QPushButton("Register 7=");
    R8=new QPushButton("register 8=");
    R9=new QPushButton("Register9=");
    R10=new QPushButton("Register 10=");
    R11=new QPushButton("Register 11=");
    R12=new QPushButton("Register 12=");
    R13=new QPushButton("Register 13=");
    R14=new QPushButton("Register 14=");
    R15=new QPushButton("Register 15=");
    layout->addWidget(ppc);
    ins=new QPushButton("ins = ");
    Opcode=new QPushButton("OPcode = ");
    RS=new QPushButton("RS = ");
    RD=new QPushButton("Rd = ");
    RT=new QPushButton("Rt = ");
    Imm=new QPushButton("imm = ");
    Layout->addWidget(Opcode);
    Layout->addWidget(RS);
    Layout->addWidget(RD);
    Layout->addWidget(RT);
    Layout->addWidget(Imm);
    layout->addWidget(ins);
    MainLayout->addLayout(Layout);
    //Registers
    Registers=new QVBoxLayout;
    Registers->addWidget(R0);
    Registers->addWidget(R1);
    Registers->addWidget(R2);
    Registers->addWidget(R3);
    Registers->addWidget(R4);
    Registers->addWidget(R5);
    Registers->addWidget(R6);
    Registers->addWidget(R7);
    Registers->addWidget(R8);
    Registers->addWidget(R9);
    Registers->addWidget(R10);
    Registers->addWidget(R11);
    Registers->addWidget(R12);
    Registers->addWidget(R13);
    Registers->addWidget(R14);
    Registers->addWidget(R15);
    layout->addLayout(Registers);
    ALU=new QPushButton("ALU");
    layout->addWidget(ALU);
    Mem0=new QPushButton("0");
    Mem1=new QPushButton("1");
    Mem2=new QPushButton("2");
    Mem3=new QPushButton("3");
    Mem4=new QPushButton("4");
    Mem5=new QPushButton("5");
    Mem6=new QPushButton("6");
    Mem7=new QPushButton("7");
    Mem8=new QPushButton("8");
    Mem9=new QPushButton("9");
    Mem10=new QPushButton("10");
    Mem11=new QPushButton("11");
    Mem12=new QPushButton("12");
    Mem13=new QPushButton("13");
    Mem14=new QPushButton("14");
    Mem15=new QPushButton("15");
    Mem16=new QPushButton("16");
    Mem17=new QPushButton("17");
    Mem18=new QPushButton("18");
    Mem19=new QPushButton("19");
    //meory
    Memory=new QVBoxLayout;
    Memory->addWidget(Mem0);
    Memory->addWidget(Mem1);
    Memory->addWidget(Mem2);
    Memory->addWidget(Mem3);
    Memory->addWidget(Mem4);
    Memory->addWidget(Mem5);
    Memory->addWidget(Mem6);
    Memory->addWidget(Mem7);
    Memory->addWidget(Mem8);
    Memory->addWidget(Mem9);
    Memory->addWidget(Mem10);
    Memory->addWidget(Mem11);
    Memory->addWidget(Mem12);
    Memory->addWidget(Mem13);
    Memory->addWidget(Mem14);
    Memory->addWidget(Mem15);
    Memory->addWidget(Mem16);
    Memory->addWidget(Mem17);
    Memory->addWidget(Mem18);
    Memory->addWidget(Mem19);
    layout->addLayout(Memory);
    MainLayout->addLayout(layout);
    setLayout(MainLayout);
}
void newwindow::ReloadFile()
{

    QString filter=" All File (*.*) ;; text File (*.txt) ;; Machincode File (*.mc)";
    QString Filename=QFileDialog::getOpenFileName(this,"Open a File","C://",filter);
    QMessageBox::information(this,"..",Filename);
    QFile file(Filename);
    if(!file.open(QFile::ReadOnly |QFile::Text))
    {
        QMessageBox::warning(this,"title","file not open");
    }
    QRandomGenerator64 random,rand;randomm[0]=0;
    for(int i=1;i<16;i++)
    {
        QString x=(QString::number(random.generate()%16,10));
        randomm[i]=x.toInt();
        if(i==1)
            R1->setText("Register1 ="+x);
        if(i==2)
            R2->setText("Register2 ="+x);
        if(i==3)
            R3->setText("Register3 ="+x);
        if(i==4)
            R4->setText("Register4 ="+x);
        if(i==5)
            R5->setText("Register5 ="+x);
        if(i==6)
            R6->setText("Register6 ="+x);
        if(i==7)
            R7->setText("Register7 ="+x);
        if(i==8)
            R8->setText("Register8 ="+x);
        if(i==9)
            R9->setText("Register9 ="+x);
        if(i==10)
            R10->setText("Register10 ="+x);
        if(i==11)
            R11->setText("Register11 ="+x);
        if(i==12)
            R12->setText("Register12 ="+x);
        if(i==13)
            R13->setText("Register13 ="+x);
        if(i==14)
            R14->setText("Register14 ="+x);
        if(i==15)
            R15->setText("Register15 ="+x);
    }
    for(int i=0;i<20;i++)
    {
        QString x=(QString::number(random.generate()%20,10));
        memory[i]=x.toInt();
        if(i==0)
            Mem0->setText("Memory0 ="+x);
        if(i==1)
            Mem1->setText("Memory1 ="+x);
        if(i==2)
            Mem2->setText("Memory2 ="+x);
        if(i==3)
            Mem3->setText("Memory3 ="+x);
        if(i==4)
            Mem4->setText("Memory4 ="+x);
        if(i==5)
            Mem5->setText("Memory5 ="+x);
        if(i==6)
            Mem6->setText("Memory6 ="+x);
        if(i==7)
            Mem7->setText("Memory7 ="+x);
        if(i==8)
            Mem8->setText("Memory8 ="+x);
        if(i==9)
            Mem9->setText("Memory9 ="+x);
        if(i==10)
            Mem10->setText("Memory10 ="+x);
        if(i==11)
            Mem11->setText("Memory11 ="+x);
        if(i==12)
            Mem12->setText("Memory12 ="+x);
        if(i==13)
            Mem13->setText("Memory13 ="+x);
        if(i==14)
            Mem14->setText("Memory14 ="+x);
        if(i==15)
            Mem15->setText("Memory15 ="+x);
        if(i==16)
            Mem16->setText("Memory16 ="+x);
        if(i==17)
            Mem17->setText("Memory17 ="+x);
        if(i==18)
            Mem18->setText("Memory18 ="+x);
        if(i==19)
            Mem19->setText("Memory19 ="+x);
    }
    QTextStream in(&file);int PC=0,k=0;
    while (!in.atEnd())
    {
        QString line = in.readLine();
        inst[k].instruction=line;
        inst[k].PC=PC;
        for(int j=0;j<5;j++)
            inst[k].Step[j]=0;
        inst[k].Use=0;
        PC++;k++;
    }
    connect(actionf,SIGNAL(triggered()),this,SLOT(run()));
}
void newwindow::run()
{
    int temp,answer; bool taken=false;
    for(int i=0;i<11;i++)
    {
        temp=i;
        if(taken)
        {
            i=inst[i-1].PC+1+inst[i-1].imm;
            if(inst[i].OPcode=="1011")
            {
                taken=false;
                temp=i;
            }
            inst[i].Use=0;inst[i].Step[0]=1;inst[i].Step[1];inst[i].Step[2]=0;inst[i].Step[3]=0;inst[i].Step[4]=0;
        }
        if(inst[i].Use==0)
        {
            if(inst[i].Step[0]==0)
            {
                /*fetch*/
                if(inst[i].instruction.toInt()<65535)
                {
                    QMessageBox::warning(this,"title","Not Instruction"); inst[i].Use=1;
                    continue;
                }
                ppc->setText("PC= "+QString::number(inst[i].PC));
                ins->setText(inst[i].instruction);inst[i].Step[0]=1;
                break;
            }
            if(inst[i].Step[1]==0)
            {
                /*decode*/
                char * x=bin(inst[i].instruction.toInt());
                QString OPcode,Rs,Rd,Rt,imm,offset;
                OPcode.push_back(x[27]);
                OPcode.push_back(x[26]);
                OPcode.push_back(x[25]);
                OPcode.push_back(x[24]);
                inst[i].OPcode=OPcode;
                if(OPcode=="0000")
                {
                    Opcode->setText("OPcode= 0000,(Add)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs= GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt= GETInsInDecimal4(Rt);
                    Rd.push_back(x[15]);
                    Rt.push_back(x[14]);
                    Rt.push_back(x[13]);
                    Rt.push_back(x[12]);
                    inst[i].rd= GETInsInDecimal4(Rd);
                    inst[i].rd=Rd.toInt();
                    RS->setText("RS="+Rs);
                    RD->setText("RD="+Rd);
                    RT->setText("RT"+Rt);inst[i].imm=0;
                    Imm->setText("IMM=0");inst[i].Step[1]=1;break;
                }
                else if(OPcode=="0001")
                {
                    Opcode->setText("OPcode =0001,(Sub)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs= GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt= GETInsInDecimal4(Rt);
                    Rd.push_back(x[15]);
                    Rd.push_back(x[14]);
                    Rd.push_back(x[13]);
                    Rd.push_back(x[12]);
                    inst[i].rd= GETInsInDecimal4(Rd);
                    RS->setText("RS="+Rs);RD->setText("RD="+Rd); Imm->setText("IMM=0");
                    RT->setText("RT="+Rt);inst[i].imm=0;
                    inst[i].Step[1]=1;break;
                }
                else if(OPcode=="0010")
                {
                    Opcode->setText("OPcode =0010,(Slt)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs= GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt= GETInsInDecimal4(Rt);
                    Rd.push_back(x[15]);
                    Rt.push_back(x[14]);
                    Rt.push_back(x[13]);
                    Rt.push_back(x[12]);
                    inst[i].rd= GETInsInDecimal4(Rd);
                    RS->setText("RS="+Rs);
                    RD->setText("RD="+Rd);
                    RT->setText("RT="+Rt);
                    Imm->setText("IMM=0");inst[i].imm=0;
                    inst[i].Step[1]=1;break;
                }
                else if(OPcode=="0011")
                {
                    Opcode->setText("Opcode= 0011,(Or)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs= GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt= GETInsInDecimal4(Rt);
                    Rd.push_back(x[15]);
                    Rt.push_back(x[14]);
                    Rt.push_back(x[13]);
                    Rt.push_back(x[12]);
                    inst[i].rd=GETInsInDecimal4(Rd);
                    RS->setText("RS="+Rs);
                    RD->setText("RD="+Rd);
                    RT->setText("RT="+Rt);
                    Imm->setText("IMM=0");inst[i].imm=0;
                    inst[i].Step[1]=1;break;
                }
                else if(OPcode=="0100")
                {
                    Opcode->setText("Opcode= 0100,(Nand)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs=GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt=GETInsInDecimal4(Rt);
                    Rd.push_back(x[15]);
                    Rt.push_back(x[14]);
                    Rt.push_back(x[13]);
                    Rt.push_back(x[12]);
                    inst[i].rd=GETInsInDecimal4(Rd);
                    RS->setText("RS="+Rs);
                    RD->setText("RD="+Rd);
                    RT->setText("RT"+Rt);
                    Imm->setText("IMM=0");inst[i].imm=0;
                    inst[i].Step[1]=1;break;
                }
                else if (OPcode=="0101")
                {
                    Opcode->setText("OPcode =0101,(AddI)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs=GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt=GETInsInDecimal4(Rt);
                    RS->setText("RS="+Rs);
                    RT->setText("RT="+Rt);
                    for(int counter=15;counter>=0;counter--)
                    {
                        imm.push_back(x[counter]);
                    }
                    if(imm[0]=='1')
                    {
                        for(int m=0;m<16;m++)
                            imm.push_front('1');
                    }
                    else
                        for(int m=0;m<16;m++)
                            imm.push_front('0');
                    Imm->setText("Imm="+imm);
                    inst[i].imm=GETInsInDecimal32(imm);inst[i].rd=0;
                    RD->setText("Rd=0");
                    inst[i].Step[1]=1;
                    break;
                }
                else if (OPcode=="0110")
                {
                    Opcode->setText("OPcode= 0110,(Slti)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs=GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt=GETInsInDecimal4(Rt);
                    for(int counter=15;counter>=0;counter--)
                    {
                        imm.push_back(x[counter]);
                    }
                    if(imm[0]=='1')
                    {
                        for(int i=0;i<16;i++)
                            imm.push_front('1');
                    }
                    else
                        for(int m=0;m<16;m++)
                            imm.push_front('0');
                    Imm->setText("Imm="+imm);
                    inst[i].imm=GETInsInDecimal32(imm);inst[i].rd=0;
                    RS->setText("RS="+Rs);
                    RT->setText("RT="+Rt);
                    RD->setText("Rd=0");inst[i].Step[1]=1;break;
                }
                else if (OPcode=="0111")
                {
                    Opcode->setText("OPcode= 0111,(Ori)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs=GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt=GETInsInDecimal4(Rt);
                    for(int counter=15;counter>=0;counter--)
                    {
                        imm.push_back(x[counter]);
                    }
                    if(imm[0]=='1')
                    {
                        for(int i=0;i<16;i++)
                            imm.push_front('1');
                    }
                    else
                        for(int m=0;m<16;m++)
                            imm.push_front('0');
                    Imm->setText("Imm="+imm);
                    inst[i].imm=GETInsInDecimal32(imm);
                    RS->setText("RS="+Rs);
                    RT->setText("RT="+Rt);inst[i].rd=0;
                    RD->setText("Rd=0");inst[i].Step[1]=1;break;
                }
                else if (OPcode=="1000")
                {
                    Opcode->setText("OPcode= 1000,(Lui)");
                    inst[i].rs=0;
                    RS->setText("RS=0");
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt=GETInsInDecimal4(Rt);
                    for(int counter=15;counter>=0;counter--)
                    {
                        imm.push_back(x[counter]);
                    }
                    Imm->setText("Imm="+imm);
                    inst[i].imm=GETInsInDecimal16(imm);
                    RD->setText("RD=0");
                    RS->setText("RS=0");
                    RT->setText("RT="+Rt);inst[i].rd=0;inst[i].rs=0;
                    inst[i].Step[1]=1;break;
                }
                else if (OPcode=="1001")
                {
                    Opcode->setText("OPcode= 1001,(Lw)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs=GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt=GETInsInDecimal4(Rt);
                    for(int counter=15;counter>=0;counter--)
                    {
                        imm.push_back(x[counter]);
                    }
                    if(imm[0]=='1')
                    {
                        for(int m=0;m<16;m++)
                            imm.push_front('1');
                    }
                    else
                        for(int i=0;i<16;i++)
                            imm.push_front('0');
                    Imm->setText("Imm="+imm);
                    inst[i].imm=GETInsInDecimal32(imm);inst[i].rd=0;
                    RS->setText("RS="+Rs);
                    RD->setText("RD= 0"+Rd);
                    RT->setText("RT="+Rt);
                    inst[i].Step[1]=1;break;
                }
                else if (OPcode=="1010")
                {
                    Opcode->setText("OPcode= 1010,(Sw)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs=GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt=GETInsInDecimal4(Rt);
                    for(int counter=15;counter>=0;counter--)
                    {
                        imm.push_back(x[counter]);
                    }
                    if(imm[0]=='1')
                    {
                        for(int m=0;m<16;m++)
                            imm.push_front('1');
                    }
                    else
                        for(int m=0;m<16;m++)
                            imm.push_front('0');
                    Imm->setText("Imm"+imm);
                    inst[i].imm=GETInsInDecimal32(imm);
                    RS->setText("RS="+Rs);
                    RD->setText("RD="+Rd);inst[i].rd=0;
                    RT->setText("RT="+Rt);
                    inst[i].Step[1]=1;break;
                }
                else if (OPcode=="1011")
                {
                    Opcode->setText("OPcode= 1011,(Beq)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs=GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt=GETInsInDecimal4(Rt);
                    for(int counter=15;counter>=0;counter--)
                    {
                        imm.push_back(x[counter]);
                    }
                    if(imm[0]=='1')
                    {
                        for(int i=0;i<16;i++)
                            imm.push_front('1');
                    }
                    else
                        for(int m=0;m<16;m++)
                            imm.push_front('0');
                    Imm->setText("Imm="+imm);
                    inst[i].imm=GETInsInDecimal32(imm);
                    RS->setText("RS="+Rs);
                    RD->setText("Rd=0");
                    RT->setText("RT="+Rt);inst[i].rd=0;
                    inst[i].Step[1]=1;break;
                }
                else if (OPcode=="1100")
                {
                    Opcode->setText("OPcode= 1100,(Jalr)");
                    Rs.push_back(x[23]);
                    Rs.push_back(x[22]);
                    Rs.push_back(x[21]);
                    Rs.push_back(x[20]);
                    inst[i].rs=GETInsInDecimal4(Rs);
                    Rt.push_back(x[19]);
                    Rt.push_back(x[18]);
                    Rt.push_back(x[17]);
                    Rt.push_back(x[16]);
                    inst[i].rt=GETInsInDecimal4(Rt);
                    RS->setText("RS="+Rs);
                    RD->setText("Rd=0");
                    RT->setText("RT="+Rt);
                    Imm->setText("Imm=0");inst[i].imm=0;inst[i].rd=0;
                    inst[i].Step[1]=1;break;
                }
                else if (OPcode=="1101")
                {
                    Opcode->setText("OPcode= 1101,(J)");
                    for(int counter=15;counter>=0;counter--)
                    {
                        imm.push_back(x[counter]);
                    }
                    for(int m=0;m<16;m++)
                        imm.push_front('0');
                    inst[i].imm=GETInsInDecimal32(imm);
                    RS->setText("RS=0");
                    RD->setText("RD=0");
                    RT->setText("RT=0");
                    Imm->setText("Imm="+imm);inst[i].rd=0;inst[i].rs=0;inst[i].rt=0;
                    inst[i].Step[1]=1;break;
                }
                else if (OPcode=="1110")
                {
                    Opcode->setText("OPcode= 1101,(Halt)");
                    RS->setText("RS=0");
                    RD->setText("RD=0");
                    RT->setText("RT=0");
                    Imm->setText("Imm=0");
                    inst[i].imm=0;inst[i].rd=0;inst[i].rt=0;inst[i].rs=0;
                    inst[i].Step[1]=1;break;
                }
            }
            if(inst[i].Step[2]==0)
            {
                //exe
                if(inst[temp].OPcode=="0000") //add
                {
                    randomm[inst[i].rd]=randomm[inst[i].rt]+randomm[inst[i].rs];
                }
                else if(inst[temp].OPcode=="0000") //sub
                {
                    randomm[inst[temp].rd]=randomm[inst[temp].rs]-randomm[inst[temp].rt];
                }
                else if(inst[temp].OPcode=="0010") // slt
                {
                    if(randomm[inst[i].rs]<randomm[inst[i].rt])
                        randomm[inst[i].rd]=1;
                    else
                        randomm[inst[i].rd]=0;
                }
                else if (inst[i].OPcode=="0011") //or
                {
                    randomm[inst[i].rd]=randomm[inst[i].rt]|randomm[inst[i].rs];
                }
                else if (inst[i].OPcode=="0100") //and
                {
                    randomm[inst[i].rd]=randomm[inst[i].rt]&randomm[inst[i].rs];
                }
                else if (inst[i].OPcode=="0101") //addi
                {
                    randomm[inst[i].rt]=inst[i].imm+randomm[inst[i].rs];
                }
                else if (inst[i].OPcode=="0110") //slti
                {
                    if(randomm[inst[i].rs]<inst[i].imm)
                        randomm[inst[i].rt]=1;
                    else
                        randomm[inst[i].rt]=0;
                }
                else if (inst[i].OPcode=="0111") //ori
                {
                    randomm[inst[i].rt]=inst[i].imm|randomm[inst[i].rs];
                }
                else if (inst[i].OPcode=="1000") //lui
                {
                    randomm[inst[i].rt]=inst[i].imm<<16;
                }
                else if (inst[i].OPcode=="1001") //lw
                {
                    randomm[inst[i].rt]=inst[i].imm+randomm[inst[i].rs];
                }
                else if (inst[i].OPcode=="1011")//beq
                {
                    if(randomm[inst[i].rs]==randomm[inst[i].rt])
                    {
                        taken=true;
                        temp=i;
                    }
                }
                else if (inst[i].OPcode=="1100")//jalr
                {
                    randomm[inst[i].rt]=inst[i].PC+1;
                    inst[i].PC= randomm[inst[i].rs];
                }
                else if (inst[i].OPcode=="1101") //j
                {
                    inst[i].PC= inst[i].imm;
                }
                else if (inst[i].OPcode=="1110")
                {
                    QMessageBox::warning(this,"title","Instruction Halt is Enterd,Finish");
                    this->exit();
                }
                inst[i].Step[2]=1;break;
            }
            if(inst[i].Step[3]==0)
            {
                //mem
                if(inst[i].OPcode=="1001")
                {
                    if(randomm[inst[i].rt]==0)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==1)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==2)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==3)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==4)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==5)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==6)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==7)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==8)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==9)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==10)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==11)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==12)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==13)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==14)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==15)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==16)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==17)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==18)
                        answer=memory[randomm[inst[i].rt]];
                    if(randomm[inst[i].rt]==19)
                        answer=memory[randomm[inst[i].rt]];

                    //wb for lw into register
                    if(inst[i].rt==1)
                        R1->setText("Register1 ="+QString::number(answer));
                    if(inst[i].rt==2)
                        R2->setText("Register2 ="+QString::number(answer));
                    if(inst[i].rt==3)
                        R3->setText("Register3 ="+QString::number(answer));
                    if(inst[i].rt==4)
                        R4->setText("Register4 ="+QString::number(answer));
                    if(inst[i].rt==5)
                        R5->setText("Register5 ="+QString::number(answer));
                    if(inst[i].rt==6)
                        R6->setText("Register6 ="+QString::number(answer));
                    if(inst[i].rt==7)
                        R7->setText("Register7 ="+QString::number(answer));
                    if(inst[i].rt==8)
                        R8->setText("Register8 ="+QString::number(answer));
                    if(inst[i].rt==9)
                        R9->setText("Register9 ="+QString::number(answer));
                    if(inst[i].rt==10)
                        R10->setText("Register10 ="+QString::number(answer));
                    if(inst[i].rt==11)
                        R11->setText("Register11 ="+QString::number(answer));
                    if(inst[i].rt==12)
                        R12->setText("Register12 ="+QString::number(answer));
                    if(inst[i].rt==13)
                        R13->setText("Register13 ="+QString::number(answer));
                    if(inst[i].rt==14)
                        R14->setText("Register14 ="+QString::number(answer));
                    if(inst[i].rt==15)
                        R15->setText("Register15 ="+QString::number(answer));
                    inst[i].Step[3]=1;break;
                }
                else if(inst[i].OPcode=="1010")
                {
                    if(inst[i].imm+randomm[inst[i].rs]>19)
                    {
                        QMessageBox::warning(this,"title","Out of Bound in Memory");
                    }
                    else
                    {
                        if(randomm[inst[i].rt]==0)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==1)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==2)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==3)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==4)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==5)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==6)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==7)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==8)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==9)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==10)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==11)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==12)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==13)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==14)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==15)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==16)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==17)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==18)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                        if(randomm[inst[i].rt]==19)
                            memory[inst[i].imm+randomm[inst[i].rs]]=inst[i].rt;
                    }
                    inst[i].Step[3]=1;break;
                }
                else
                {
                    QMessageBox::warning(this,"title","No Need for Memory out of lw & sw");
                }
                inst[i].Step[3]=1;break;
            }
            if(inst[i].Step[4]==0)
            {
                //wb
                QString p;
                if(inst[i].OPcode=="0000"||inst[i].OPcode=="0001"||inst[i].OPcode=="0010"||inst[i].OPcode=="0011"||inst[i].OPcode=="0100")
                {
                    if(inst[temp].rd==1)
                        R1->setText("Register1 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==2)
                        R2->setText("Register2 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==3)
                        R3->setText("Register3 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==4)
                        R4->setText("Register4 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==5)
                        R5->setText("Register5 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==6)
                        R6->setText("Register6 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==7)
                        R7->setText("Register7 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==8)
                        R8->setText("Register8 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==9)
                        R9->setText("Register9 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==10)
                        R10->setText("Register10 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==11)
                        R11->setText("Register11 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==12)
                        R12->setText("Register12 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==13)
                        R13->setText("Register13 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[temp].rd==14)
                        R14->setText("Register14 ="+p.setNum(randomm[inst[i].rd]));
                    if(inst[i].rd==15)
                        R15->setText("Register15 ="+p.setNum(randomm[inst[i].rd]));
                }
                if(inst[i].OPcode=="0101"||inst[i].OPcode=="0110"||inst[i].OPcode=="0111"||inst[i].OPcode=="1000"||inst[i].OPcode=="1100")
                {
                    if(inst[temp].rt==1)
                        R1->setText("Register1 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==2)
                        R2->setText("Register2 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==3)
                        R3->setText("Register3 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==4)
                        R4->setText("Register4 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==5)
                        R5->setText("Register5 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==6)
                        R6->setText("Register6 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==7)
                        R7->setText("Register7 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==8)
                        R8->setText("Register8 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==9)
                        R9->setText("Register9 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==10)
                        R10->setText("Register10 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==11)
                        R11->setText("Register11 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==12)
                        R12->setText("Register12 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==13)
                        R13->setText("Register13 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==14)
                        R14->setText("Register14 ="+QString::number(randomm[inst[i].rt]));
                    if(inst[temp].rt==15)
                        R15->setText("Register15 ="+QString::number(randomm[inst[i].rt]));
                }
                inst[i].Step[4]=1;break;
            }
            inst[i].Use=1;
        }
    }
}
void newwindow::exit()
{
    this->close();
}
