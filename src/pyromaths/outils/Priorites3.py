#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#
#----------------------------------------------------------------------
# Pyromaths : GESTION DES PRIORITES
#----------------------------------------------------------------------
#from pyromaths.classes.PolynomesCollege import Polynome
#from pyromaths.classes.Fractions import Fraction
from Affichage import decimaux

def cherche_classe(calcul, index):
    """**cherche_classe**\ (*calcul*\ , *index*)

    Recherche le premier objet polynôme ou fraction dans la chaîne calcul à une
    position supérieure ou égale à index, sans expression régulière

    :param calcul: le calcul à tester
    :type calcul: string
    :param index: position à partir de laquelle effectuer le test
    :type index: integer

    >>> from pyromaths.classes.PolynomesCollege import Polynome
    >>> from pyromaths.classes.Fractions import Fraction
    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.cherche_classe('Polynome([[-4, 2]], "x")-Polynome([[-5, 1], [4, 2], [1, 0]], "x")+Polynome([[6,  0], [5, 1]], "x")', 5)
    'Polynome([[-5, 1], [4, 2], [1, 0]], "x")'
    >>> Priorites3.cherche_classe('Polynome([[-4, 2]], "x")+Fraction(3,2)+Polynome([[6,  0], [5, 1]], "x")', 5)
    'Fraction(3,2)'

    :rtype: string
    """
    classes = ["Polynome(", "Fraction("]
    indexes = [calcul.find(classe, index) for classe in classes]
    position, i = 0, 1
    while i < len(classes):
        if 0 <= indexes[i] and (indexes[position] < 0 or indexes[i]< indexes[position]):
            position = i
        i += 1
    if indexes[position] < 0: return None
    classe = classes[position]
    index = indexes[position]
    par, i = 1, index + len(classe) # nombre de parenthèses ouvertes, début de recherche
    while par:
        if calcul.find("(", i)>0:
            i = min(calcul.find("(", i), calcul.find(")", i))
        else:
            i = calcul.find(")", i)
        if calcul[i] == ")": par += -1
        else: par += 1
        i += 1
    return calcul[index:i]

def cherche_decimal(calcul, index):
    """**cherche_decimal**\ (*calcul*\ , *index*)

    Recherche le premier nombre décimal dans la chaîne calcul à une position
    supérieure ou égale à index, sans expression régulière.
    Un nombre décimal peut être entouré de parenthèses s'il a un signe, ou avoir
    un signe s'il est en début de chaîne.

    Cette fonction est 130 fois plus rapide qu'avec une expression régulière.

    :param calcul: le calcul à tester
    :type calcul: string
    :param index: position à partir de laquelle effectuer le test
    :type index: integer

    >>> from pyromaths.outils import Priorites3
    >>> p = '-Polynome([[-4, 2]], "x")*6**2+3'
    >>> Priorites3.cherche_decimal(p, 1)
    '4'
    >>> p = '-6*(-11)*(-5)'
    >>> Priorites3.cherche_decimal(p, 1)
    '6'
    >>> Priorites3.cherche_decimal(p, 0)
    '6'

    **TODO :** vérifier ces deux derniers exemples. Je pense que je devrais récupérer -6

    :rtype: string
    """
    end = len(calcul)
    while index<=end:
        try:
            int(calcul[index])
        except:
            index+=1
        else:
            break
    if index>end: return None
    while end>index:
        try:
            float(calcul[index:end])
        except ValueError:
            end -= 1
        else:
            break
    if index>1 and (calcul[index-2:index] == "(+" or calcul[index-2:index] ==
            "(-") :
        if end < len(calcul) and calcul[end]==")":
            index -= 2
            end += 1
        else:
            index -= 1
    return calcul[index:end]

def cherche_operateur(calcul, index):
    """**cherche_operateur**\ (*calcul*\ , *min_i*)

    Recherche le premier opérateur +, -, \*, /, ^ dans la chaîne calcul à une position
    supérieure ou égale à min_i, sans expression régulière.
    
    :param calcul: le calcul à tester
    :type calcul: string
    :param min_i: position à partir de laquelle effectuer le test
    :type min_i: integer

    >>> from pyromaths.outils import Priorites3
    >>> p = '-Polynome([[-4, 2]], "x")*6**2+3'
    >>> Priorites3.cherche_decimal(p, 1)
    '4'
    >>> p = '-6*(-11)*(-5)'
    >>> Priorites3.cherche_decimal(p, 1)
    '6'
    >>> Priorites3.cherche_decimal(p, 0)
    '6'

    :rtype: string
    """
    operateur = ['**', '+', '-', '*', '/', '^']
    l = []
    for op in operateur:
        try:
            l.append(calcul[index:].index(op)+index)
        except:
            l.append(None)
    min_i=0
    for i in range (1, len(l)):
        if l[i] is not None and (l[i] < l[min_i] or l[min_i] is None):
            min_i = i
    if l[min_i] > None:
        return operateur[min_i]
    else:
        return None

