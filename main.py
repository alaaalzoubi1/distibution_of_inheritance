from experta import *
import tkinter as tk
from tkinter import messagebox

class Person:
    def __init__(self, gender, mother=None, father=None, spouse=None, _sons=None, _daughters=None, aLive=True,
                 name=None, allotment=0):
        self._gender = gender
        self._mother = mother
        self._father = father
        self._spouse = spouse
        self._sons = []
        self._daughters = []
        self.aLive = aLive                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        self.name = name
        self.allotment = allotment

    # Getter and Setter for gender
    def get_gender(self):
        return self._gender

    def set_gender(self, gender):
        self._gender = gender

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    # Getter and Setter for mother
    def get_mother(self):
        return self._mother

    def set_mother(self, mother):
        self._mother = mother

    # Getter and Setter for father
    def get_father(self):
        return self._father

    def set_father(self, father):
        self._father = father

    def get_spouse(self):
        return self._spouse

    def set_spouse(self, spouse):
        self._spouse = spouse

    def get_allotment(self):
        return self.allotment

    def set_allotment(self, allotment):
        self.allotment = allotment

    def add_sons(self, _sons):
        self._sons.append(_sons)

    def get_sons(self):
        return self._sons

    def add_daughters(self, _daughters):
        self._daughters.append(_daughters)

    def get_daughters(self):
        return self._daughters

    def set_aLive(self, aLive):
        if (aLive == "yes"):
            self.aLive = True
        else:
            self.aLive = False

    def get_aLive(self):
        return self.aLive


def has_children(person):
    for daughter in person.get_daughters():
        if (daughter.get_aLive()):
            return True
    for son in person.get_sons():
        if (son.get_aLive()):
            return True
    return False;


def children_count(person):
    counter = len(person.get_daughters()) + len(person.get_sons())
    return counter


the_walking_dead = Person("male", name="alaa")

