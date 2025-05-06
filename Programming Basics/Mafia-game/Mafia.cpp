#include <iostream> // for all
#include <string> // for good sake
#include <algorithm> // for swap two elements
#include <Windows.h> // for coloring in console
#include <iomanip> // for arrangement in cout print

using namespace std;

int DAY = 1;

// enum class For Roles
enum class Role {
	UNKOWN = 0x0,
	VILLAGER = 0x1,
	WOLFMAN = 0x2,
	KILLER = 0x3,
	FIREMAN = 0x4,
	ANGLE = 0x5,
	LOVE = 0x6,
	FACTION = 0x7,
	HUNTER = 0x8
};

struct Person {
	string name;
	Role role = Role::UNKOWN;
	bool status = true;
	bool is_oily = false;
	string partner;
};

int number_of_people;
struct Person* persons;

/*Run Command only one time*/
bool WOLFMAN = false;
bool KILLER = false;
bool FIREMAN = false;
bool ANGLE = false;
bool LOVE = false;
bool FACTION = false;
bool HUNTER = false;
string error;

/* Defining Functions */
struct Person& find(string);
void print();
int count_role_alive(Role);
void kill(string);
void save(string);
void love(string, string);
void oily(string);
void burn();
void cult(string);
void shoot(string);
void vote();
void setcolor(int);
string role_to_string(Role);
void reset();

int main() {
	srand((unsigned int)time(NULL));
	cin >> number_of_people;
	persons = new Person[number_of_people];

	// Get persons name from stdin
	for (int i = 0; i < number_of_people; i++)
		cin >> persons[i].name;

	// Assign 6 well-known roles to persons using rand() function
	for (int i = 3; i < 9;)
	{
		int index = rand() % number_of_people;
		if (persons[index].role == Role::UNKOWN)
			persons[index].role = (Role)i++;
	}

	// Assign WOLFMAN roles to persons using rand() function
	for (int i = 0; i < (number_of_people - 6) / 4;)
	{
		int index = rand() % number_of_people;
		if (persons[index].role == Role::UNKOWN) {
			persons[index].role = Role::WOLFMAN;
			i++;
		}
	}

	// Assign VILLAGER roles to others using rand() function
	for (int i = 0; i < number_of_people; i++)
		if (persons[i].role == Role::UNKOWN)
			persons[i].role = Role::VILLAGER;

	string command;
	while (_UI64_MAX)
	{
		print();
		cout << endl;
		if (!error.empty()) {
			setcolor(0x4);
			cout << "[-]" << error << endl;
			setcolor(0xF);
		}
		error.clear();

		setcolor(0x3);
		cout << endl << "#Command: ";
		setcolor(0xF);
		cin >> command;
		if (command == "Eat") {
			string name;
			cin >> name;
			if (WOLFMAN) {
				error = "WOLFMAN already has used his power for today";
				continue;
			}
			if (!count_role_alive(Role::WOLFMAN)) {
				error = "No WOLFMAN AVAILABLE";
				continue;
			}
			kill(name);
			WOLFMAN = true;
		}
		else if (command == "Kill") {
			string name;
			cin >> name;
			if (KILLER) {
				error = "KILLER already has used his power for today";
				continue;
			}
			if (!count_role_alive(Role::KILLER)) {
				setcolor(0x4);
				cout << "[-]No KILLER Available" << endl;
				setcolor(0xF);
				continue;
			}
			kill(name);
			KILLER = true;
		}

		else if (command == "Oil") {
			string name;
			cin >> name;
			if (FIREMAN) {
				error = "FIREMAN already has used his power for today";
				continue;
			}
			if (!count_role_alive(Role::FIREMAN)) {
				error = "No FIREMAN Available";
				continue;
			}
			oily(name);
			FIREMAN = true;
		}
		else if (command == "Burn") {
			if (FIREMAN) {
				error = "FIREMAN already has used his power for today";
				continue;
			}
			if (!count_role_alive(Role::FIREMAN)) {
				error = "No FIREMAN Available";
				continue;
			}
			burn();
			FIREMAN = true;
		}

		else if (command == "Love") {
			string name1, name2;
			cin >> name1 >> name2;
			if (LOVE) {
				error = "LOVE ANGLE already has used his power for today";
				continue;
			}
			if (!count_role_alive(Role::LOVE)) {
				error = "No LOVE ANGLE Available";
				continue;
			}
			love(name1, name2);
			LOVE = true;
		}

		else if (command == "Save") {
			string name;
			cin >> name;
			if (ANGLE) {
				error = "GUARDIAN ANGLE already has used his power for today";
				continue;
			}
			if (!count_role_alive(Role::ANGLE)) {
				error = "No GUARDIAN ANGLE Available";
				continue;
			}
			save(name);
			ANGLE = true;
		}

		else if (command == "Shoot") {
			string name;
			cin >> name;
			if (HUNTER) {
				error = "HUNTER already has used his power for today";
				continue;
			}
			if (!count_role_alive(Role::HUNTER)) {
				error = "No HUNTER Available";
				continue;
			}
			shoot(name);
			HUNTER = true;
		}

		else if (command == "Cult") {
			string name;
			cin >> name;
			if (FACTION) {
				error = "FACTION already has used his power for today";
				continue;
			}
			if (!count_role_alive(Role::FACTION)) {
				error = "No FACTION Available";
				continue;
			}
			cult(name);
			FACTION = true;
		}

		else if (command == "Vote") {
			vote();
		}
		else error = "Wrong Command. Try Again";

	}
	return 0;
}