def split_calcul(calcul):
    """**split_calcul**\ (*calcul*)

    Partitionne la chaîne de caractères pour obtenir une liste d'opérateurs,
    de parenthèses, de polynômes et de nombres

    :param calcul: le calcul à traiter
    :type calcul: string

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.split_calcul('-Polynome([[-4, 2]], "x")*6**2+3')
    ['-', 'Polynome([[-4, 2]], "x")', '*', '6', '**', '2', '+', '3']
    >>> Priorites3.split_calcul('-6*(-11)*(-5)')
    ['-', '6', '*', '(-11)', '*', '(-5)']
    >>> Priorites3.split_calcul("Polynome('Fraction(1,3)x')+Polynome('x')")
    ["Polynome('Fraction(1,3)x')", '+', "Polynome('x')"]

    **TODO :** vérifier ce dernier exemple. Je pense que je devrais récupérer -6

    :rtype: list
    """
    l = []
    findings = (cherche_classe, cherche_decimal)#, cherche_operateur)
    for finding in findings:
        nb = finding(calcul, 0)
        while nb:
            l.extend(calcul.partition(nb))
            l[-3] = l[-3].strip()
            l[-2] = l[-2].strip()
            l[-1] = l[-1].strip()
            if l[-3] and l[-2]:
                l0 = split_calcul(l[-3])
                if l0:
                    l0.extend(l[-2:])
                    l = l[:-3]
                    l.extend(l0)
            elif not l[-3]:
                l.pop(-3)
            calcul = l[-1]
            nb = finding(calcul, 0)
            l = l[:-1]
    if calcul: l.append(calcul)
    while l and not l[0]:
        l.pop(0)
    return l

def EstNombre(value):
    """**EstNombre**\ (*value*)

    Teste si `value` est une valeur, c'est à dire un entier, un réel, un polynôme, une fraction

    :param value: la valeur à traiter
    :type value: string

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.EstNombre('-15')
    True
    >>> Priorites3.EstNombre('Polynome([[-4, 2]], "x")')
    True

    :rtype: list
    """
    from pyromaths.classes.PolynomesCollege import Polynome
    from pyromaths.classes.Fractions import Fraction
    try:
        return isinstance(eval(value), (float, int, Polynome, Fraction))
    except:
        return False


def splitting(calcul):
    """**splitting**\ (*calcul*)

    Partitionne la chaîne de caractères pour obtenir une liste d'opérateurs,
    de parenthèses, de polynômes et de nombres puis arrange la liste des
    opérandes et opérateurs

    :param calcul: le calcul à traiter
    :type calcul: string

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.splitting('-Polynome([[-4, 2]], "x")*6**2+3')
    ['-', 'Polynome([[-4, 2]], "x")', '*', '6', '**', '2', '+', '3']
    >>> Priorites3.splitting('-6*(-11)*(-5)')
    ['-6', '*', '(-11)', '*', '(-5)']
    >>> Priorites3.splitting("Fraction(1,7)x^2-Fraction(3,8)x-1")
    ['Fraction(1,7)', 'x', '^', '2', '-', 'Fraction(3,8)', 'x', '-', '1']

    :rtype: list
    """
    if calcul == "": return []
    l = split_calcul(calcul)
    if l[0] == "+" and len(l) > 1: l[0] += l.pop(1)
    elif l[0] == "-" and len(l) > 1 and l[1][0] in "0123456789": l[0] += l.pop(1)
    j = 0
    while j < len(l):
        op, i, t = l[j], 0, []
        if op == "**": j+= 1
        else:
            if not EstNombre(op):
                while i < len(op):
                    if op[i:i+2] == "**":
                        t.append("**")
                        i += 2
                    else: 
                        t.append(op[i])
                        i += 1
                l[j:j+1] = t
                j += len(t)
            else: j += 1
    return l

def recherche_parentheses(calcul):
    """**recherche_parentheses**\ (*calcul*)

    Recherche les premières parenthèses (éventuellement intérieures) dans une expression

    :param calcul: le calcul à traiter
    :type calcul: list

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.recherche_parentheses(['-6', '*', '(-11)', '*', '(-5)'])
    >>>
    >>> Priorites3.recherche_parentheses(['-9', '-', '6', '*', '(', '(-2)', '-', '4', ')'])
    (4, 9)

    :rtype: tuple
    """
    if calcul.count("("):
        debut = calcul.index("(")
        if calcul[debut+1:].count(")"): fin = calcul[debut:].index(")") + debut
        else: return None
        for dummy in range(calcul[debut + 1:fin].count("(")):
            debut += calcul[debut+1:].index("(") + 1
        return (debut, fin+1)
    else:
        return None