class FamilyTree(KnowledgeEngine):
    @DefFacts()
    def _initial_facts(self):
        yield Fact(action="start")

    @Rule(Fact(action='start'), NOT(Fact(gender=W())), salience=10)
    def gender(self):
        the_walking_dead.set_gender(input("what is you gender"))
        self.declare(Fact(gender="yes"))

    @Rule(Fact(action='start'), Fact(gender=W()), NOT(Fact(has_father=W())), salience=10)
    def has_father(self):
        father = Person("male")
        the_walking_dead.set_father(father)
        father.set_name(input("what is your fathers name?"))
        is_alive_input = input("Is he alive? (yes/no): ")
        print(the_walking_dead.get_father().get_name())
        father.set_aLive(is_alive_input)
        self.declare(Fact(has_father=is_alive_input))

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father=W())), NOT(Fact(has_mother=W())), salience=10)
    def has_mother(self):
        mother = Person("female")
        the_walking_dead.set_mother(mother)

        if the_walking_dead.get_gender() == "male":
            mother.add_sons(the_walking_dead)
        else:
            mother.add_daughters(the_walking_dead)
        mother.set_name(input("what is your mothers name?"))
        is_alive_input = input("Is she alive? (yes/no): ")
        print(the_walking_dead.get_mother().get_name())
        mother.set_aLive(is_alive_input)
        self.declare(Fact(has_mother=is_alive_input))

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father=W())), (Fact(has_mother=W())),
          NOT(Fact(has_spouse=W())), salience=10)
    def has_spouse(self):
        if (input("did you have a spouse?") == "no"):
            self.declare(Fact(has_spouse="no"))
        else:
            if (the_walking_dead.get_gender() == "male"):
                spouse = Person("female")
            else:
                spouse = Person("male")
            the_walking_dead.set_spouse(spouse)
            spouse.set_spouse(the_walking_dead)

            spouse.set_name(input("what is your spouse name?"))
            is_alive_input = input("are they alive? (yes/no): ")
            print(the_walking_dead.get_spouse().get_name())
            spouse.set_aLive(is_alive_input)
            self.declare(Fact(has_spouse=is_alive_input))

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father=W())), (Fact(has_mother=W())), Fact(has_spouse=W()),
          NOT(Fact(has_daughters=W())), salience=10)
    def has_daughters(self):
        try:
            daughters_count_str = input("How many daughters do you have? ")
            daughters_count = int(daughters_count_str)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return

        if daughters_count == 0:
            self.declare(Fact(has_daughters="no"))
        else:
            self.declare(Fact(has_daughters="yes"))
            for i in range(daughters_count):
                daughter_name = input(f"Input the {i + 1}-daughter name: ")

                daughter_temp = Person("female", name=daughter_name)
                daughter_temp.set_aLive(input("is she a live?"))
                if(not(daughter_temp.get_aLive())):
                    has_child = input("did she has alive children ?")
                    if(has_child == "yes"):
                        children_count = input("how many?")
                        c = int(children_count)
                        for i in range(c):
                            gender = input("male or female?")
                            child_name = input("what is name ? ")
                            child = Person(gender,name=child_name)
                            if(gender == "male"):
                                daughter_temp.add_sons(child)
                            if(gender == "female"):
                                daughter_temp.add_daughters(child)
                the_walking_dead.add_daughters(daughter_temp)

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father=W())), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), NOT(Fact(has_sons=W())), salience=10)
    def has_sons(self):
        try:
            sons_count_str = input("How many sons do you have? ")
            sons_count = int(sons_count_str)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return

        if sons_count == 0:
            self.declare(Fact(has_sons="no"))
        else:
            self.declare(Fact(has_sons="yes"))
            for i in range(sons_count):
                son_name = input(f"Input the {i + 1}-son name: ")
                son_temp = Person("male", name=son_name)
                son_temp.set_aLive(input("is he alive?"))
                the_walking_dead.add_sons(son_temp)

                print(the_walking_dead.get_sons())
                if not son_temp.get_aLive():
                    has_child = input("has he got alive children ?")
                    if (has_child == "yes"):
                        children_count = input("how many?")
                        c = int(children_count)
                        for i in range(c):
                            gender = input("male or female?")
                            child_name = input("what is name ? ")
                            child = Person(gender, name=child_name)
                            if (gender == "male"):
                                son_temp.add_sons(child)
                            if (gender == "female"):
                                son_temp.add_daughters(child)

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father=W())), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), Fact(has_sons="yes"), salience=10)
    def inheritance_distribution1(self):
        inheritance = 100
        inheritance2 = 100
        if (the_walking_dead.get_father().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_father().set_allotment(str(allotment))
            print(the_walking_dead.get_father().get_name() + " : " + the_walking_dead.get_father().get_allotment())
        if (the_walking_dead.get_mother().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_mother().set_allotment(str(allotment))
            print(the_walking_dead.get_mother().get_name() + " : " + the_walking_dead.get_mother().get_allotment())

        if(the_walking_dead.get_spouse() != None):
            if (the_walking_dead.get_spouse().get_aLive()):
                if (the_walking_dead.get_spouse().get_gender() == "female"):
                    allotment = inheritance / 8
                    inheritance2 -= allotment
                    the_walking_dead.get_spouse().set_allotment(str(allotment))
                else:
                    allotment = inheritance / 4
                    inheritance2 -= allotment
                    the_walking_dead.get_spouse().set_allotment(str(allotment))
                print(the_walking_dead.get_spouse().get_name() + " : " + the_walking_dead.get_spouse().get_allotment())
        daughter_counter = 0
        sons_counter = 0
        for daughter in the_walking_dead.get_daughters():
            daughter_counter += 1
        for son in the_walking_dead.get_sons():
            sons_counter += 1
        daughter_counter = daughter_counter / 2
        allotment = inheritance2 / (daughter_counter + sons_counter)
        for son in the_walking_dead.get_sons():
            if (son.get_aLive()):
                son.set_allotment(str(allotment))
                print(son.get_name() + " : " + son.get_allotment())
            else:
                children_count = 0
                for s in son.get_sons():
                    children_count+=1
                for s in son.get_daughters():
                    children_count += 1
                if(children_count > 0):
                    for s in son.get_sons():
                        s.set_allotment(str(allotment/children_count))
                        print(s.get_name() + " : " + s.get_allotment())
                    for s in son.get_daughters():
                        s.set_allotment(str(allotment/children_count))
                        print(s.get_name() + " : " + s.get_allotment())

        for daughter in the_walking_dead.get_daughters():
            if (daughter.get_aLive()):
                daughter.set_allotment(str(allotment / 2))
                print(daughter.get_name() + " : " + daughter.get_allotment())
            else:
                children_count = 0
                for s in daughter.get_sons():
                    children_count += 1
                for s in daughter.get_daughters():
                    children_count += 1
                print(children_count)
                if (children_count > 0):
                    for s in daughter.get_sons():
                        s.set_allotment(str(allotment / (children_count*2)))
                        print(s.get_name() + " : " + s.get_allotment())
                    for s in daughter.get_daughters():

                        s.set_allotment(str(allotment / (children_count*2)))
                        print(s.get_name() + " : " + s.get_allotment())

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father="yes")), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), Fact(has_sons="no"), salience=10)
    def inheritance_distribution2(self):
        inheritance = 100
        inheritance2 = 100
        if (the_walking_dead.get_father().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_father().set_allotment(str(allotment))
        if (the_walking_dead.get_mother().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_mother().set_allotment(str(allotment))
            print(the_walking_dead.get_mother().get_name() + " : " + the_walking_dead.get_mother().get_allotment())

        if (the_walking_dead.get_spouse() != None):
            if (the_walking_dead.get_spouse().get_aLive()):
                children_count = 0
                for s in the_walking_dead.get_sons():
                    children_count += 1
                for s in the_walking_dead.get_daughters():
                    children_count += 1
                if (the_walking_dead.get_spouse().get_gender() == "female"):
                    if(children_count>0):
                        allotment = inheritance / 8
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                else:
                    if(children_count>0):
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 2
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                print(the_walking_dead.get_spouse().get_name() + " : " + the_walking_dead.get_spouse().get_allotment())
        daughter_count = 0
        for da in the_walking_dead.get_daughters():
            daughter_count += 1
        daughter_allotment = (2 * inheritance) / (3 * daughter_count)
        for daughter in the_walking_dead.get_daughters():

            if (daughter.get_aLive()):
                if daughter_count == 1:
                    allotment = inheritance / 2
                    daughter.set_allotment(str(allotment))
                    inheritance2 -= allotment
                    print(daughter.get_name() + " : " + daughter.get_allotment())
                else:
                    allotment = daughter_allotment
                    inheritance2 -= allotment
                    daughter.set_allotment(str(allotment))
                    print(daughter.get_name() + " : " + daughter.get_allotment())

            else:
                children_count = 0
                for s in daughter.get_sons():
                    children_count += 1
                for s in daughter.get_daughters():
                    children_count += 1
                print(children_count)
                if (children_count > 0):
                    for s in daughter.get_sons():
                        s.set_allotment(str(daughter_allotment / children_count))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
                    for s in daughter.get_daughters():
                        s.set_allotment(str(daughter_allotment / (children_count)))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
        the_father_allotment = float(the_walking_dead.get_father().get_allotment())
        if inheritance2 > 0:
            the_father_allotment += inheritance2
        the_walking_dead.get_father().set_allotment(str(the_father_allotment))
        print(the_walking_dead.get_father().get_name() + " : " + the_walking_dead.get_father().get_allotment())

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father="no")), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), Fact(has_sons=W()), NOT(Fact(has_grandfather=W())), salience=10)
    def has_grandfather(self):
        grandfather_name = input("what is your grandfathers name?")
        alive = input("is he alive?")
        grandfather = Person("male", name=grandfather_name)
        grandfather.set_aLive(alive)
        the_walking_dead.get_father().set_father(grandfather)
        if grandfather.get_aLive():
            self.declare(Fact(has_grandfather="yes"))
        else:
            self.declare(Fact(has_grandfather="no"))

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father="no")), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), Fact(has_sons="no"),Fact(has_grandfather=W()), NOT(Fact(has_siblings=W())), salience=10)
    def has_siblings(self):
        try:
            siblings_count_str = input("How many siblings do you have? ")
            siblings_count = int(siblings_count_str)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return

        if siblings_count == 0:
            self.declare(Fact(has_siblings="no"))
        else:
            self.declare(Fact(has_siblings="yes"))
            for i in range(siblings_count):
                gender = input("what is your sibling gender?")
                sibling_name = input(f"Input the {i + 1}-sibling name: ")
                sibling_temp = Person(gender, name=sibling_name)
                sibling_temp.set_aLive(input("is they a live?"))
                if (not (sibling_temp.get_aLive())):
                    has_child = input("did they has alive children ?")
                    if (has_child == "yes"):
                        children_count = input("how many?")
                        c = int(children_count)
                        for i in range(c):
                            gender = input("male or female?")
                            child_name = input("what is name ? ")
                            child = Person(gender, name=child_name)
                            if (gender == "male"):
                                sibling_temp.add_sons(child)
                            if (gender == "female"):
                                sibling_temp.add_daughters(child)
                if sibling_temp.get_gender() == "male":
                    the_walking_dead.get_father().add_sons(sibling_temp)
                else:
                    the_walking_dead.get_father().add_daughters(sibling_temp)

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father="no")), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), Fact(has_sons="no"),Fact(has_grandfather=W()),Fact(has_siblings="yes"), salience=10)
    def inheritance_distribution3(self):
        inheritance = 100
        inheritance2 = 100
        if (the_walking_dead.get_father().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_father().set_allotment(str(allotment))
        elif(the_walking_dead.get_father().get_father().get_aLive):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_father().get_father().set_allotment(str(allotment))
            print(the_walking_dead.get_father().get_father().get_name() + " : " + the_walking_dead.get_father().get_father().get_allotment())
        if (the_walking_dead.get_mother().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_mother().set_allotment(str(allotment))
            print(the_walking_dead.get_mother().get_name() + " : " + the_walking_dead.get_mother().get_allotment())
        if (the_walking_dead.get_spouse() != None):
            if (the_walking_dead.get_spouse().get_aLive()):
                children_count = 0
                for s in the_walking_dead.get_sons():
                    children_count += 1
                for s in the_walking_dead.get_daughters():
                    children_count += 1
                if (the_walking_dead.get_spouse().get_gender() == "female"):
                    if (children_count > 0):
                        allotment = inheritance / 8
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                else:
                    if (children_count > 0):
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 2
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                print(the_walking_dead.get_spouse().get_name() + " : " + the_walking_dead.get_spouse().get_allotment())
        daughter_count = 0
        for da in the_walking_dead.get_daughters():
            daughter_count += 1
        if daughter_count > 0:
            daughter_allotment = (2 * inheritance) / (3 * daughter_count)
        for daughter in the_walking_dead.get_daughters():

            if (daughter.get_aLive()):
                if daughter_count == 1:
                    allotment = inheritance / 2
                    daughter.set_allotment(str(allotment))
                    inheritance2 -= allotment
                    print(daughter.get_name() + " : " + daughter.get_allotment())
                else:
                    allotment = daughter_allotment
                    inheritance2 -= allotment
                    daughter.set_allotment(str(allotment))
                    print(daughter.get_name() + " : " + daughter.get_allotment())

            else:
                children_count = 0
                for s in daughter.get_sons():
                    children_count += 1
                for s in daughter.get_daughters():
                    children_count += 1
                print(children_count)
                if (children_count > 0):
                    for s in daughter.get_sons():
                        s.set_allotment(str(daughter_allotment / children_count))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
                    for s in daughter.get_daughters():
                        s.set_allotment(str(daughter_allotment / (children_count)))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
        siblings_count = 0
        for bro in the_walking_dead.get_father().get_sons():
            siblings_count += 1
        for sis in the_walking_dead.get_father().get_daughters():
            siblings_count += 0.5
        allotment = inheritance2 / siblings_count
        for bro in the_walking_dead.get_father().get_sons():
            if bro.get_aLive():
                bro.set_allotment(str(allotment))
                print(bro.get_name() + " : " + bro.get_allotment())
            else:
                children_ofsibling_count = 0
                for sibbro in bro.get_sons():
                    children_ofsibling_count += 1
                for sibgir in bro.get_daughters():
                    children_ofsibling_count += 0.5
                print(children_ofsibling_count)
                if children_ofsibling_count > 0:
                    for sibbro in bro.get_sons():
                        sibbro.set_allotment(str(allotment/children_ofsibling_count))
                        print(sibbro.get_name() + " : " + sibbro.get_allotment())
                    for sibgir in bro.get_daughters():
                        sibgir.set_allotment(str(allotment/(children_ofsibling_count*2)))
                        print(sibgir.get_name() + " : " + sibgir.get_allotment())

        for sis in the_walking_dead.get_father().get_daughters():
            if sis.get_aLive():
                sis.set_allotment(str(allotment/2))
                print(sis.get_name() + " : " + sis.get_allotment())
            else:
                children_ofsibling_count = 0
                for sibbro in sis.get_sons():
                    children_ofsibling_count += 1
                for sibgir in sis.get_daughters():
                    children_ofsibling_count += 0.5
                if children_ofsibling_count > 0:
                    for sibbro in sis.get_sons():
                        sibbro.set_allotment(str(allotment / children_ofsibling_count))
                        print(sibbro.get_name() + " : " + sibbro.get_allotment())
                    for sibgir in sis.get_daughters():
                        sibgir.set_allotment(str(allotment / (children_ofsibling_count * 2)))
                        print(sibgir.get_name() + " : " + sibgir.get_allotment())

    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father="no")), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), Fact(has_sons="no"), Fact(has_grandfather="yes"), Fact(has_siblings="no"),
          salience=10)
    def inheritance_distribution4(self):
        inheritance = 100
        inheritance2 = 100
        if (the_walking_dead.get_father().get_father().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_father().get_father().set_allotment(str(allotment))
        if (the_walking_dead.get_mother().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_mother().set_allotment(str(allotment))
            print(the_walking_dead.get_mother().get_name() + " : " + the_walking_dead.get_mother().get_allotment())

        if (the_walking_dead.get_spouse() != None):
            if (the_walking_dead.get_spouse().get_aLive()):
                children_count = 0
                for s in the_walking_dead.get_sons():
                    children_count += 1
                for s in the_walking_dead.get_daughters():
                    children_count += 1
                if (the_walking_dead.get_spouse().get_gender() == "female"):
                    if (children_count > 0):
                        allotment = inheritance / 8
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                else:
                    if (children_count > 0):
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 2
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                print(the_walking_dead.get_spouse().get_name() + " : " + the_walking_dead.get_spouse().get_allotment())
        daughter_count = 0
        for da in the_walking_dead.get_daughters():
            daughter_count += 1
        if daughter_count > 0:
            daughter_allotment = (2 * inheritance) / (3 * daughter_count)
        for daughter in the_walking_dead.get_daughters():

            if (daughter.get_aLive()):
                if daughter_count == 1:
                    allotment = inheritance / 2
                    daughter.set_allotment(str(allotment))
                    inheritance2 -= allotment
                    print(daughter.get_name() + " : " + daughter.get_allotment())
                else:
                    allotment = daughter_allotment
                    inheritance2 -= allotment
                    daughter.set_allotment(str(allotment))
                    print(daughter.get_name() + " : " + daughter.get_allotment())

            else:
                children_count = 0
                for s in daughter.get_sons():
                    children_count += 1
                for s in daughter.get_daughters():
                    children_count += 1
                print(children_count)
                if (children_count > 0):
                    for s in daughter.get_sons():
                        s.set_allotment(str(daughter_allotment / children_count))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
                    for s in daughter.get_daughters():
                        s.set_allotment(str(daughter_allotment / (children_count)))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
        the_father_allotment = float(the_walking_dead.get_father().get_father().get_allotment())
        if inheritance2 > 0:
            the_father_allotment += inheritance2
        the_walking_dead.get_father().get_father().set_allotment(str(the_father_allotment))
        print(the_walking_dead.get_father().get_father().get_name() + " : " + the_walking_dead.get_father().get_father().get_allotment())
    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father="no")), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), Fact(has_sons="no"), Fact(has_grandfather="no"), Fact(has_siblings="no"),NOT(Fact(has_uncleOrAnte=W())),
          salience=10)
    def has_uncleOrAnte(self):
        unc_count = input("how many uncles have you got?")
        u_count = int(unc_count)
        ant_count = input("how many antes have you got?")
        a_count = int(ant_count)
        if u_count == 0 and a_count ==0:
            self.declare(Fact(has_shas_uncleOrAnteons="no"))
        else:
            self.declare(Fact(has_has_uncleOrAntesons="yes"))
            for i in range(u_count):
                uncle_name = input(f"Input the {i + 1}-uncle name: ")
                uncle_temp = Person("male", name=uncle_name)
                uncle_temp.set_aLive(input("is he alive?"))
                if (not (uncle_temp.get_aLive())):
                    has_child = input("has he got alive children ?")
                    if (has_child == "yes"):
                        children_count = input("how many?")
                        c = int(children_count)
                        for i in range(c):
                            gender = input("male or female?")
                            child_name = input("what is name ? ")
                            child = Person(gender, name=child_name)
                            if (gender == "male"):
                                uncle_temp.add_sons(child)
                            if (gender == "female"):
                                uncle_temp.add_daughters(child)
                the_walking_dead.get_father().get_father().add_sons(uncle_temp)
            for i in range(a_count):
                ante_name = input(f"Input the {i + 1}-ante name: ")
                ante_temp = Person("male", name=ante_name)
                ante_temp.set_aLive(input("is she alive?"))
                if (not (ante_temp.get_aLive())):
                    has_child = input("has she got alive children ?")
                    if (has_child == "yes"):
                        children_count = input("how many?")
                        c = int(children_count)
                        for i in range(c):
                            gender = input("male or female?")
                            child_name = input("what is name ? ")
                            child = Person(gender, name=child_name)
                            if (gender == "male"):
                                ante_temp.add_sons(child)
                            if (gender == "female"):
                                ante_temp.add_daughters(child)
                the_walking_dead.get_father().get_father().add_daughters(ante_temp)
    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father="no")), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), Fact(has_sons="no"), Fact(has_grandfather="no"), Fact(has_siblings="no"),NOT(Fact(has_uncleOrAnte="yes")),
          salience=10)
    def inheritance_distribution5(self):
        inheritance = 100
        inheritance2 = 100
        if (the_walking_dead.get_mother().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_mother().set_allotment(str(allotment))
            print(the_walking_dead.get_mother().get_name() + " : " + the_walking_dead.get_mother().get_allotment())
        if (the_walking_dead.get_spouse() != None):
            if (the_walking_dead.get_spouse().get_aLive()):
                children_count = 0
                for s in the_walking_dead.get_sons():
                    children_count += 1
                for s in the_walking_dead.get_daughters():
                    children_count += 1
                if (the_walking_dead.get_spouse().get_gender() == "female"):
                    if (children_count > 0):
                        allotment = inheritance / 8
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                else:
                    if (children_count > 0):
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 2
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                print(the_walking_dead.get_spouse().get_name() + " : " + the_walking_dead.get_spouse().get_allotment())
        daughter_count = 0
        for da in the_walking_dead.get_daughters():
            daughter_count += 1
        if daughter_count > 0:
            daughter_allotment = (2 * inheritance) / (3 * daughter_count)
        for daughter in the_walking_dead.get_daughters():

            if (daughter.get_aLive()):
                if daughter_count == 1:
                    allotment = inheritance / 2
                    daughter.set_allotment(str(allotment))
                    inheritance2 -= allotment
                    print(daughter.get_name() + " : " + daughter.get_allotment())
                else:
                    allotment = daughter_allotment
                    inheritance2 -= allotment
                    daughter.set_allotment(str(allotment))
                    print(daughter.get_name() + " : " + daughter.get_allotment())

            else:
                children_count = 0
                for s in daughter.get_sons():
                    children_count += 1
                for s in daughter.get_daughters():
                    children_count += 1
                print(children_count)
                if (children_count > 0):
                    for s in daughter.get_sons():
                        s.set_allotment(str(daughter_allotment / children_count))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
                    for s in daughter.get_daughters():
                        s.set_allotment(str(daughter_allotment / (children_count)))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
        unclesandantes_count = 0
        for uncle in the_walking_dead.get_father().get_father().get_sons():
            unclesandantes_count += 1
        for ante in the_walking_dead.get_father().get_father().get_daughters():
            unclesandantes_count += 0.5
        if unclesandantes_count > 0:
            allotment = inheritance2 / unclesandantes_count
        for uncle in the_walking_dead.get_father().get_father().get_sons():
            if uncle.get_aLive():
                uncle.set_allotment(str(allotment))
                print(uncle.get_name() + " : " + uncle.get_allotment())
            else:
                children_ofuncle_count = 0
                for cousin in uncle.get_sons():
                    children_ofuncle_count += 1
                for cousin_g in uncle.get_daughters():
                    children_ofuncle_count += 0.5
                if children_ofuncle_count > 0:
                    for sibbro in uncle.get_sons():
                        sibbro.set_allotment(str(allotment / children_ofuncle_count))
                        print(sibbro.get_name() + " : " + sibbro.get_allotment())
                    for sibgir in uncle.get_daughters():
                        sibgir.set_allotment(str(allotment / (children_ofuncle_count * 2)))
                        print(sibgir.get_name() + " : " + sibgir.get_allotment())

        for ante in the_walking_dead.get_father().get_father().get_daughters():
            if ante.get_aLive():
                ante.set_allotment(str(allotment / 2))
                print(ante.get_name() + " : " + ante.get_allotment())
            else:
                children_ofante_count = 0
                for sibbro in ante.get_sons():
                    children_ofante_count += 1
                for sibgir in ante.get_daughters():
                    children_ofante_count += 0.5
                if children_ofante_count > 0:
                    for sibbro in ante.get_sons():
                        sibbro.set_allotment(str(allotment / (children_ofante_count*2)))
                        print(sibbro.get_name() + " : " + sibbro.get_allotment())
                    for sibgir in ante.get_daughters():
                        sibgir.set_allotment(str(allotment / ((children_ofante_count * 4))))
                        print(sibgir.get_name() + " : " + sibgir.get_allotment())
    @Rule(Fact(action='start'), Fact(gender=W()), (Fact(has_father="no")), (Fact(has_mother=W())), Fact(has_spouse=W()),
          Fact(has_daughters=W()), Fact(has_sons="no"), Fact(has_grandfather="no"), Fact(has_siblings="no"),NOT(Fact(has_uncleOrAnte="no")),
          salience=10)
    def inheritance_distribution6(self):
        inheritance = 100
        inheritance2 = 100
        if (the_walking_dead.get_mother().get_aLive()):
            allotment = inheritance / 6
            inheritance2 -= allotment
            the_walking_dead.get_mother().set_allotment(str(allotment))
            print(the_walking_dead.get_mother().get_name() + " : " + the_walking_dead.get_mother().get_allotment())
        if (the_walking_dead.get_spouse() != None):
            if (the_walking_dead.get_spouse().get_aLive()):
                children_count = 0
                for s in the_walking_dead.get_sons():
                    children_count += 1
                for s in the_walking_dead.get_daughters():
                    children_count += 1
                if (the_walking_dead.get_spouse().get_gender() == "female"):
                    if (children_count > 0):
                        allotment = inheritance / 8
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                else:
                    if (children_count > 0):
                        allotment = inheritance / 4
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                    else:
                        allotment = inheritance / 2
                        inheritance2 -= allotment
                        the_walking_dead.get_spouse().set_allotment(str(allotment))
                print(the_walking_dead.get_spouse().get_name() + " : " + the_walking_dead.get_spouse().get_allotment())
        daughter_count = 0
        for da in the_walking_dead.get_daughters():
            daughter_count += 1
        if daughter_count > 0:
            daughter_allotment = (2 * inheritance) / (3 * daughter_count)
        for daughter in the_walking_dead.get_daughters():

            if (daughter.get_aLive()):
                if daughter_count == 1:
                    allotment = inheritance / 2
                    daughter.set_allotment(str(allotment))
                    inheritance2 -= allotment
                    print(daughter.get_name() + " : " + daughter.get_allotment())
                else:
                    allotment = daughter_allotment
                    inheritance2 -= allotment
                    daughter.set_allotment(str(allotment))
                    print(daughter.get_name() + " : " + daughter.get_allotment())

            else:
                children_count = 0
                for s in daughter.get_sons():
                    children_count += 1
                for s in daughter.get_daughters():
                    children_count += 1
                print(children_count)
                if (children_count > 0):
                    for s in daughter.get_sons():
                        s.set_allotment(str(daughter_allotment / children_count))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
                    for s in daughter.get_daughters():
                        s.set_allotment(str(daughter_allotment / (children_count)))
                        inheritance2 -= (daughter_allotment / children_count)
                        print(s.get_name() + " : " + s.get_allotment())
        print("ترد باقي التركة على اصحاب الفروض من الورثة عدا الزوجين")
family_tree = FamilyTree()

# Declare the initial facts
family_tree.reset()
family_tree.declare(Fact(action="start"))
family_tree.run()
