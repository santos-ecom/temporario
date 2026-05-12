import re

with open("index-fr.html", "r", encoding="utf-8") as f:
    text = f.read()

replacements = {
    # Title
    "FoieGras – Atlas Library": "High Protein Low Carb – Atlas Library",
    
    # Hero text
    "Retenez-vous\n                            votre respiration à chaque fois que votre médecin parle de votre foie... mais n'avez\n                            toujours aucune idée de ce que vous êtes censé manger ?": "Mangez de façon saine, équilibrée et revitalisez votre corps. Parfait pour la perte de poids, la prise de muscle, et les journées bien remplies ! Mettez fin aux recettes compliquées !",
    "Vous n'êtes pas le seul.": "Aucune compétence culinaire complexe requise.",
    "Et vous ne faites rien de mal.": "Vous débutez avec un régime riche en protéines et faible en glucides sans savoir par où commencer ?",
    "La plupart des gens diagnostiqués avec un foie gras s'entendent dire :\n                    « Perdez du poids. Mangez plus sainement. »": "Fatigué des recettes difficiles qui demandent des compétences poussées ou qui sacrifient la saveur au profit de la nutrition ?",
    "Ensuite, ils sont renvoyés chez eux sans véritable plan. Aucun\n                    exemple de repas. Aucune structure étape par étape.": "Voici plus de 100 recettes soigneusement sélectionnées — parfaites pour soutenir la perte de poids, le gain musculaire et votre énergie ! Découvrez aussi nos astuces de préparation pratiques.",
    
    # Package Title - trying to match both possible ones just in case
    "Le Livre de Recettes Complet pour le Foie Gras pour\n                                                Débutants + 2\n                                                BONUS": "Pack Ultime : High Protein Low Carb + 2 BONUS",
    "The Complete Fatty Liver Diet Cookbook for Beginners + 2\n                                            BONUSES": "Pack Ultime : High Protein Low Carb + 2 BONUS",
    
    # Bundle name
    "Le Pack Complet du Livre de Recettes pour le Foie Gras pour Débutants": "Le Guide Ultime High Protein Low Carb pour Débutants",
    
    # Points intro
    "Le Livre de Recettes Complet du Régime pour le Foie Gras (Édition 2026) comprend :": "Ce pack extraordinaire de 3 livres comprend :",
    
    # Book 1
    "Un guide nutritionnel sur le foie gras adapté aux débutants": "Livre 1 : High Protein & Low Carb pour Débutants",
    "Des explications claires sur ce qui aide votre foie — et ce qui joue contre lui en silence — sans\n                        jargon médical déroutant.": "Des instructions étape par étape claires et faciles à suivre pour chaque recette riche en protéines, de la préparation des ingrédients à l'assaisonnement final.",
    
    # Book 2
    "+ de 100 recettes savoureuses et respectueuses de votre foie": "Livre 2 : Super Easy High Protein Low Carb Cookbook",
    "De vrais repas avec de vrais ingrédients. D'inspiration méditerranéenne, rassasiants et approuvés par toute la famille.": "Des plats simples, accessibles et savoureux qui vous rassasient plus longtemps et réduisent vos envies de sucre. Sans ingrédients onéreux !",
    
    # Book 3
    "Un plan de repas structuré sur 28 jours": "Livre 3 : 124 Recettes Protéinées par Heather Choate",
    "Plus de devinettes. Plus de fatigue décisionnelle. Suivez simplement le plan et reprenez le contrôle.": "Écrit par Heather Choate (mère de 8 enfants), brûlez les graisses naturellement avec + de 120 repas réparateurs prêts en - de 20 minutes (budget économique).",
    
    # Feature 4
    "Stratégies alimentaires anti-inflammatoires": "Nutrition détaillée pour chaque plat",
    "Découvrez comment réduire l'inflammation de votre foie tout en continuant à profiter des aliments que vous aimez.": "La répartition complète (calories, protéines, glucides, graisses, fibres, etc.) accompagne chaque repas pour adapter facilement vos objectifs.",
    
    # Feature 5
    "Listes de courses hebdomadaires": "Plans de Repas de 14, 30 et 60 jours",
    "Conçues pour vous faire gagner du temps, de l'argent et éviter le stress au supermarché.": "Un panel de plans d'action inclus pour maintenir votre constance sans aucun stress, sans avoir besoin de deviner ce que vous allez cuisiner ce soir.",
    
    # Feature 6
    "Repas favorisant un bon poids corporel — sans régime draconien": "Photos colorées et appétissantes",
    "Créés pour encourager une perte de poids progressive et durable, pas des extrêmes à court terme.": "Mangez d'abord avec les yeux ! Obtenez des résultats réels avec des repas réconfortants et sains (y compris pizzas, crêpes et hamburgers).",
    
    # Feature 7
    "Conseils et motivation pour créer de bonnes habitudes": "Astuces géniales de stockage et gestion",
    "Pour que cela devienne un changement de mode de vie — pas juste un autre livre qui prend la poussière.": "Économisez du temps et réduisez le gaspillage alimentaire ! Des experts vous montrent comment bien préparer en grandes quantités et conserver pour les jours intenses.",
    
    # Testimonials heading / why wait
    "Le foie gras s'améliore\n                            quand…": "Alimentez-vous intelligemment. Sentez-vous plus fort.\n                            Soyez constant…",
    "…l'inflammation diminue et la sensibilité à l'insuline\n                        s'améliore.": "…grâce à plus de 120 recettes créées pour les vies bien remplies.",
    
    "Si vous vous sentez :": "Si vous luttez tous les jours contre :",
    "👉 anxieux concernant la santé de votre foie": "👉 les envies de sucre incontrôlables",
    "👉 frustré par les conseils contradictoires": "👉 le manque d'énergie chronique et le métabolisme lent",
    "👉 dépassé à chaque fois qu'il faut cuisiner": "👉 l'effet yoyo épuisant des régimes fades et monotones",
    "👉 ou inquiet que les choses empirent si vous n'agissez pas": "👉 l'évanouissement énergétique après des séances de sport",
    
    "Vous n'avez pas besoin d'être parfait(e).": "Ce n'est pas un énième régime triste avec du brocoli.",
    "Vous n'avez pas besoin d'extrêmes.": "C'est l'évolution riche en protéines",
    "Vous avez juste besoin d'un": "dont votre corps et votre",
    "plan clair et adapté": "budget ont réellement besoin",
    "qui s'intègre à la vraie vie.": "sans avoir à dépenser une fortune.",
    
    "— moins\n                        que le prix d'un repas à emporter, mais quelque chose qui peut vraiment changer comment vous vous sentez": "— un investissement bien moindre qu'un fast-food, pour changer radicalement vos habitudes et objectifs !",
    
    "Prenez le contrôle de la santé de votre foie dès aujourd'hui calmement, avec confiance, et sans\n                            renoncer": "Ne laissez plus passer cette chance unique de propulser vos objectifs musculaires / perte de poids sans",
}

for k, v in replacements.items():
    text = text.replace(k, v)

# Also fix any straggler instances of The Complete Fatty Liver Diet Cookbook...
text = re.sub(r'The Complete Fatty Liver Diet Cookbook for Beginners \+ 2\s+BONUSES', 'Pack Ultime : High Protein Low Carb + 2 BONUS', text)

with open("proteinafrances.html", "w", encoding="utf-8") as out:
    out.write(text)

print("proteinafrances.html generated successfully.")