def recherche_puissance(calcul):
    """**recherche_puissance**\ (*calcul*)

    Recherche la première occurrence d'une puissance dans une liste de
    calculs. Elle doit être entourée de deux nombres.

    :param calcul: le calcul à traiter
    :type calcul: list

    >>> from pyromaths.outils import Priorites3
    >>> c = ['-6', '**', '(-11)', '*', '(-5)']
    >>> Priorites3.recherche_puissance(c)
    (0, 3)
    >>> p = ['-', 'Polynome([[-4, 2]], "x")', '**', '2', '+', '3']
    >>> Priorites3.recherche_puissance(p)
    (1, 4)

    :rtype: tuple
    """
    if calcul.count("**"):
        i = calcul.index("**")
        return (i-1, i+2)
    else:
        return None

def recherche_operation(calcul, op, l_interdit, debut = 0):
    """**recherche_operation**\ (*calcul*\ , *op*\ , *l_interdit*\ [, *debut*])

    Recherche la première occurrence de l'opération op dans la liste de
    calculs list. L'opérateur doit être entouré de deux nombres, le premier ne
    doit pas être précédé d'un opérateur inclus dans la liste l_interdit.
    L'opérateur à trouver doit être avant la position debut (si debut est non
    nul).

    :param calcul: le calcul à traiter
    :type calcul: list
    :param op: l'opérateur à chercher
    :type op: string
    :param l_interdit: liste des opérateurs à ignorer, pour respecter les priorités
    :type l_interdit: list
    :param debut: À partir d'où chercher l'opérateur dans l'expression
    :type debut: integer

    >>> from pyromaths.outils import Priorites3
    >>> c = ['-6', '**', '(-11)', '*', '(-5)']
    >>> Priorites3.recherche_operation(c, "*", ("**", "/"))
    >>>
    >>> c = ['-9', '-', '6', '*', '2', '-', '4']
    >>> Priorites3.recherche_operation(c, "*", ("**", "/"))
    3

    :rtype: integer
    """
    ind, fin = 0, len(calcul)
    for dummy in range(calcul.count(op)):
        ind = calcul.index(op, ind)
        if ind == 1 and ind < fin-1 and EstNombre(calcul[ind-1]) and\
            EstNombre(calcul[ind+1]):
                if debut: debut = min(debut, ind)
                else: debut = ind
                break
        elif ind > 1 and ind < fin -1 and EstNombre(calcul[ind-1]) and\
            EstNombre(calcul[ind+1]) and calcul[ind-2] not in l_interdit:
                if debut: debut = min(debut, ind)
                else: debut = ind
                break
        else:
            ind += 1
    if debut: return debut
    else: return None

def recherche_fin_operation(calcul, op, l_interdit, debut):
    """**recherche_fin_operation**\ (*calcul*\ , *op*\ , *l_interdit*\ , *debut*)

    Recherche la fin de la suite d'opération @op situé à la position @debut
    de la liste de calculs @calcul, en vérifiant que cet enchaînement n'est pas
    suivi par un opérateur compris dans @l_interdit.

    :param calcul: le calcul à traiter
    :type calcul: string
    :param op: l'opérateur à chercher
    :type op: string
    :param l_interdit: liste des opérateurs à ignorer, pour respecter les priorités
    :type l_interdit: list
    :param debut: À partir d'où chercher l'opérateur dans l'expression
    :type debut: integer

    >>> from pyromaths.outils import Priorites3
    >>> c     = ['-9', '-', '6', '*', '2', '*', '5', '-', '4']
    >>> Priorites3.recherche_fin_operation(c, "*", ("**", "/"),0)
    2
    >>> Priorites3.recherche_fin_operation(c, "*", ("**", "/"),4)
    6

    :rtype: integer
    """
    index, fin = debut + 2, len(calcul)
    while index < fin-1 and calcul[index] == op and EstNombre(calcul[index+1]):
        index +=2
    if index < fin and calcul[index] in l_interdit:
        index -=2
    if index == debut: return None
    return index

def recherche_produit(calcul):
    """**recherche_produit**\ (*calcul*)

    Recherche la première occurrence d'une multiplication ou divisions dans
    une liste de calculs. Elle doit être précédée d'un nombre qui ne doit pas
    être précédé d'une puissance ou d'une division, ni suivie d'un exposant.

    :param calcul: le calcul à traiter
    :type calcul: list

    >>> from pyromaths.outils import Priorites3
    >>> c = ['-9', '-', '6', '*', '2', '*', '5', '-', '4']
    >>> Priorites3.recherche_produit(c)
    (2, 7)

    :rtype: tuple
    """
    debut = recherche_operation(calcul, "*", ("**", "/"))
    debut = recherche_operation(calcul, "/", ("**", "/"), debut)
    if debut is not None:
        fin = recherche_fin_operation(calcul, calcul[debut], ("**"), debut)
        if fin is not None: return (debut - 1, fin)
    return None

