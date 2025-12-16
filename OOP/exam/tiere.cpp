#include <iostream>
#include <string>

using namespace std;


/* Dieser Teil, also der Splash Screen ist KI generiert, nur damit da kein Missverständis aufkommt*/
void printCenteredSplashScreen(int width = 120) {
    string splashArt[] = {
        "$$$$$$$\\",
        "$$  __$$\\",
        "$$ |  $$ | $$$$$$\\  $$\\   $$\\  $$$$$$\\  $$$$$$$\\   $$$$$$$\\",
        "$$$$$$$\\ |$$  __$$\\ $$ |  $$ | \\____$$\\ $$  __$$\\ $$  _____|",
        "$$  __$$\\ $$ |  \\__|$$ |  $$ | $$$$$$$ |$$ |  $$ |\\$$$$$$\\",
        "$$ |  $$ |$$ |      $$ |  $$ |$$  __$$ |$$ |  $$ | \\____$$\\",
        "$$$$$$$  |$$ |      \\$$$$$$$ |\\$$$$$$$ |$$ |  $$ |$$$$$$$  |",
        "\\_______/ \\__|       \\____$$ | \\_______|\\__|  \\__|\\_______/",
        "                    $$\\   $$ |",
        "                    \\$$$$$$  |",
        "                     \\______/",
        "$$$$$$$$\\                          $$$$$$$\\",
        "\\____$$  |                         $$  __$$\\",
        "    $$  / $$$$$$\\   $$$$$$\\        $$ |  $$ | $$$$$$\\   $$$$$$\\   $$$$$$\\   $$$$$$\\  $$$$$$\\  $$$$$$\\$$$$\\  $$$$$$\\$$$$\\",
        "   $$  / $$  __$$\\ $$  __$$\\       $$$$$$$  |$$  __$$\\ $$  __$$\\ $$  __$$\\ $$  __$$\\ \\____$$\\ $$  _$$  _$$\\ $$  _$$  _$$\\",
        "  $$  /  $$ /  $$ |$$ /  $$ |      $$  ____/ $$ |  \\__|$$ /  $$ |$$ /  $$ |$$ |  \\__|$$$$$$$ |$$ / $$ / $$ |$$ / $$ / $$ |",
        " $$  /   $$ |  $$ |$$ |  $$ |      $$ |      $$ |      $$ |  $$ |$$ |  $$ |$$ |     $$  __$$ |$$ | $$ | $$ |$$ | $$ | $$ |",
        "$$$$$$$$\\\\$$$$$$  |\\$$$$$$  |      $$ |      $$ |      \\$$$$$$  |\\$$$$$$$ |$$ |     \\$$$$$$$ |$$ | $$ | $$ |$$ | $$ | $$ |",
        "\\________|\\______/  \\______/       \\__|      \\__|       \\______/  \\____$$ |\\__|      \\_______|\\__| \\__| \\__|\\__| \\__| \\__|",
        "                                                                 $$\\   $$ |",
        "                                                                 \\$$$$$$  |",
        "                                                                  \\______/"
    };

    for (const auto& line : splashArt) {

        cout << line << endl;

    }
}


class Tier {
protected:
    string name;
    int alter;

public:
    Tier(string n, int a) {
        name = n;
        alter = a;
        cout << "Das Tier " << name << " wurde aus der Erde erchaffen.\n";
    }

    virtual void vorstellen() const {
        cout << "Ich bin ein tierisches Tier. Me nombre es " << name << " und ich bin " << alter << " Sonnenumlaufe alt.\n";   
    }

    virtual void lautGeben() = 0; // wie @abstractmethod in Python

    virtual ~Tier() {
        cout << "Das Tier, welches sich " << name << " schimpft wurde getoetet.\n";
    }
};

class Vogel : public Tier {
private:
    float flugelspannweite;

public:
    Vogel(string n, int a, float f) : Tier(n, a) {
        flugelspannweite = f;
        cout << "Geschluepft: " << name << "." << endl;
    }