void print() {
	system("cls");
	cout << setw(50) << right << "DAY " << DAY << endl << endl;
	cout.width(20); cout << left << "Name";
	cout.width(20); cout << left << "Role";
	cout.width(20); cout << left << "Status";
	cout.width(20); cout << left << "Is Oily";
	cout.width(20); cout << left << "Partner";
	cout << endl;
	for (size_t i = 0; i < number_of_people; i++)
	{
		persons[i].status ? setcolor(0x2) : setcolor(0x4);
		if (persons[i].is_oily && persons[i].status)
			setcolor(0x6);
		cout.width(20); cout << left << persons[i].name;
		cout.width(20); cout << left << role_to_string(persons[i].role);
		cout.width(20); cout << left << (persons[i].status ? "alive" : "dead");
		cout.width(20); cout << left << (persons[i].is_oily ? "True" : "False");
		cout.width(20); cout << left << (persons[i].partner.empty() ? "-" : persons[i].partner);
		cout << endl;
		setcolor(0xF);
	}
}

Person& find(string name)
{
	for (int i = 0; i < number_of_people; i++)
	{
		if (persons[i].name == name)
			return persons[i];
	}
	error = "invalid name";
}

void kill(string name)
{
	find(name).status = false;
	if (!find(name).partner.empty())
		find(find(name).partner).status = false;
}

void save(string name)
{
	if (find(name).status == false)
		find(name).status = true;
}

void love(string name1, string name2)
{
	find(name1).partner = name2;
	find(name2).partner = name1;
}

void oily(string name)
{
	find(name).is_oily = true;
}

void burn()
{
	for (int i = 0; i < number_of_people; i++)
		if (persons[i].is_oily)
			kill(persons[i].name);
}

void shoot(string name) {
	static int bullet = 2;
	if (bullet > 0) {
		if (find(name).role == Role::FACTION)
			kill(name);
		else error = "shoot missed -- shoot only works on factions";
		bullet--;
	}
	else error = "Sorry no bullet available";
}

void cult(string name)
{
	if (find(name).role == Role::HUNTER)
		error = "Couldn't add HUNTER to FACTION";
	else if (!find(name).status)
		error = "Couldn't add Dead person to FACTION";
	else find(name).role = Role::FACTION;
}

int count_role_alive(Role r)
{
	int temp = 0;
	for (int i = 0; i < number_of_people; i++)
	{
		if (persons[i].role == r && persons[i].status == true)
			temp++;
	}
	return temp;
}

int count_except_role_alive(Role r)
{
	int temp = 0;
	for (int i = 0; i < number_of_people; i++)
	{
		if (persons[i].role != r && persons[i].status == true)
			temp++;
	}
	return temp;
}

int count_alive()
{
	int temp = 0;
	for (int i = 0; i < number_of_people; i++)
	{
		if (persons[i].status)
			temp++;
	}
	return temp;
}