def recherche_somme(calcul):
    """**recherche_somme**\ (*calcul*)

    Recherche la première occurrence d'une addition ou soustraction dans une
    liste de calculs. Elle doit être précédée d'un nombre qui ne doit pas être
    précédé d'une puissance, d'une multiplication, d'une division ou d'une
    soustraction, ni suivie d'un exposant, d'une multiplaication ou d'une
    division.

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.recherche_somme(['1', '-', '2', '-', '3'])
    (0, 5)
    >>> Priorites3.recherche_somme(['Polynome("x+1")', '-', 'Polynome("x+2")', '-', 'Polynome("x+3")'])
    (0, 5)

    :param calcul: le calcul à traiter
    :type calcul: list
    :rtype: tuple
    """
    debut = recherche_operation(calcul, "+", ("**", "*", "/", "-"))
    debut = recherche_operation(calcul, "-", ("**", "*", "/", "-"), debut)
    if debut is not None:
        fin = recherche_fin_operation(calcul, calcul[debut], ("**", "*", "/"),
                debut)
        if fin is not None: return (debut - 1, fin)
    return None

def recherche_neg(calcul):
    """**recherche_neg**\ (*calcul*)

    Recherche la première occurence d'un opposé `-(-5)` ou `-Polynome` ou
    d'une écriture du style `+(-5)` dans une liste de calculs qui ne doit pas être
    suivie d'un exposant.

    :param calcul: le calcul à traiter
    :type calcul: list
    :rtype: tuple
    """
    ind, debut, fin = 0, None, len(calcul)
    for dummy in range(calcul.count("-")):
        ind = calcul.index("-", ind)
        if ind < fin-1 and EstNombre(calcul[ind+1]):
            if calcul[ind+1][0] == "(":# or isinstance(n, Polynome):
#                or (isinstance(n, Polynome) and (len(n)>1 or n.monomes[0][0]<0)):
                debut = ind
                break
        else:
            ind += 1
    for dummy in range(calcul[ind+1:].count("+")):
        ind = calcul.index("+", ind)
        if ind < fin-1 and EstNombre(calcul[ind+1]) and calcul[ind+1][0] == "(":
            if debut is not None: debut = min(debut, ind)
            else: debut = ind
            break
        else:
            ind += 1
    if debut is not None and (debut+2 == fin or (debut+2<fin and
        calcul[debut+2] != "**")):
        return (debut, debut+2)
    else: return None

def post_polynomes(calcul):
    """**post_polynomes**\ (*calcul*)

    Retourne la liste `calcul` dans laquelle

    * les polynômes sont ordonnés si nécessaire
    * les polynômes sont réduits s'ils sont déjà ordonnés

    :param calcul: le calcul à traiter
    :type calcul: list

    >>> from pyromaths.classes.Fractions import Fraction
    >>> Priorites3.post_polynomes(['Polynome([[1, 2], [-1, 0], [3, 1], [-9, 2], [-8, 1]], "x")'])
    ['Polynome([[1, 2], [-9, 2], [3, 1], [-8, 1], [-1, 0]], "x")']
    >>> Priorites3.post_polynomes(['Polynome([[1, 2], [-9, 2], [3, 1], [-8, 1], [-1, 0]], "x")'])
    ['(', '1', '-', '9', ')', '*', 'Polynome([[1, 2]], "x")', '+', '(', '3', '-', '8', ')', '*', 'Polynome([[1, 1]], "x")', '+', 'Polynome("-1x^0")']

    :rtype: list
    """
    from pyromaths.classes.PolynomesCollege import Polynome
    for k in range(len(calcul)):
        if 'Polynome(' in calcul[k]:
            p = eval(calcul[k])
            if Polynome.reductible(p):
                p = Polynome.reduction_detaillee(p)
                if isinstance(p, Polynome): calcul[k] = repr(p)
                else:
                    if isinstance(p, basestring): p = splitting(p)
                    if (k and calcul[k-1] in "*-") or (k<len(calcul)-1 and calcul[k+1] in "**"):
                        p.insert(0, "(")
                        p.append(")")
                    calcul[k:k+1] = p
    return calcul

