Desarrollo de Herramientas de Software — Trabajo Final

Maximiliano A. Eschoyez y Daniel A. Rosso

Resumen

El objetivo de este Trabajo Final es extender las funcionalidades del progra- ma realizado como Trabajo Práctico. El programa a desarrollar tiene como objetivo tomar un archivo de código fuente en C, generar como salida una verificación gra- matical reportando errores en caso de existir, generar código intermedio y realizar alguna optimización al código intermedio.

Consigna

Dado un archivo de entrada en C, se debe generar como salida el reporte de errores en caso de existir. Para lograr esto se debe construir un parser que tenga como mínimo la implementación de los siguientes puntos:

- Reconocimiento de bloques de código delimitados por llaves y controlar balance de apertura y cierre.
  - Verificaciónde la estructura de las operaciones aritmético/lógicas y las variables o números afectadas.
    - Verificación de la correcta utilización del punto y coma para la terminación de instrucciones.
      - Balance de llaves, corchetes y paréntesis.
        - Tabla de símbolos.
          - Llamado a funciones de usuario.

Si la fase de verificacióngramatical no ha encontrado errores, se debe proceder a:

1. detectar variables y funciones declaradas pero no utilizadas y viceversa,
1. generar la versión en código intermedio utilizando código de tres direcciones, el cual fue abordado en clases y se encuentra explicado con mayor profundidad en la bibliografía de la materia,

En resumen, dado un código fuente de entrada el programa deberá generar los si- guientes archivos de salida:

1. La tabla de símbolos para todos los contextos,
1. La versión en código de tres direcciones del código fuente,

Presentación del Trabajo Final

Código Fuente

El código fuente generado para este proyecto y la versión digital del informe en PDF deberánentregarseatravésdelenlacecorrespondiente en elAula Virtual. En dichoenlace se deberá subir un único archivo en formato ZIP conteniendo todos los código fuente que se requieran para la realización del trabajo finaly el informe.

El proyecto a entregar debe responder a las pautas utilizadas en clase, consistentes en un proyecto en Python y ANTLR gestionado con Maven y Git para seguimiento de los cambios. Se deberá copiar en el Aula Virtual y en el informe escrito el enlace al repositorio en GitLab del IUA que aloja al proyecto. Por tratarse de una continuación de los Trabajos Prácticos de clase, debe utilizarse el mismo repositorio. No olvidar etiquetar (tag) el commitcorrespondientes al TP.

Informe Escrito

Se entregará al profesor un informe escrito (en versión digital formato PDF) donde se debe describir la problemática abordada en el trabajo final,el desarrollo de la solución propuesta y una conclusión. El texto deberá ser conciso y con descripciones apropiadas. No se debe incluir el código fuente, sino los textos necesarios para realizar las explica- ciones pertinentes.
