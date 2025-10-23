/***<REFAH>***/
#include<iostream>
#include<windows.h>
#include<fstream>
#include<string>
using namespace std;
void setcolor(int colorcode);
#pragma warning (disable:4700)
#pragma warning (disable:26495)
#pragma warning (disable:6001)
#pragma warning (disable:6281)
int Size = 0;
ofstream fileout("fileout.txt", ios::trunc);
struct Persons
{
	string First_name;
	string Last_name;
	char* Melli_code;
	string Birth;
	double Income;
	int16_t Working_hours;
	int32_t Cost_working_hours;
	int Hard_work;
};
struct Boss
{
	Persons X;
	string Name_Of_Organization;
	int64_t Access_Level;
	long Number_Of_People;
	double Reward;
};
struct Supervisor
{
	Persons Y;
	string Name_Of_Department;
	int64_t Access_Level;
	long Number_Of_People;
	double Reward;
};
struct Employee
{
	Persons Z;
	int64_t Personnel_Number;
	double Service_Deficit_Cost;
	int  Number_Of_Family_Members;
};
struct Node
{
	struct Boss A;
	struct Supervisor B;
	struct Employee C;
	bool check1 = false; bool check2 = false; bool check3 = false;
	Node* Next = NULL;
	Node* Prevous = NULL;
};
Node* head, * tail;
void show1()
{
	cout << endl; setcolor(13);
	cout << "1-"; setcolor(4); cout << "First Name"; cout << endl; setcolor(13);
	cout << "2-"; setcolor(4); cout << "Last Name"; cout << endl; setcolor(13);
	cout << "3-"; setcolor(4); cout << "Melli Code"; cout << endl; setcolor(13);
	cout << "4-"; setcolor(4); cout << "Birth"; cout << endl; setcolor(13);
	cout << "5-"; setcolor(4); cout << "Income"; cout << endl; setcolor(13);
	cout << "6-"; setcolor(4); cout << "Working_hours"; cout << endl; setcolor(13);
	cout << "7-"; setcolor(4); cout << "Cost_working_hours"; cout << endl; setcolor(13);
	cout << "8"; setcolor(4); cout << "Reward" << endl;
}
void show()
{
	cout << endl; setcolor(13);
	cout << "1-"; setcolor(4); cout << "Show menu"; cout << endl; setcolor(13);
	cout << "2-"; setcolor(4); cout << "Add new person"; cout << endl; setcolor(13);
	cout << "3-"; setcolor(4); cout << "show menu"; cout << endl; setcolor(13);
	cout << "4-"; setcolor(4); cout << "Delete new person"; cout << endl; setcolor(13);
	cout << "5-"; setcolor(4); cout << "Show new person"; cout << endl; setcolor(13);
	cout << "6-"; setcolor(4); cout << "Show income of new person"; cout << endl; setcolor(13);
	cout << "7-"; setcolor(4); cout << "Exit" << endl;
}
void push(string name)
{
	Node* temp = new Node();
	if (name == "Boss")
	{
		setcolor(12); cout << " Enter string For First Name" << endl;
		cin >> temp->A.X.First_name;
		fileout << temp->A.X.First_name << endl;
		setcolor(12); cout << "Enter string For Last Name" << endl;
		cin >> temp->A.X.Last_name;
		fileout << temp->A.X.Last_name << endl;
		setcolor(12); cout << "Enter string For Melli code" << endl;
		cin >> (cin, temp->A.X.Melli_code);
		fileout << temp->A.X.Melli_code << endl;
		setcolor(12); cout << "Enter string For Birth" << endl;
		cin >> temp->A.X.Birth;
		fileout << temp->A.X.Birth << endl;
		setcolor(12); cout << "Enter number For Income" << endl;
		cin >> temp->A.X.Income;
		fileout << temp->A.X.Income << endl;
		setcolor(12); cout << " Enter number For Working hours" << endl;
		cin >> temp->A.X.Working_hours;
		fileout << temp->A.X.Working_hours << endl;
		setcolor(12); cout << "Enter number For Cost Working hours" << endl;
		cin >> temp->A.X.Cost_working_hours;
		fileout << temp->A.X.Cost_working_hours << endl;
		setcolor(12); cout << "Enter number For Hard work" << endl;
		cin >> temp->A.X.Hard_work;
		fileout << temp->A.X.Hard_work << endl;
		setcolor(12); cout << "Enter string  For Name of Organization" << endl;
		cin >> temp->A.Name_Of_Organization;
		fileout << temp->A.Name_Of_Organization << endl;
		setcolor(12); cout << "Enter number For Access Level" << endl;
		cin >> temp->A.Access_Level;
		fileout << temp->A.Access_Level << endl;
		setcolor(12); cout << "Enter number For Number Of people" << endl;
		cin >> temp->A.Number_Of_People;
		fileout << temp->A.Number_Of_People << endl;
		setcolor(12); cout << "Enter number For Reward" << endl;
		cin >> temp->A.Reward;
		fileout << temp->A.Reward << endl;
		if (Size == 0)
		{
			head = temp;
			tail = temp;
		}
		else
		{
			temp->Next = NULL;
			temp->Prevous = tail;
			tail = tail->Next;
		}
		setcolor(10); cout << "New person succesfully Added" << endl;
		Size++;
		temp->check1 = true;
	}
	else if (name == "Supervisor")
	{
		setcolor(12); cout << " Enter string For First Name" << endl;
		cin >> temp->B.Y.First_name;
		fileout << temp->B.Y.First_name << endl;
		setcolor(12); cout << "Enter string For Last Name" << endl;
		cin >> temp->B.Y.Last_name;
		fileout << temp->B.Y.Last_name << endl;
		setcolor(12); cout << "Enter string For Melli code" << endl;
		cin >> (cin, temp->B.Y.Melli_code);
		fileout << temp->B.Y.Melli_code << endl;
		setcolor(12); cout << "Enter string For Birth" << endl;
		cin >> temp->B.Y.Birth;
		fileout << temp->B.Y.Birth << endl;
		setcolor(12); cout << "Enter number For Income" << endl;
		cin >> temp->B.Y.Income;
		fileout << temp->B.Y.Income << endl;
		setcolor(12); cout << " Enter number For Working hours" << endl;
		cin >> temp->B.Y.Working_hours;
		fileout << temp->B.Y.Working_hours << endl;
		setcolor(12); cout << "Enter number For Cost Working hours" << endl;
		cin >> temp->B.Y.Cost_working_hours;
		fileout << temp->B.Y.Cost_working_hours << endl;
		setcolor(12); cout << "Enter number For Hard work" << endl;
		cin >> temp->B.Y.Hard_work;
		fileout << temp->B.Y.Hard_work << endl;
		setcolor(12); cout << "Enter string  For Name of Department" << endl;
		cin >> temp->B.Name_Of_Department;
		fileout << temp->B.Name_Of_Department << endl;
		setcolor(12); cout << "Enter number For Access Level" << endl;
		cin >> temp->B.Access_Level;
		fileout << temp->B.Access_Level << endl;
		setcolor(12); cout << "Enter number For Number Of people" << endl;
		cin >> temp->B.Number_Of_People;
		fileout << temp->B.Number_Of_People << endl;
		setcolor(12); cout << "Enter number For Reward" << endl;
		cin >> temp->B.Reward;
		fileout << temp->B.Reward << endl;
		if (Size == 0)
		{
			head = temp;
			tail = temp;
		}
		else
		{
			temp->Next = NULL;
			temp->Prevous = tail;
			tail = tail->Next;
		}
		setcolor(10); cout << "New person succesfully Added" << endl;
		Size++;
		temp->check2 = true;
	}
	else if (name == "Employee")
	{
		setcolor(12); cout << " Enter string For First Name" << endl;
		cin >> temp->C.Z.First_name;
		fileout << temp->C.Z.First_name << endl;
		setcolor(12); cout << "Enter string For Last Name" << endl;
		cin >> temp->C.Z.Last_name;
		fileout << temp->C.Z.Last_name << endl;
		setcolor(12); cout << "Enter string For Melli code" << endl;
		cin >> temp->C.Z.Melli_code;
		fileout << temp->C.Z.Melli_code << endl;
		setcolor(12); cout << "Enter string For Birth" << endl;
		cin >> temp->C.Z.Birth;
		fileout << temp->C.Z.Birth << endl;
		setcolor(12); cout << "Enter number For Income" << endl;
		cin >> temp->C.Z.Income;
		fileout << temp->C.Z.Income << endl;
		setcolor(12); cout << " Enter number For Working hours" << endl;
		cin >> temp->C.Z.Working_hours;
		fileout << temp->C.Z.Working_hours << endl;
		setcolor(12); cout << "Enter number For Cost Working hours" << endl;
		cin >> temp->C.Z.Cost_working_hours;
		fileout << temp->C.Z.Cost_working_hours << endl;
		setcolor(12); cout << "Enter number For Hard work" << endl;
		cin >> temp->C.Z.Hard_work;
		fileout << temp->C.Z.Hard_work << endl;
		setcolor(12); cout << "Enter number For Personal Number" << endl;
		cin >> temp->C.Personnel_Number;
		fileout << temp->C.Personnel_Number << endl;
		setcolor(12); cout << "Enter number For Service Deficit Cost" << endl;
		cin >> temp->C.Service_Deficit_Cost;
		fileout << temp->C.Service_Deficit_Cost << endl;
		setcolor(12); cout << "Enter number For Number Of Family Members" << endl;
		cin >> temp->C.Number_Of_Family_Members;
		fileout << temp->C.Number_Of_Family_Members << endl;
		if (Size == 0)
		{
			head = temp;
			tail = temp;
		}
		else
		{
			temp->Next = NULL;
			temp->Prevous = tail;
			tail = tail->Next;
		}
		setcolor(10); cout << "New person succesfully Added" << endl;
		Size++;
		temp->check3 = true;
	}
}
void Edit(string name)
{
	string changepart;
	Node* temp1; Node* tmp = head;
	if (name == "Boss")
	{
		while (tmp)
		{
			if (tmp->check1)
			{
				setcolor(1); cout << "To Edit information Of Boss You Want:" << endl;
				setcolor(12); cout << " Enter string For First Name" << endl; cin >> temp1->A.X.First_name;
				setcolor(12); cout << "Enter string For Last Name" << endl; cin >> temp1->A.X.Last_name;
				setcolor(12); cout << "Enter string For Melli code" << endl; cin >> (cin, temp1->A.X.Melli_code);
				setcolor(12); cout << "Enter string For Birth" << endl; cin >> temp1->A.X.Birth;
				setcolor(12); cout << "Enter number For Income" << endl; cin >> temp1->A.X.Income;
				setcolor(12); cout << " Enter number For Working hours" << endl; cin >> temp1->A.X.Working_hours;
				setcolor(12); cout << "Enter number For Cost Working hours" << endl; cin >> temp1->A.X.Cost_working_hours;
				setcolor(12); cout << "Enter number For Hard work" << endl; cin >> temp1->A.X.Hard_work;
				setcolor(12); cout << "Enter string  For Name of Organization" << endl; cin >> temp1->A.Name_Of_Organization;
				setcolor(12); cout << "Enter number For Access Level" << endl; cin >> temp1->A.Access_Level;
				setcolor(12); cout << "Enter number For Number Of people" << endl; cin >> temp1->A.Number_Of_People; setcolor(12); cout << "Enter number For Reward" << endl;
				cin >> temp1->A.Reward;
				if (tmp->A.X.First_name == temp1->A.X.First_name && tmp->A.X.Last_name == temp1->A.X.Last_name && strcmp(tmp->A.X.Melli_code, temp1->A.X.Melli_code) == 0 &&
					tmp->A.X.Birth == temp1->A.X.Birth && tmp->A.X.Income == temp1->A.X.Income && tmp->A.X.Cost_working_hours == temp1->A.X.Cost_working_hours &&
					tmp->A.X.Hard_work == temp1->A.X.Hard_work && tmp->A.X.Working_hours == temp1->A.X.Working_hours)
				{
					setcolor(2); cout << "User found Succesfuly" << endl;
					while (true)
					{
						string s; int number; int j;
						setcolor(5); cout << "Enter your number You Want To Edit" << endl;
						show1();
						getline(cin, changepart);
						if (changepart == "1")
						{
							getline(cin, s); tmp->A.X.First_name = s; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "2")
						{
							getline(cin, s); tmp->A.X.Last_name = s; setcolor(9);
							cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "3")
						{
							getline(cin, s); tmp->A.X.Birth = s; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "4")
						{
							cin >> j; tmp->A.X.Working_hours = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "5")
						{
							cin >> j; tmp->A.X.Cost_working_hours = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl;	cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "6")
						{
							cin >> j; tmp->A.X.Hard_work = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "7")
						{
							tmp->A.X.Income = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						if (changepart == "8")
						{
							getline(cin, s); tmp->A.Name_Of_Organization = s; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						if (changepart == "9")
						{
							tmp->A.Number_Of_People = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						if (changepart == "10")
						{
							cin >> j; tmp->A.Access_Level = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						if (changepart == "11")
						{
							cin >> j; tmp->A.Reward = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
					}
				}
			}
			tmp = tmp->Next;
		}
	}
	else if (name == "Supervisor")
	{
		while (tmp)
		{
			if (tmp->check2)
			{
				setcolor(1); cout << "To Edit information Of Boss You Want:" << endl;
				setcolor(12); cout << " Enter string For First Name" << endl; cin >> temp1->B.Y.First_name;
				setcolor(12); cout << "Enter string For Last Name" << endl; cin >> temp1->B.Y.Last_name;
				setcolor(12); cout << "Enter string For Melli code" << endl; cin >> temp1->B.Y.Melli_code;
				setcolor(12); cout << "Enter string For Birth" << endl; cin >> temp1->B.Y.Birth;
				setcolor(12); cout << "Enter number For Income" << endl; cin >> temp1->B.Y.Income;
				setcolor(12); cout << " Enter number For Working hours" << endl; cin >> temp1->B.Y.Working_hours;
				setcolor(12); cout << "Enter number For Cost Working hours" << endl; cin >> temp1->B.Y.Cost_working_hours;
				setcolor(12); cout << "Enter number For Hard work" << endl; cin >> temp1->B.Y.Hard_work;
				setcolor(12); cout << "Enter string  For Name of Organization" << endl; cin >> temp1->B.Name_Of_Department;
				setcolor(12); cout << "Enter number For Access Level" << endl; cin >> temp1->B.Access_Level;
				setcolor(12); cout << "Enter number For Number Of people" << endl; cin >> temp1->B.Number_Of_People; setcolor(12); cout << "Enter number For Reward" << endl;
				cin >> temp1->B.Reward;
				if (tmp->B.Y.First_name == temp1->B.Y.First_name && tmp->B.Y.Last_name == temp1->B.Y.Last_name && strcmp(tmp->B.Y.Melli_code, temp1->B.Y.Melli_code) == 0 &&
					tmp->B.Y.Birth == temp1->B.Y.Birth && tmp->B.Y.Income == temp1->B.Y.Income && tmp->B.Y.Cost_working_hours == temp1->B.Y.Cost_working_hours &&
					tmp->B.Y.Hard_work == temp1->B.Y.Hard_work && tmp->B.Y.Working_hours == temp1->B.Y.Working_hours)
				{
					setcolor(2); cout << "User found Succesfuly" << endl;
					while (true)
					{
						string s; int number; int j;
						setcolor(5); cout << "Enter your number You Want To Edit" << endl;
						show1(); getline(cin, changepart);
						if (changepart == "1")
						{
							getline(cin, s); tmp->B.Y.First_name = s; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "2")
						{
							getline(cin, s); tmp->B.Y.Last_name = s; setcolor(9);
							cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "3")
						{
							getline(cin, s); tmp->B.Y.Birth = s; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "4")
						{
							cin >> j; tmp->B.Y.Working_hours = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "5")
						{
							cin >> j; tmp->B.Y.Cost_working_hours = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl;	cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "6")
						{
							cin >> j; tmp->B.Y.Hard_work = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "7")
						{
							tmp->B.Y.Income = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "8")
						{
							getline(cin, s); tmp->B.Name_Of_Department = s; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "9")
						{
							tmp->B.Number_Of_People = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "10")
						{
							cin >> j; tmp->B.Access_Level = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "11")
						{
							cin >> j; tmp->B.Reward = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
					}
				}
			}
			tmp = tmp->Next;
		}
	}
	else if (name == "Employee")
	{
		while (tmp)
		{
			if (tmp->check3)
			{
				setcolor(1); cout << "To Edit information Of Boss You Want:" << endl;
				setcolor(12); cout << " Enter string For First Name" << endl; cin >> temp1->C.Z.First_name;
				setcolor(12); cout << "Enter string For Last Name" << endl; cin >> temp1->C.Z.Last_name;
				setcolor(12); cout << "Enter string For Melli code" << endl; cin >> temp1->C.Z.Melli_code;
				setcolor(12); cout << "Enter string For Birth" << endl; cin >> temp1->C.Z.Birth;
				setcolor(12); cout << "Enter number For Income" << endl; cin >> temp1->C.Z.Income;
				setcolor(12); cout << " Enter number For Working hours" << endl; cin >> temp1->C.Z.Working_hours;
				setcolor(12); cout << "Enter number For Cost Working hours" << endl; cin >> temp1->C.Z.Cost_working_hours;
				setcolor(12); cout << "Enter number For Hard work" << endl; cin >> temp1->C.Z.Hard_work;
				setcolor(12); cout << "Enter string  For Name of Members" << endl; cin >> temp1->C.Number_Of_Family_Members;
				setcolor(12); cout << "Enter number For PERSONAL nUMBER" << endl; cin >> temp1->C.Personnel_Number;
				setcolor(12); cout << "Enter number For Service" << endl; cin >> temp1->C.Service_Deficit_Cost;
				if (tmp->C.Z.First_name == temp1->C.Z.First_name && tmp->C.Z.Last_name == temp1->C.Z.Last_name && strcmp(tmp->C.Z.Melli_code, temp1->C.Z.Melli_code) == 0 &&
					tmp->C.Z.Birth == temp1->C.Z.Birth && tmp->C.Z.Income == temp1->C.Z.Income && tmp->C.Z.Cost_working_hours == temp1->C.Z.Cost_working_hours &&
					tmp->C.Z.Hard_work == temp1->C.Z.Hard_work && tmp->C.Z.Working_hours == temp1->C.Z.Working_hours)
				{
					setcolor(2); cout << "User found Succesfuly" << endl;
					while (true)
					{
						string s; int number; int j; setcolor(5); cout << "Enter your number You Want To Edit" << endl; show1(); getline(cin, changepart);
						if (changepart == "1")
						{
							getline(cin, s); tmp->C.Z.First_name = s; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "2")
						{
							getline(cin, s); tmp->C.Z.Last_name = s; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "3")
						{
							getline(cin, s); tmp->C.Z.Birth = s; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "4")
						{
							cin >> j; tmp->C.Z.Working_hours = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "5")
						{
							cin >> j; tmp->C.Z.Cost_working_hours = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl;	cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "6")
						{
							cin >> j; tmp->C.Z.Hard_work = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "7")
						{
							tmp->C.Z.Income = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "8")
						{
							cin >> j; tmp->C.Number_Of_Family_Members = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "9")
						{
							tmp->C.Personnel_Number = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
						else if (changepart == "10")
						{
							cin >> j; tmp->C.Service_Deficit_Cost = j; setcolor(9); cout << "continue or break choose 1(continue) or 2(break):" << endl; cin >> number;
							if (1 == number)
								continue;
							else if (number == 2)
								break;
						}
					}
				}
			}
			tmp = tmp->Next;
		}
	}
}
void setcolor(int colorcode) {

	HANDLE console = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleTextAttribute(console, colorcode % 255);
}
void Delete(char* melli)
{
	Node* permanent = head;
	while (permanent)
	{
		if (strcmp(permanent->A.X.Melli_code, melli) == 0 | strcmp(permanent->B.Y.Melli_code, melli) == 0 || strcmp(permanent->C.Z.Melli_code, melli) == 0)
		{
			if (permanent == head)
			{
				if (Size == 0)
				{
					head = head->Next;
					tail = NULL;
				}
				else
				{
					head = head->Next;
					head->Prevous = NULL;
					delete(permanent);
				}
			}
			else if (permanent == tail)
			{
				if (Size == 0)
				{
					head = head->Next;
					tail = NULL;
				}
				else
				{
					tail = tail->Prevous;
					tail->Next = NULL;
				}
			}
			else
			{
				permanent->Next->Prevous = permanent->Prevous;
				permanent->Prevous->Next = permanent->Next;
			}
		}
		permanent = permanent->Next;
	}
	Size--;
}
void showinformation(char* melli)
{
	Node* temp = head;
	while (temp)
	{
		if (strcmp(temp->A.X.Melli_code, melli) == 0 || strcmp(temp->B.Y.Melli_code, melli) == 0 || strcmp(temp->C.Z.Melli_code, melli) == 0)
		{
			setcolor(10);
			cout << "User found User information" << endl;
			setcolor(7);
			if ((temp->A.X.Melli_code, melli) == 0)
			{
				cout << temp->A.X.First_name << endl; cout << temp->A.X.Last_name << endl; cout << temp->A.X.Birth << endl; cout << temp->A.X.Cost_working_hours; cout << temp->A.X.Hard_work << endl;
				cout << temp->A.X.Income << endl; cout << temp->A.X.Melli_code << endl; cout << temp->A.X.Working_hours << endl; cout << temp->A.Access_Level << endl; cout << temp->A.Name_Of_Organization << endl; cout << temp->A.Number_Of_People << endl; cout << temp->A.Reward << endl;
			}
			else if (strcmp(temp->B.Y.Melli_code, melli) == 0)
			{
				cout << temp->B.Y.First_name << endl; cout << temp->B.Y.Last_name << endl; cout << temp->B.Y.Birth << endl; cout << temp->B.Y.Cost_working_hours; cout << temp->B.Y.Hard_work << endl;
				cout << temp->B.Y.Income << endl; cout << temp->B.Y.Melli_code << endl; cout << temp->B.Y.Working_hours << endl; cout << temp->B.Access_Level << endl; cout << temp->B.Name_Of_Department << endl; cout << temp->B.Number_Of_People << endl; cout << temp->B.Reward << endl;
			}
			else if (strcmp(temp->C.Z.Melli_code, melli) == 0)
			{
				cout << temp->C.Z.First_name << endl; cout << temp->C.Z.Last_name << endl; cout << temp->C.Z.Birth << endl; cout << temp->C.Z.Cost_working_hours; cout << temp->C.Z.Hard_work << endl;
				cout << temp->C.Z.Income << endl; cout << temp->C.Z.Melli_code << endl; cout << temp->C.Z.Working_hours << endl; cout << temp->C.Number_Of_Family_Members << endl; cout << temp->B.Access_Level << endl; cout << temp->B.Name_Of_Department << endl; cout << temp->B.Number_Of_People << endl; cout << temp->B.Reward << endl;
			}
		}
		temp = temp->Next;
	}
}
void income(string name)
{
	Node* temp = head;
	if (name == "Boss")
	{
		while (temp)
		{
			if (temp->check1)
			{
				double total = (temp->A.Reward * 2) + (temp->A.X.Working_hours * temp->A.X.Cost_working_hours * temp->A.X.Hard_work);
				setcolor(4);
				cout << "income ==" << total << endl;
				temp->A.X.Income = total;
				break;
			}
		}
	}
	else if (name == "supervisor")
	{
		while (temp)
		{
			if (temp->check2)
			{
				double total = (temp->A.Reward) + (temp->A.X.Working_hours * temp->A.X.Cost_working_hours * temp->A.X.Hard_work);
				setcolor(4);
				cout << "income ==" << total << endl;
				temp->B.Y.Income = total;
				break;
			}
		}
	}
	else if (name == "Employee")
	{
		while (temp)
		{
			if (temp->check3)
			{
				double total = (temp->A.X.Working_hours * temp->A.X.Cost_working_hours * temp->A.X.Hard_work) - temp->C.Service_Deficit_Cost;
				setcolor(4);
				cout << "income ==" << total << endl;
				temp->C.Z.Income = total;
				break;
			}
		}
	}
}
int main()
{
	setcolor(9);
	cout << "========================***Welcome_TO_The_Refah_System***===========================" << endl;
	show();
	int comand;
	string temp;
	while (true)
	{
		cin >> comand;
		switch (comand)
		{
		case 1:
			show();
			continue;
		case 2:
			cout << "Enter kind of people" << endl;
			getline(cin, temp);
			push(temp);
			continue;
		case 3:
			cout << "Enter kind of people" << endl;
			getline(cin, temp);
			Edit(temp);
			continue;
		case 4:
			char* array;
			cout << "enter for code melii" << endl;
			cin.get(array, 10);
			Delete(array);
			continue;
		case 5:
			char* arrayname;
			cout << "enter for code melii" << endl;
			cin.get(array, 10);
			showinformation(arrayname);
			continue;
		case 6:
			cout << "Enter kind of people" << endl;
			getline(cin, temp);
			income(temp);
			continue;
		}
	}
	setcolor(6); cout << "Have a good day :)) " << endl;
	return 0;
}