def post_fractions(calcul, final = False):
    """**post_fractions**\ (*calcul*,\ [, *final*])

    Retourne la liste `calcul` dans laquelle

    * les produits au numérateur et dénominateur sont effectuée dans les sommes et différences de fractions
    * les produits au numérateur et dénominateur sont simplifiés sinon

    :param calcul: le calcul à traiter
    :type calcul: list
    :param final: si le calcul est fini, simplifie toutes les fractions restantes
    :type final: boolean

    >>> from pyromaths.classes.PolynomesCollege import Polynome
    >>> Priorites3.post_fractions(['Fraction(3*4, 2*4, "r") + Fraction(5, 8)'])
    ['Fraction(12, 8) + Fraction(5, 8)']
    >>> Priorites3.post_fractions(['Fraction(3*4*5, 2*4, "s")'])
    ['Fraction(15, 2)']

    :rtype: list
    """
    from pyromaths.classes.Fractions import Fraction
    e = [calcul[k] for k in range(len(calcul))]
    if final:
        index = 0
        while index < len(e[0]) and 'Fraction(' in e[0][index:]:
            index = e[0].index('Fraction', index)
            splitted = e[0].partition(cherche_classe(e[0], index))
            frac = eval(splitted[1])
            e[0] = e[0][:index] + repr(Fraction.simplifie(frac)) + splitted[2]
            index += 1
        return e
    if len(e) > 1:
        for k in range(len(e)):
            index = 0
            while index < len(e[k]) and 'Fraction(' in e[k][index:]:
                index = e[k].index('Fraction(', index)
                splitted = e[k].partition(cherche_classe(e[k], index))
                frac = eval(splitted[1])
                if frac.code == "s": 
                    e[k] = e[k][:index] + repr(Fraction.simplifie(frac)) + splitted[2]
                elif frac.code == "r":
                    e[k] = e[k][:index] + repr(Fraction.reduit(frac)) + splitted[2]
                index += 1
    else:
        index = 0
        while index < len(e[0]) and 'Fraction(' in e[0][index:]:
            index = e[0].index('Fraction(', index)
            splitted = e[0].partition(cherche_classe(e[0], index))
            frac = eval(splitted[1])
            if frac.code == "s": 
                e[0] = e[0][:index] + repr(Fraction.simplifie(frac)) + splitted[2]
            elif frac.code == "r":
                e[0] = e[0][:index] + repr(Fraction.reduit(frac)) + splitted[2]
            else:
                e[0] = e[0][:index] + Fraction.decompose(frac) + splitted[2]
            index += 1
    return e

def effectue_calcul(calcul):
    """**effectue_calcul**\ (*calcul*)

    Effectue une étape du calcul en respectant les priorités

    :param calcul: le calcul à traiter
    :type calcul: list

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.effectue_calcul(['-5', '-', '(', '(-6)', '-', '1', '+', '(-3)', ')', '*', '(-1)'])
    ['-5', '-', '(', '-7', '-', '3', ')', '*', '(-1)']
    >>> Priorites3.effectue_calcul(['-5', '-', '(', '-7', '-', '3', ')', '*', '(-1)'])
    ['-5', '-', '-10', '*', '(-1)']
    >>> Priorites3.effectue_calcul(['-5', '-', '-10', '*', '(-1)'])
    ['-5', '-', '10']
    >>> Priorites3.effectue_calcul(['-5', '-', '10'])
    ['-15']

    :rtype: list
    """
    from pyromaths.classes.PolynomesCollege import Polynome
    from pyromaths.classes.Fractions import Fraction
    serie = (recherche_parentheses, recherche_puissance, recherche_produit,
            recherche_neg, recherche_somme)
    result, post, break_somme = [], "", False
    for recherche in serie:
        if break_somme and recherche == recherche_somme: break
        if calcul: test = recherche(calcul)
        else: test = None
        while test:
            pre = calcul[:test[0]]
            calc = calcul[test[0]:test[1]]
            post = calcul[test[1]:]
            # On essaie d'utiliser les priorités sur la première partie du
            # calcul pour raccourcir la résolution de l'expression
            if test != recherche_neg and pre:
                # Si on simplifie les écritures, on n'essaie pas les sommes
                tmp = effectue_calcul(pre)
                if tmp and result and result[-1] not in "+-**/(" and tmp[0][0]\
                    not in "+-*/)":
                    # un signe + si l'expression en a besoin
                    result.append("+")
                # On ajoute le résultat ou l'expression
                if tmp: result.extend(tmp)
                else: result.extend(pre)
            else:
                result.extend(pre)
            if recherche == recherche_parentheses:
                # On supprime les parenthèses autour de l'expression
                calc = calc[1:-1]
                # On réduit directement les calculs numériques dans une
                # expression littérale
                sol = effectue_calcul(calc)
                if len(sol)>1:
                    sol.insert(0, "(")
                    sol.append(")")
                elif sol and isinstance(eval(sol[0]), (int, float, Fraction)) and post and post[0] == "*" and \
                        'Polynome(' in post[1] and len(eval(post[1])) == 1 and eval(post[1])[0][0] == 1:
                            # Sans doute une factorisation de sommes de polynômes
                            sol = [repr(eval(sol[0])*eval(post[1]))]
                            post = post[2:]
                            #Suppression des parenthèses autour de ((9.0-80.0)*Polynome("x")) devenu (Polynome("-71.0x"))
                            if post and result and post[0] == ")" and result[-1] == "(" :
                                result,  post = result[:-1],  post[1:]
            else:
                sol = eval("".join(calc))
                if isinstance(sol, basestring): sol = splitting(sol)
                elif isinstance(sol, (int, float)): sol = [str(sol)]
                elif isinstance(sol, (Polynome, Fraction)): sol = [repr(sol)]
                else : raise ValueError(u"Le résultat a un format inattendu")
