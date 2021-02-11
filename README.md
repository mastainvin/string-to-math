# String to math
Module permettant de générer est utiliser des formules mathématiques sous forme de chaine de caractères.


Pour importer le module il faut le placer dans les fichiers sources, la commande d'import est : 

```
from string_to_math import compute
```

## La classe Str_math_formula(str)

### Le paramètre str

C'est la chaine de caractère représentant votre fonction mathématique.

#### Syntaxe de la chaine
Le module dispose d'une syntaxe simple et correspondant à la réalité (règles de calcul)
##### Variables
On peut utiliser toutes les combinaisons de lettres désirées à part 'pi' (car pi est réservé pour la valeur) ainsi que le symbole '_'
##### Opérateurs
addition +, soustraction -, division /, multiplication * et exposant ^ 
##### Racine carrée
()^(1/2)
##### Exponentielle et Logarithme
exp() et ln()

e = exp(1)
##### Fonctions trigonométriques
cos(), sin(), tan()

arcos() et arcsin() s'écrivent acos() et asin()

Les angles sont à mettre en radians

Prend en paramètre la chaine de caractère de la fonction mathématique.

### Attributs :
* str : chaine de caractère initiale
* lexing_str : chaine de caractère après passage dans la fonction de lexing
* variables : liste contenant les variables de la formule

### méthodes:

#### is_valid()
Permet de savoir si la chaine est valide
#### are_variables_valid(variables_order) 
Permet de savoir si les variables que l'on donne sont valident
#### Compute
La méthode compute prend deux paramètres obligatoires:
* values_table
* variables_order


### Le paramètre values_table

C'est un tableau contenant toutes valeurs d'entrée à mettre dans la fonction générée.
Chaque ligne correspond à un antécédant.

### Le paramètre variables_order
C'est une liste contenant l'ordre des variables du tableau d'entrée. Elle indique au programme par quel valeur il doit remplacer chaque variables.


### A savoir
Toutes les méthodes et l'attribut lexing_str retournent un tuple avec en premier élément un bouléen correspondant à la réussite ou non de la génération. 
Si il vaut False alors le deuxième élément est la raison de l'échec
Si il vaut True alors le deuxième élément est la liste contenant tous les résultats (chaque élément correspond à l'image d'une ligne du paramètre values_table).



### Mises à jours
Les mises à jours futures permetteront l'utilisation de plus de fonctions mathématiques