    void vorstellen() {
        Tier::vorstellen();
        float wing_span_inches = flugelspannweite / 2.54;
        cout << "Hey, there!. Bird here...with a wingspan of " << flugelspannweite << " cm. Or " << wing_span_inches << " in freedom units for you gun slinging Jesus-loving americans" << endl;
    }

    void lautGeben() {
        cout << name << " singt: I'm like a bird, I'll only fly away. I don't know where my soul is (Soul is). I don't know where my home is All I need for you to know is - Nelly Furtado (ca. 2000)" << endl;
    }

    ~Vogel() {
        cout << "Ein Vogel namens " << name << " ist von Himmel geschoßen worden." << endl;
    }
};

class Saeugetier : public Tier {
private:
    string fellfarbe;

public:
    Saeugetier(string n, int a, string f) : Tier(n, a) {
        fellfarbe = f;
        cout << "Ein einsamer Säuger, getauft im Namen " << name << " ward geboren." << endl;
    }

    void vorstellen() {
        Tier::vorstellen();
        cout << "Mein Fell hat die Farbe " << fellfarbe << ". Ganz schön rassistisch mich das zu fragen findest du nicht? Lol." << endl;
    }

    void lautGeben() {
        cout << name << " : Moo. I said moo. Look, I'm just a cow, okay?!" << endl; // Fun Fact: Ist ein pop-cult reference aus Diablo 1....das Spiel wurde auch in C/C++ geschrieben.
    }

    ~Saeugetier() {
        cout << "Ein kleiner " << name << " stirbt nur zum Schein Wollte ganz alleine sein. Das kleine Herz stand still für Stunden So hat man es für tot befunden." << endl; // Rammstein Reference
    };
};

int main() {

    printCenteredSplashScreen();
    
    cout << "Preamble" << endl;
    cout << "Dann sprach Gott: 'Die Erde bringe alle Arten lebender Wesen hervor, Vieh, Kriechgetier und wilde Landtiere, jedes nach seiner Art!' Und es geschah so. Da machte Gott alle Arten der wilden Landtiere und alle Arten des Viehs und alles Getier, das auf dem Erdboden kriecht, jedes nach seiner Art. Und Gott sah, dass es gut war.\n\n" << endl;

    Vogel* adler = new Vogel("Der Adler Detlef Heinrich von Eberstahl", 5, 200.5);
    Saeugetier* kuh = new Saeugetier("Die Kuh Berta Mandy Schmidt", 10, "chromoxydgrün");

    cout << "\nVORSTELLUNGSRUNDE!!!" << endl;
    adler->vorstellen();
    kuh->vorstellen();

    cout << "\nPARTY!!!" << endl; // Polymorphismus ist dem Compiler direkt klar
    adler->lautGeben();
    kuh->lautGeben();

    cout << "\nMorphius von Poly" << endl; // Polymorph erst Runtime klar
    Tier* tiere[2];
    tiere[0] = adler;
    tiere[1] = kuh;

    for (int i = 0; i < 2; i++) {
        tiere[i]->lautGeben();
    }

    cout << "\nDer Schlachthof beginnt seine Arbeit" << endl;
    delete adler;
    delete kuh;

    cout << "\n\nFin!\n" << endl;
    cout << "////////////////////////////////////////////////////////////" << endl;
    cout << "// Eine Bryan Barcelona TELE-PRODUKTION (2025)            //" << endl;
    cout << "////////////////////////////////////////////////////////////" << endl;
    cout << " " << endl;
    cout << "Dieses Telespiel ist eine Produktion von Bryan Barcelona in Ko-Produktion" << endl;
    cout << "mit dem Norddeutschen Rundfunk (NDR), dem Westdeutschen Rundfunk (WDR)," << endl;
    cout << "dem Hessischen Rundfunk (HR) und der ARD, hergestellt in den Ateliers" << endl;
    cout << "Berlin-Babelsberg unter Verwendung des Magnetton-Verfahrens." << endl;
    cout << " " << endl;
    cout << "////////////////////////////////////////////////////////////" << endl;
    return 0;

}