#             if recherche == recherche_neg and len(sol) > 1:
            if recherche == recherche_neg and pre:
                # Ajoute le "+" ou sépare le "-":
                # "1-(-9)" => "1 + 9" et "1+(-9)" => "1 - 9"
                if sol[0][0] == "-": sol = ["-", sol[0][1:]]
                else: sol = ["+", sol[0]]
            if recherche == recherche_produit and len(sol) > 1:
                # Ajoute les parenthèses si produit précédé d'un "-" ou "*"
                # ou suivi d'un "*"
                if (result and result[-1] in "*-") or (post and post[0] == "*"):
                    sol.insert(0, "(")
                    sol.append(")")
            # Si @sol est négatif et @result se termine par un "+", on l'enlève
            if result and result[-1] == "+" and sol and sol[0][0] == "-":
                    result[-1] = "-"
                    sol[0] = sol[0].lstrip("-")
            result.extend(sol)
            calcul = post
            if calcul: test = recherche(calcul)
            else: test = None
            if post and recherche == recherche_neg: break_somme=True
    result.extend(post)
    if not result: result = calcul
    return result

def priorites(calcul):
    """**priorites**\ (*calcul*)

    Effectue un enchaînement d'opérations contenues dans calcul en
    respectant les priorités et en détaillant les étapes.

    :param calcul: le calcul à traiter
    :type calcul: string

    >>> from pyromaths.outils import Priorites3
    >>> Priorites3.priorites('-1+5-(-5)+(-6)*1')
    [['4', '+', '5', '-', '6'], ['9', '-', '6'], ['3']]

    :rtype: list
    """
    calcul = splitting(calcul)
    solution = []
    while len(calcul)>1:
        s= effectue_calcul(calcul)
        if s:
            s = post_polynomes(s)
            solution.append(s)
            s2 = post_fractions(s)
            if s2 != s:
                solution.append(s2)
                s = [k for k in s2]
        calcul = [k for k in s] # dissocie calcul et s
        if len(calcul) == 1 and post_polynomes(calcul) != s:
            # Finit la réduction du polynôme résultat
            solution.append(calcul)
        if len(calcul) == 1 and 'Fraction(' in calcul[0]:
            s = post_fractions(s, True)
            if s[0] != calcul[0]:
                calcul = [[s[0]]]
                solution.append(calcul[0])
    return solution

