import string
import math

alphabet = [letter for letter in string.ascii_letters]
number_list = [str(i) for i in range(10)]

tokens = {
    'keyword': (['sin', 'cos', 'exp', 'ln', 'acos', 'asin', 'tan'],  # elements
                False,  # est il concatenable
                {
        'separator',  # elements pouvant être à côté
        'operator',
    }),
    'separator': (['(', ')', '{', '}'],
                  False,
                  {
        'keyword',
        'separator',
        'number',
        'identifier',
        'operator'
    }
    ),
    'operator': (['+', '-', '*', '/', '^'],
                 False,
                 {
        'keyword',
        'number',
        'identifier',
        'separator'
    }),
    'number': (number_list + ['.'],
               True,
               {
        'separator',
        'operator',
        'number'
    }),
    'identifier': (alphabet + number_list + ['_',],
                   True,
                   [
        'separator',
        'operator',
        'identifier'
    ]),

}


def get_type_char(char):
    keys_list = []
    for key, value in tokens.items():
        # On cherche si le caractère est présent dans un token
        if char in value[0]:
            keys_list.append(key)

    if keys_list:
        return (True, keys_list)
    return (False, "Syntaxe incorrecte.")


def is_buildable_by(string, type):
    for c in string:
        # On regarde si tous les caractères son dans le token "type"
        c_type = get_type_char(c)
        if c_type[0] == False:
            return c_type
        elif type not in c_type[1]:
            return (True, False)
    return (True, True)


def besidable_dict(my_key):
    besible_dict = dict()
    for key, value in tokens.items():
        if key in tokens[my_key][2]:  # on récupère les éléments de tokens qui peuvent
            besible_dict[key] = value  # être à côté de notre mot

    return besible_dict


def get_type_notfixed(string, preced_type):
    for preced_key in preced_type:
        for key, value in besidable_dict(preced_key).items():
            # On regarde si la chaine est présente dans un token ou si elle
            # est construisible dans un token qui accepte la concatenation
            key_build_string = is_buildable_by(string, key)
            if key_build_string[0] == False:
                return key_build_string
            elif string in value[0] or (key_build_string[1] and is_concatenable(key)):
                return (True, key)
    return (False, "Syntaxe incorrecte.")


def get_type_fixed(string):
    for key, value in tokens.items():
        # On regarde si la chaine est présente dans un token ou si elle
        # est construisible dans un token qui accepte la concatenation
        key_build_string = is_buildable_by(string, key)
        if key_build_string[0] == False:
            return key_build_string
        elif string in value[0] or (key_build_string[1] and is_concatenable(key)):
            return (True, key)
    return (False, "Syntaxe incorrecte.")


def is_concatenable(type):
    # On récupère si le type accepte la concatenation
    return tokens[type][1]


def lexing(string):
    lexing_list = []
    str_without_space = []
    lexing_without_type = []

    # On retire tous les espaces de la chaîne
    for char in string:
        if char != ' ':
            str_without_space.append(char)

    # On crée le lexing
    for i in range(len(str_without_space)):
        # Pour chaque element de la liste sans espaces
        # On récupère le caractère actuel et le précèdant
        # On vérifie s'il sont concatenable et si ils sont du même type
        # On les concatène dans la même chaine et les rajoute dans la liste

        charac = str_without_space[i]  # Carac actuel

        if i-1 >= 0:  # Carac précèdant
            charac_preced = str_without_space[i-1]
            type_char_prec = get_type_char(charac_preced)
            if type_char_prec[0] == False:
                return type_char_prec
            charac_type = get_type_notfixed(
                charac, type_char_prec[1])  # son type
        else:
            charac_preced = ''
            charac_type = get_type_char(charac)
            
        if charac_type[0] == False:
            return charac_type

        if not lexing_without_type or charac_type[1] not in get_type_char(charac_preced)[1] or not is_concatenable(charac_type[1]):
            # Si liste vide ou d'un type différent ou non concaténable
            # On rajoute le caractère
            lexing_without_type.append(charac)
        else:
            # Sinon on la rajoute a l'élément précédant de la liste
            lexing_without_type[-1] += charac

    # On remplie la liste finale avec le type de chaque élément
    for element in lexing_without_type:
        type_fixed_elmt = get_type_fixed(element)
        if type_fixed_elmt[0] == False:
            return type_fixed_elmt
        lexing_list.append((type_fixed_elmt[1], element))
        lexing_list = minus(lexing_list) # Rajout des zéros pour les nombres négatifs
    return (True, lexing_list)