void check_win() {

	if (count_alive() == 0) {
		setcolor(0xA);
		cout << "Game finished without Winner" << endl;
		setcolor(0xF);
		exit(0);
	}

	/*Phase 1: Only Factions are alive then FACTION*/
	if (
		!count_role_alive(Role::ANGLE) &&
		!count_role_alive(Role::FIREMAN) &&
		!count_role_alive(Role::HUNTER) &&
		!count_role_alive(Role::KILLER) &&
		!count_role_alive(Role::LOVE) &&
		!count_role_alive(Role::VILLAGER) &&
		!count_role_alive(Role::WOLFMAN) &&
		count_role_alive(Role::FACTION))
	{
		setcolor(0xA);
		cout << "Factoin Won the Game!" << endl;
		setcolor(0xF);
		exit(0);
	}

	/*Phase 2: WOLFMAN counts == alive persons and no KILLER and no FIREMAN then WOLFMAN*/
	if (
		!count_role_alive(Role::FIREMAN) &&
		!count_role_alive(Role::KILLER) &&
		count_role_alive(Role::WOLFMAN) == count_except_role_alive(Role::WOLFMAN)
		)
	{
		setcolor(0xA);
		cout << "WOLFMAN Won the Game!" << endl;
		setcolor(0xF);
		exit(0);
	}
	/*Phase 3: no KILLER and no FIREMAN and no WOLFMAN then VILLAGER*/
	if (
		!count_role_alive(Role::FIREMAN) &&
		!count_role_alive(Role::KILLER) &&
		!count_role_alive(Role::WOLFMAN) &&
		count_role_alive(Role::VILLAGER))
	{
		setcolor(0xA);
		cout << "VILLAGER Won the Game!" << endl;
		setcolor(0xF);
		exit(0);
	}


}

void check_partner() {
	for (int i = 0; i < number_of_people; i++)
		if (!persons[i].partner.empty() && !persons[i].status)
			find(persons[i].partner).status = false;
}
void vote() {
	check_partner();
	DAY++;
	print();
	setcolor(95);
	cout << "===================================Time For Voting===================================" << endl;
	setcolor(0xF);
	if (count_alive() == 1) {
		for (int i = 0; i < number_of_people; i++)
		{
			if (persons[i].status) {
				setcolor(0xA);
				cout << persons[i].name << " Won the Game!" << endl;
				setcolor(0xF);
				exit(0);
			}
		}
	}

	int n = count_alive();
	int* votes = new int[n];
	memset(votes, 0, n * sizeof(votes[0]));
	string* names = new string[n];
	string name;
	int  cur = 0;
	int find = 0;
	/*start getting votes from alive persons*/
	for (int i = 0; i < number_of_people; i++)
	{
		if (persons[i].status) {
			cout << persons[i].name << " : ";
			cin >> name;
			find = 0;
			for (int j = 0; j < n; j++)
			{
				if (names[j] == name) {
					votes[j]++;
					find = true;
					break;
				}

			}
			if (!find) {
				names[cur] = name;
				votes[cur]++;
				cur++;
			}
		}
	}

	/*start sorting based on number of votes*/
	for (int i = 0; i < n - 1; i++)
		for (int j = 0; j < n - i - 1; j++)
			if (votes[j] > votes[j + 1]) {
				swap(votes[j], votes[j + 1]);
				swap(names[j], names[j + 1]);
			}

	/*Kill a person who has the max votes*/
	if (votes[n - 1] != votes[n - 2] && votes[n - 1] != 0)
		kill(names[n - 1]);

	reset();
	check_win();
}

void setcolor(int colorcode) {
	HANDLE console = GetStdHandle(STD_OUTPUT_HANDLE);
	SetConsoleTextAttribute(console, colorcode % 255);
}

string role_to_string(Role r)
{
	if (r == Role::UNKOWN) return string("UNKOWN");
	else if (r == Role::VILLAGER) return string("VILLAGER");
	else if (r == Role::WOLFMAN) return string("WOLFMAN");
	else if (r == Role::KILLER) return string("KILLER");
	else if (r == Role::FIREMAN) return string("FIREMAN");
	else if (r == Role::ANGLE) return string("GUARDIAN ANGLE");
	else if (r == Role::LOVE) return string("LOVE ANGLE");
	else if (r == Role::HUNTER) return string("HUNTER");
	else if (r == Role::FACTION) return string("FACTION");
	else return string("INVALID");
}

void reset()
{
	WOLFMAN = KILLER = FIREMAN = ANGLE = LOVE = FACTION = HUNTER = false;
}