def texify(liste_calculs):
    r"""**texify**\ (*liste_calculs*)

    Convertit la liste de chaînes de caractères `liste_calculs` contenant
    des polynômes en liste de chaînes de caractères au format TeX

    **TODO :** intégrer cela dans :mod:`outils.Affichage` et gérer l'ensemble des
    classes de Pyromaths.

    :param calcul: le calcul à traiter
    :type calcul: string

    >>> from pyromaths.outils import Priorites3
    >>> from pyromaths.classes.PolynomesCollege import Polynome
    >>> l = [['4', '+', '5', '-', '6'], ['9', '-', '6'], ['3']]
    >>> Priorites3.texify(l)
    ['4+5-6', '9-6', '3']
    >>> Priorites3.texify(Priorites3.priorites('(-7)+8-Polynome([[-4, 1], [-9, 2], [-5, 0]], "x")'))
    ['1-\\left( -4\\,x-9\\,x^{2}-5\\right) ', '1+4\\,x+9\\,x^{2}+5', '9\\,x^{2}+4\\,x+1+5', '9\\,x^{2}+4\\,x+6']

    :rtype: list
    """
    from pyromaths.classes.PolynomesCollege import Polynome
    from pyromaths.classes.Fractions import Fraction
    ls = []
    for calcul in liste_calculs:
        if isinstance(calcul,  basestring): calcul = splitting(calcul)
        s = ""
        puiss = 0
        for i in range(len(calcul)):
            el = calcul[i]
            if el[:9] == "Polynome(":
                # Doit-on entourer ce polynôme de parenthèses ?
                p = eval(el)
                if i+1 < len(calcul): q = calcul[i+1]
                else: q= ""
                """ 3 cas :
                * {*,-}(2x+3) ou {*,-}(-2x)
                * (2x+3)*...
                * (2x+1)**2"""
                if (s and s[-1] in "*-" and (len(p)>1 or p.monomes[0][0]<0)) \
                    or (q and q == "*" and len(p)>1) \
                    or ((len(p)>1 or p.monomes[0][0]!=1) and q and q == "**"):
                    s += "(" + str(p) +")"
                elif s and s[-1] == "+" and p.monomes[0][0]<0:
                    s = s[:-1]
                    s += str(p)
                else:
                    s += str(p)
            elif el[:9] == "Fraction(":
                # Doit-on entourer cette fraction de parenthèses ?
                p = el[9:-1].split(",")
                if len(p) == 2:
                    texfrac = str(Fraction(eval(p[0]), eval(p[1])))
                else:
                    texfrac = str(Fraction(eval(p[0]), eval(p[1]), eval(p[2])))
                if i+1 < len(calcul): q = calcul[i+1]
                else: q= ""
                if (eval(p[0]) < 0 or p[1] != "1") and q and q == "**":
                    s += "\\left( " + texfrac + " \\right)"
                else:
                    s += texfrac
            elif EstNombre(el):
                if el[0]=="(": s += "(" + decimaux(el[1:-1]) + ")"
                else: s += decimaux(el)
            elif el == "**":
                s += "**{"
                puiss += 1
            elif el == "(":
                if puiss: puiss += 1
                s += "("
            elif el == ")":
                if puiss: puiss -= 1
                s += ")"
            else :
                # "+", "-", "*", "/"
                s += el
            if puiss == 1 and s[-1] != "{":
                puiss = 0
                s += "}"
        s = s.replace("**{", "^{")
        s = s.replace("(", "\\left( ")
        s = s.replace(")", "\\right) ")
        s = s.replace("*", "\\times ")
        s = s.replace("/", "\\div ")
        if not ls or s != ls[-1]:
            ls.append(s)
    return ls