def get_element(block):
    try:
        return block[1][0]
    except:
        return ' '
# Fonction donnant la possiblité d'utilisation des nombres négatifs dans la chaine parsé
def minus(lexing_list): 
    zero = ('number', '0')
    if get_element(lexing_list[-1]) == '-': # On rajoute simplement un zéro si le signe moins correspond à un nombre négatif (pas à l'opération)
        if len(lexing_list) < 2:
            lexing_list.insert(0, zero)
        elif get_element_type(lexing_list[-2]) != 'number' and get_element_type(lexing_list[-2]) != 'identifier':
            lexing_list.insert(-1, zero)
    return lexing_list


def count_parentheses(lexing_ch):
    # Fonction vérifiant que le nombre de parenthèses ouvrante est égale au notre de parenthèse fermante
    left_count = 0
    right_count = 0
    for element in lexing_ch:
        if get_element(element) == '(': left_count += 1
        elif get_element(element) == ')': right_count += 1
    if left_count == right_count:
        return (True, )
    else:
        return (False, 'Parenthèses en trop ou manquantes.')

def get_variables(lexing_ch):
    variables_list = list()
    for element in lexing_ch:
        if get_element_type(element) == 'identifier':
            variables_list.append(element[1])
    return variables_list


def blocked_parentheses(lexing_ch, sous_chaine=None, index=0):
    # Fonction qui transforme les parenthèses en blocs
    if len(lexing_ch) != 0:
        if get_element_type(lexing_ch[-1]) == 'keyword':
            lexing_ch.pop()
    if sous_chaine != None:
        lexing_ch.insert(index, sous_chaine)
    for i in range(len(lexing_ch)):
        if lexing_ch[i][1] == ')':  # cherche la première parenthèse fermante
            chaine = []
            for k in range(i, -1, -1):  # puis on cherche la prenthèse ouvrante correspondante
                if lexing_ch[k][1] == '(':
                    lexing_return = lexing_ch[:k] + \
                        lexing_ch[i+1:]  # on crée le bloc
                    # on fait cela récursivement
                    try:
                        if get_element_type(lexing_ch[k-1]) == 'keyword':
                            chaine.insert(0, lexing_ch[k-1])
                            return blocked_parentheses(lexing_return, ('NODE', chaine), k-1)
                        else:
                            return blocked_parentheses(lexing_return, ('NODE', chaine), k)

                    except:
                        blocked_parentheses(lexing_return, ('NODE', chaine), k)

                elif k != i and get_element_type(lexing_ch[k]) != 'keyword':
                    # on rajoute des éléments dans notre bloc
                    chaine.insert(0, lexing_ch[k])

    return ('NODE', lexing_ch)


def get_element_type(element):  # retourne le type d'un bloc
    try:
        return element[0]
    except:
        return ' '


def get_block_type(block):
    try:
        return block[1][0][0]
    except:
        return ' '


def get_block_type_mid(block):
    try:
        return block[1][1][0]
    except:
        return ' '

def get_operation(node):  # retourne l'opération d'un bloc
    try:
        return node[1][1][1]
    except:
        return ' '


def get_keyword(node):  # retourne l'opération d'un bloc
    try:
        return node[1][0][1]
    except:
        return ' '


# vérifie si un bloc est déjà un bloc fermé (ne pas accumulé de blocs inutiles)
def already_block(complet_list):
    return len(complet_list) == 3


