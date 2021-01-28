# String to math
Module permettant de générer est utiliser des formules mathématiques sous forme de chaine de caractères.


Pour importer le module il faut le placer dans les fichiers sources, la commande d'import est : 

```
from string_to_math import compute
```

## La fonction compute()

La fonction compute prend trois paramètres obligatoires:
* string 
* values_table
* variables_order

La fonction retourne un tuple avec en premier élément un bouléen correspondant à la réussite ou non de la génération. 
Si il vaut False alors le deuxième élément est la raison de l'échec
Si il vaut True alors le deuxième élément est la liste contenant tous les résultats (chaque élément correspond à l'image d'une ligne du paramètre values_table).

### Le paramètre string

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

### Le paramètre values_table

C'est un tableau contenant toutes valeurs d'entrée à mettre dans la fonction générée.
Chaque ligne correspond à un antécédant.

### Le paramètre variables_order
C'est une liste contenant l'ordre des variables du tableau d'entrée. Elle indique au programme par quel valeur il doit remplacer chaque variables.


### Mises à jours
Les mises à jours futures permetteront l'utilisation de plus de fonctions mathématiques