#===============================================================================
# #----------------------------------------------------------------------
# # Pyromaths : FICHIERS DE TESTS
# #----------------------------------------------------------------------
# def valeurs(n, polynomes=0, entier=1):
#     """*fichier de tests :* Renvoie une chaîne de caractères contenant un calcul aléatoire de
#     n nombres, qui sont soit des entiers, soit des décimaux, soit des polynômes."""
#     import random
#     def deci(entier):
#         if entier:
#             return random.randrange(-11, 11)
#         else:
#             return random.randrange(-110, 110)/10.
#     def poly(entier):
#         lg = random.randrange(3)
#         degre=[0, 1, 2]
#         p = [[deci(entier), degre.pop(random.randrange(len(degre)))] for dummy in range(lg+1)]
#         p = Polynome(p, "x")
#         while p == Polynome([[0, 0]], "x"):
#             degre=[0, 1, 2]
#             p = [[deci(entier), degre.pop(random.randrange(len(degre)))] for dummy in range(lg+1)]
#             p = Polynome(p, "x")
#         if len(p) == 1 and Polynome.degre(p) == 0:
#             p = p[0][0]
#             if p < 0: p = "(" + str(p) +")"
#             else: p = str(p)
#         else: p = repr(p)
#         return p
#     if polynomes: nb=poly
#     else: nb=deci
#     nbp = []
#     lo = ['+','*','-']
#     for i in range(n):
#         if not i:
#             s = "%s" % nb(entier)
#         else:
#             if nbp and nbp[-1] > 2 and not random.randrange(2):
#                 s += ')'
#                 nbp.pop(-1)
#             s += lo[random.randrange(3)]
#             if nbp:
#                 for cpt in range(len(nbp)):
#                     nbp[cpt] += 1
#             a = random.randrange(3)
#             if s[-1] in '*-/' and i<=n-2 and not a:
#                 s += '('
#                 nbp.append(1)
#             nombre = nb(entier)
#             if nombre < 0: s += "(" + str(nombre) + ")"
#             else: s += str(nombre)
#             if not polynomes: #TODO: tester les puissances avec les polynômes
#                 a = random.randrange(10)
#                 if (not nbp or nbp[-1]>1) and not a:
#                     s += "**2"
#     while nbp:
#         s += ')'
#         nbp.pop(-1)
#     return s
# 
# def test_entiers(nbval, polynomes, entiers):
#     for c in range(10000):
#         a = valeurs(nbval, polynomes, entiers)
#         try:
#             r = priorites(a)
#             texify(r)
#         except:
#             print(a)
#             break
#         else:
#             if not polynomes:
#                 print u"%s ème calcul" % (c+1), a, " = ", eval(a), u" en %s étapes"%(len(r))
#                 if eval(a) != eval("".join(r[-1])):
#                     print a, " = ", eval(a)
#                     print r
#                     break
#             if polynomes:
#                 from sympy import Symbol, expand
#                 x = Symbol('x')
#                 print u" : %s ème calcul en %s étapes" % (c+1, len(r))
#                 if not len(r):
#                     print a
#                     break
#                 else:
#                     t0=sympyfy([a])[0]
#                     t1=sympyfy(r[-1])
#                     if isinstance(eval(t1[0]), (int, float)) : t1[0] = "%s+x-x" % (t1[0])
#                     if isinstance(eval(t0), (int, float)) : t0 = "%s+x-x" % (t0)
# 
#                     if eval(t0).expand()!=eval(t1[0]).expand():
#                         print a, "=", t1
#                         print "\n".join(sympyfy(r))
# 
#                         print u"Devrait être : ", eval(t0).expand()
#                         break
# 
# def sympyfy(liste_calculs):
#     """*fichier de tests :* Convertit une liste de chaînes de caractères 'liste_calculs' contenant
#     des polynômes en liste de chaînes de caractères au format Sympy"""
#     ls = []
#     for calcul in liste_calculs:
#         if isinstance(calcul,  basestring): calcul = splitting(calcul)
#         s = ""
#         puiss = 0
#         for i in range(len(calcul)):
#             el = calcul[i]
#             if el[:9] == "Polynome(":
#                 # Doit-on entourer ce polynôme de parenthèses ?
#                 p = eval(el)
#                 if i+1 < len(calcul): q = calcul[i+1]
#                 else: q= ""
#                 if (s and s[-1] in "*-" and (len(p)>1 or p.monomes[0][0]<0)) \
#                     or (q and q == "*" and len(p)>1) \
#                     or ((len(p)>1 or p.monomes[0][0]!=1) and q and q == "**"):
#                     s += "(" + str(p) +")"
#                 elif s and s[-1] == "+" and p.monomes[0][0]<0:
#                     s = s[:-1]
#                     s += str(p)
#                 else:
#                     s += str(p)
#             elif EstNombre(el):
#                 if el[0]=="(": s += "(" + decimaux(el[1:-1]) + ")"
#                 else: s += decimaux(el)
#             elif el == "**":
#                 s += "**{"
#                 puiss += 1
#             elif el == "(":
#                 if puiss: puiss += 1
#                 s += "("
#             elif el == ")":
#                 if puiss: puiss -= 1
#                 s += ")"
#             else :
#                 # "+", "-", "*", "/"
#                 s += el
#             if puiss == 1:
#                 puiss = 0
#                 s += "}"
#         s = s.replace("\\,x", "*x")
#         s = s.replace("\\,", "")
#         s = s.replace("**{", "**")
#         s = s.replace("^{", "**")
#         s = s.replace("}", "")
# #        s = s.replace("(", "\\left( ")
# #        s = s.replace(")", "\\right) ")
# #        s = s.replace("**{", "^{")
# #        s = s.replace("*", "\\times ")
# #        s = s.replace("/", "\\div ")
#         if not ls or s != ls[-1]:
#             ls.append(s)
#     return ls
# 
# def main():
#     from sympy import Symbol, expand
#     x = Symbol('x')
#     test_entiers(nbval=13, polynomes=1, entiers=1)
# #    a = valeurs(2, 1, 1)
# #    a = 'Polynome([[8, 2]], "x")*Polynome([[3, 1]], "x")-Polynome([[-3, 0], [4, 2], [10, 1]], "x")*Polynome([[-4, 2], [5, 0], [-11, 1]], "x")-Polynome([[3, 2], [-5, 1]], "x")-(Polynome([[3, 2], [-1, 0]], "x")*Polynome([[3, 2], [1, 0]], "x")*Polynome([[-6, 2], [10, 1], [2, 0]], "x"))*Polynome([[-9, 0], [-7, 2], [8, 1]], "x")-Polynome([[-8, 1]], "x")+Polynome([[-8, 2], [4, 0]], "x")+Polynome([[10, 1]], "x")+Polynome([[-9, 2], [6, 1], [7, 0]], "x")'
# #    print(a)
# ##    s= sympyfy([a])
# #    print sympyfy(priorites(a))
# #    r = texify(priorites(a))
# #    print "\\item $A=", texify([a])[0] , "$\\par"
# #    for i in r:
# #        print "$A=",
# #        print "".join(i),
# #        print "$\\par"
#===============================================================================