def block_with_operation(element, operations_list, index=0, complet_list=None, left_bloc=None):
    # crée un bloc en fonction d'opérations
    element_type = get_element_type(element)
    final_list = []
    if element_type == 'NODE':
        # Si notre bloc est un noeud
        for i in range(len(element[1])):
            # On parcours tous les éléments du bloc à la recherche d'une opération
            left_condition       = True  # Est ce que l'operateur de gauche est l'operateur étudié
            right_condition      = True  # Est ce que l'operateur de droite est un autre operateur
            already_in_condition = False
            if len(final_list) > 0:  # si on n'est pas au début du bloc (il y a un élément gauche forcément)
                # On crée le bloc enfant récursivement
                child_bloc = block_with_operation(
                    element[1][i], operations_list, i, element, final_list[-1])

                # On vérifie les conditions afin de garder le bloc enfant ou non
                left_condition = get_operation(
                    final_list[-1]) not in operations_list
                right_condition = (get_element_type(child_bloc) == 'operator' or get_block_type(
                    child_bloc) == 'operator') and (not left_condition or get_operation(child_bloc) not in operations_list)

                # Condition de garde ou non de l'élément gauche (si op à droite alors on le suppr)
                operation_condition = get_operation(
                    child_bloc) in operations_list
                if operation_condition and element[1][i] != child_bloc:
                    final_list.pop()

            else:  # si on est au début (il n'y a pas d'élément gauche)
                child_bloc = block_with_operation(
                    element[1][i], operations_list, i, element)

            # Si notre bloc enfant existe et qu'il est autorisé à être garder alors on le rajoute
            if len(final_list) > 0 and get_element_type(final_list[-1]) == 'NODE':
                already_in_condition = child_bloc in final_list[-1][1]

            if len(child_bloc[1]) != 0 and (left_condition or right_condition) and not already_in_condition:
                final_list.append(child_bloc)
    else:

        # On vérifie que ce bloc est une opération
        # Et on crée un nouveau bloc avec les éléments gauches et droites de l'opération

        if element[1] in operations_list and not already_block(complet_list[1]):
            return ('NODE', [left_bloc, element, complet_list[1][index + 1]])
        else:  # Si non on rajoute l'élément sans modifs
            return element

    # On retourne la liste finale avec tous les blocs créés
    return ('NODE', final_list)

def operator_calc(operator, var_1, var_2):
    if operator == '+':
        return (True, var_1 + var_2)
    elif operator == '-':
        return (True, var_1 - var_2)
    elif operator == '*':
        return (True, var_1 * var_2)
    elif operator == '/':
        try:
            return (True, var_1 / var_2)
        except ZeroDivisionError:
            return(False, 'Division par zéro.')
    else:
        return (True, var_1 ** var_2)


def keyword_calc(keyword, var):
    if keyword == 'cos':
        return (True, math.cos(var))
    elif keyword == 'sin':
        return (True, math.sin(var))
    elif keyword == 'exp':
        return (True, math.exp(var))
    elif keyword == 'ln':
        try:
            return (True, math.log(var))
        except ValueError:
            return(False, 'Valeur nulle ou négative dans un logarithme.')
    elif keyword == 'acos':
        try:
            return (True, math.acos(var))
        except ValueError:
            return(False, 'Valeur supérieur à 1 dans un arcos')
    elif keyword == 'asin':
        try:
            return (True, math.asin(var))
        except ValueError:
            return(False, 'Valeur supérieur à 12 dans un arcos')
    else:
        try: 
            return (True, math.tan(var))
        except ValueError:
            return(False, "Tangente dont le cosinus s'annule")

    
    
