**FREE
// --------------------------------------------------
// Erreur API ERRC0100
// BytesProvided : Nombre d'octets fournis par l'application appelante pour le code d'erreur. 
//                 Si l'appelant de l'API utilise le format ERRC0100, les octets fournis doivent être 0, 8 ou plus de 8. 
//                 Si plus de 32 783 octets (32 Ko pour les données d'exception plus 16 octets pour les autres champs) sont spécifiés, 
//                 il ne s'agit pas d'une erreur, mais seuls 32 767 octets (32 Ko) peuvent être renvoyés dans les données d'exception.
// BytesAvailable: Octets disponibles. Longueur des informations d'erreur que l'API peut renvoyer, en octets. 
//                 S'il vaut 0, aucune erreur n'a été détectée et aucun des champs qui suivent ce champ dans la structure n'est modifié.
// Exception ID. L'identifiant du message pour la condition d'erreur.
// --------------------------------------------------    
       DCL-DS ApiError qualified;
          bytesProvided     int(10) inz(%size(ApiError));
          bytesAvailable    int(10) inz(0);
          exceptionId       char(7);
          *n                char(1);
          exceptionData     char(3000);
       END-DS; 