window.QM1_FR = {
  page: {
    '.back-link': '← Tous les chapitres',
    '.hero .eyebrow': 'MÉTHODES QUANTITATIVES 1 · CHAPITRE 1',
    '.hero h1': 'Présentation des données',
    '.hero .lead': 'Organiser, classer et communiquer les données de manière responsable.',
    '.progress-card span': 'Votre progression',
    '.access-card .eyebrow': 'ACCÈS AUX CORRIGÉS',
    '#accessTitle': 'Déverrouiller les corrigés détaillés',
    '.access-card>div>p:last-child': 'Utilisez le code de séance communiqué par votre enseignant. L’accès collectif est vérifié automatiquement.',
    'label[for="accessCode"]': 'Code de séance',
    '#accessCode@placeholder': 'Saisissez le code de séance',
    '#codeForm button': 'Déverrouiller'
  },
  nav: [
    '1 · Vocabulaire statistique',
    '2 · Population, échantillon et biais',
    '3 · Construire une distribution de fréquences',
    '4 · Classes inégales et graphiques responsables',
    '5 · Audit d’un tableau de bord'
  ],
  exercises: {
    '1': {
      level: 'NIVEAU 1 : RECONNAISSANCE', title: 'Vocabulaire statistique',
      question: `<p>Une enquête interroge 240 étudiants de première année sur leur programme, leur mode de transport, leur satisfaction (de 1 à 5), leur nombre d’absences et leur temps de trajet en minutes.</p><ol><li>Identifiez la population, l’unité statistique et les cinq variables.</li><li>Classez chaque variable comme nominale, ordinale, discrète ou continue.</li><li>Donnez une valeur possible pour chaque variable.</li></ol>`,
      hint: 'Classez une variable d’après la signification de ses valeurs, et non d’après la manière dont elle est codée.',
      solution: `<h3>Corrigé détaillé</h3><p><strong>Méthode.</strong> La population est l’ensemble sur lequel porte la question de recherche ; l’unité statistique est une entité sur laquelle les observations sont enregistrées.</p><p><strong>Résultat.</strong> La population correspond aux 240 étudiants interrogés si l’objectif est de décrire ces répondants. L’unité est un étudiant. Le programme et le mode de transport sont des variables qualitatives nominales. La satisfaction est qualitative ordinale : les modalités sont classées, mais les écarts ne sont pas nécessairement égaux. Le nombre d’absences est quantitatif discret puisqu’il est dénombré. Le temps de trajet est quantitatif continu.</p><p><strong>Interprétation.</strong> Un code numérique ne transforme pas automatiquement une variable en variable quantitative : une satisfaction codée de 1 à 5 reste ordinale.</p>`
    },
    '2': {
      level: 'NIVEAU 2 : RAISONNEMENT GUIDÉ', title: 'Population, échantillon et biais',
      question: `<p>KEDGE souhaite connaître le temps de trajet moyen de ses 1 200 étudiants de première année. Un questionnaire en ligne est publié à 8 h ; 180 volontaires répondent avant midi.</p><ol><li>Définissez la population cible et l’échantillon.</li><li>L’échantillon est-il nécessairement représentatif ? Identifiez deux biais plausibles.</li><li>Proposez un meilleur plan d’échantillonnage.</li></ol>`,
      hint: 'Distinguez le groupe sur lequel on souhaite conclure du groupe effectivement observé. La taille ne garantit pas la représentativité.',
      solution: `<h3>Corrigé détaillé</h3><p><strong>Méthode.</strong> Il faut distinguer la population cible du groupe effectivement observé. La représentativité dépend du mécanisme de sélection et pas uniquement de la taille de l’échantillon.</p><p><strong>Résultat.</strong> La population cible comprend les 1 200 étudiants de première année ; l’échantillon contient les 180 volontaires. Le volontariat peut surreprésenter les étudiants les plus engagés. La fenêtre matinale peut sous-représenter ceux qui sont en trajet ou en cours. Une meilleure méthode consiste à tirer aléatoirement des étudiants dans la liste complète, éventuellement en stratifiant par programme ou campus, puis à effectuer des relances et une analyse de la non-réponse.</p><p><strong>Interprétation.</strong> Un échantillon de 180 personnes peut rester biaisé. La sélection aléatoire et la couverture sont plus importantes que le seul nombre de réponses.</p>`
    },
    '3': {
      level: 'NIVEAU 2 : CALCUL GUIDÉ', title: 'Construire une distribution de fréquences',
      question: `<p>Les nombres d’achats effectués par 20 clients sont : 0, 1, 2, 1, 3, 2, 2, 4, 1, 0, 2, 3, 1, 2, 5, 3, 2, 1, 4, 2.</p><ol><li>Construisez les effectifs, les fréquences relatives, les effectifs cumulés et les fréquences cumulées.</li><li>Déterminez la proportion de clients ayant effectué au plus deux achats.</li><li>Choisissez une représentation graphique appropriée et justifiez votre choix.</li></ol>`,
      hint: 'Commencez par ordonner les valeurs distinctes de 0 à 5. La fréquence relative est égale à l’effectif divisé par 20.',
      solution: `<h3>Corrigé détaillé</h3><p><strong>Méthode.</strong> On ordonne les valeurs, on compte chaque occurrence, on divise chaque effectif par <em>n</em> = 20, puis on cumule à partir de la plus petite valeur.</p><div class="table-wrap"><table><thead><tr><th>x</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr></thead><tbody><tr><th>Effectif</th><td>2</td><td>5</td><td>7</td><td>3</td><td>2</td><td>1</td></tr><tr><th>Fréquence</th><td>0,10</td><td>0,25</td><td>0,35</td><td>0,15</td><td>0,10</td><td>0,05</td></tr><tr><th>Effectif cumulé</th><td>2</td><td>7</td><td>14</td><td>17</td><td>19</td><td>20</td></tr><tr><th>Fréquence cumulée</th><td>0,10</td><td>0,35</td><td>0,70</td><td>0,85</td><td>0,95</td><td>1,00</td></tr></tbody></table></div><p><strong>Résultat.</strong> La proportion ayant réalisé au plus deux achats est 14/20 = 70 %. Un diagramme en bâtons convient puisque la variable est discrète.</p><p><strong>Interprétation.</strong> Sept clients, soit 35 %, ont effectué exactement deux achats, tandis que 70 % en ont effectué deux ou moins.</p>`
    },
    '4': {
      level: 'NIVEAU 3 : APPLICATION', title: 'Classes inégales et graphiques responsables',
      question: `<p>Les temps de livraison sont regroupés ainsi : [0,5[ : 20 ; [5,10[ : 30 ; [10,20[ : 40 ; [20,40[ : 20.</p><ol><li>Calculez les amplitudes, les fréquences relatives et les densités d’effectifs.</li><li>Expliquez pourquoi représenter les effectifs comme hauteurs serait trompeur.</li><li>Identifiez la classe modale à partir des densités.</li></ol>`,
      hint: 'Avec des classes d’amplitudes différentes, c’est l’aire de chaque rectangle qui doit représenter la fréquence. Densité = effectif ÷ amplitude.',
      solution: `<h3>Corrigé détaillé</h3><p><strong>Méthode.</strong> Avec des intervalles inégaux, l’aire de l’histogramme, et non sa hauteur, doit représenter la fréquence. La densité d’effectif est égale à l’effectif divisé par l’amplitude.</p><div class="table-wrap"><table><thead><tr><th>Classe</th><th>[0,5[</th><th>[5,10[</th><th>[10,20[</th><th>[20,40[</th></tr></thead><tbody><tr><th>Amplitude</th><td>5</td><td>5</td><td>10</td><td>20</td></tr><tr><th>Effectif</th><td>20</td><td>30</td><td>40</td><td>20</td></tr><tr><th>Fréquence relative</th><td>0,182</td><td>0,273</td><td>0,364</td><td>0,182</td></tr><tr><th>Densité</th><td>4</td><td>6</td><td>4</td><td>1</td></tr></tbody></table></div><p><strong>Résultat.</strong> La classe modale selon la densité est [5,10[. Utiliser les effectifs comme hauteurs exagérerait les classes larges et produirait des aires sans rapport avec les fréquences.</p><p><strong>Interprétation.</strong> Un histogramme correct conserve la fréquence par l’aire des rectangles et permet une comparaison équitable entre classes d’amplitudes différentes.</p>`
    },
    '5': {
      level: 'NIVEAU 4 : SYNTHÈSE', title: 'Audit d’un tableau de bord',
      question: `<p>Un responsable affirme que la satisfaction a « doublé » parce qu’un graphique à axe tronqué passe de 3,8 à 4,2. Il affirme aussi que l’échantillon représente l’école alors que seuls les membres d’une association étudiante ont répondu. Relevez quatre problèmes statistiques, proposez une communication corrigée et formulez une conclusion défendable.</p>`,
      hint: 'Examinez le calcul de variation, l’échelle du graphique, le cadre d’échantillonnage et le domaine auquel la conclusion peut être généralisée.',
      solution: `<h3>Corrigé détaillé</h3><p><strong>Méthode.</strong> Il faut auditer le cadre d’échantillonnage, l’échelle graphique, l’affirmation numérique et le domaine d’inférence.</p><p><strong>Résultat.</strong> Premièrement, 4,2 n’est pas le double de 3,8 : la hausse est de (4,2/3,8 − 1) × 100 = 10,53 %. Deuxièmement, l’axe tronqué amplifie visuellement la variation. Troisièmement, les membres de l’association constituent un échantillon de convenance. Quatrièmement, la moyenne d’une variable ordinale devrait être accompagnée de la distribution complète. Il faut utiliser une échelle clairement indiquée de 1 à 5, montrer les pourcentages par modalité, préciser la taille et le recrutement de l’échantillon, et éviter toute généralisation abusive.</p><p><strong>Interprétation.</strong> Conclusion défendable : « Parmi les membres de l’association ayant répondu, la satisfaction moyenne déclarée est passée de 3,8 à 4,2. Cette hausse de 0,4 point ne peut pas être automatiquement généralisée à l’ensemble des étudiants. »</p>`
    }
  }
};