# Fonction qui calcul à partir d'une chaine parsé le résultat de la fonction à partir des variables données en paramètres
def calc(parsing_ch, variable_dict):
    # Parcours récursif de la fonction mathématique parsé
    # Si l'élément est un noeud, on regarde le sous-élément du noeud
    if get_element_type(parsing_ch) == 'NODE':
        # Si le sous-élément est une relation d'opération, on réalise donc l'opération correspondant et en calculant les sous-sous-éléments de l'opération
        if get_block_type_mid(parsing_ch) == 'operator':
            var_1 = calc(parsing_ch[1][0], variable_dict)
            var_2 = calc(parsing_ch[1][2], variable_dict)
            if var_1[0] == True and var_2[0] == True:
                return operator_calc(get_operation(parsing_ch), var_1[1], var_2[1])
            elif var_1[0] == False:
                return var_1
            else:
                return var_2
        # Si le sous-élément une fonction prédéfinie on calcule la valeur en calculant le sous-sous-élément
        elif get_block_type(parsing_ch) == 'keyword':
            var_1 = calc(parsing_ch[1][1], variable_dict)
            if var_1[0] == True :
                return keyword_calc(get_keyword(parsing_ch), var_1[1])
            else:
                return var_1
        else:  # Si le sous-élément est un noeud, on le parcours
            return calc(parsing_ch[1][0], variable_dict)
    # Si l'élément n'est pas un noeud, c'est alors un nombres ou une variable
    elif get_element_type(parsing_ch) == 'number':
        return (True , float(parsing_ch[1]))  # Nombre que l'on convertit
    else:
        # Variable, dont on récupère la valeur à partir du dictionnaire donné en paramètre
        if parsing_ch[1] == 'pi': # Récupérer le nombre pi
            return(True, math.pi)
        else:
            return (True, variable_dict[parsing_ch[1]])

# Fonction permettant le calcul de plusieurs résultats avec différents valeur pour chaque variables dans une même fonction
def calc_values_table(parsin_ch, values_table, variables_order):
    results = []
    for line in values_table:  # On parcours chaque ligne du tableau
        variables_dict = {}
        # On détermine le résultat corresondant à la ligne
        for index, value in enumerate(line):
            variables_dict[variables_order[index]] = value
        # On rempli la liste des résultats
        result = calc(parsin_ch, variables_dict)
        if result[0] == True:
            results.append(result[1])
        else:
            return result
    return (True, results)

    
class Str_math_formula():

    def __init__(self, str_formula ):
        self.str = str_formula
        self.lexing_str = lexing(self.str)
        self.variables = get_variables(self.lexing_str[1])

    def is_valid(self):
        if self.lexing_str[0] == False:
            return self.lexing_str

        # Création de blocs en fonctions de parenthèses
        parentheses_check = count_parentheses(self.lexing_str[1])
        if parentheses_check[0] == False:
            return parentheses_check

        return (True, ' ')

    def are_variables_valid(self,  variables_order):
        for variable in self.variables:
            if variable not in variables_order and variable != 'pi':
                return (False, "{} n'appartient pas à la liste d'entrées.".format(variable))
        if 'pi' in variables_order:
            return (False, 'pi ne peut pas être une variable')

        return (True, ' ')
        
    def compute(self, values_table, variables_order):
        is_str_valid = self.is_valid()
        are_values_valid = self.are_variables_valid(variables_order)
        is_formula_valid =  is_str_valid[0] and are_values_valid[0]
        if is_formula_valid:
            parentheses_str = blocked_parentheses(self.lexing_str[1])
            # Création des noeuds en fonction de l'operation puissance
            parsing_str = block_with_operation(parentheses_str, ['^'])
            # Création des noeuds en fonction de l'operation multiplication
            parsing_str = block_with_operation(parsing_str, ['*', '/'])
            # Création des noeuds en fonctoin de l'operation addition
            parsing_str = block_with_operation(parsing_str, ['+', '-'])
            # Calcul des résultats
            results = calc_values_table(parsing_str, values_table, variables_order)
            return results
        else:
            if not is_str_valid[0]:
                return is_str_valid
            else:
                return are_values_valid

        
