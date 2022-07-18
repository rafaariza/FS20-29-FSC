https://andrewwalker.github.io/statefultransitions/post/gaussian-fields/
https://github.com/bsciolla/gaussian-random-fields
http://www.columbia.edu/~ap3020/LensTools/html/examples/gaussian_random_field.html
https://www.youtube.com/watch?v=_llA2q1rlSg
https://www.youtube.com/watch?v=chsLw2siRW0
https://www.forbes.com/sites/startswithabang/2019/05/11/ask-ethan-how-well-has-cosmic-inflation-been-verified/#2ae7ecd81d07
http://physics.princeton.edu/~steinh/0411036.pdf
https://astro.uchicago.edu/~andrey/talks/PM/pmpotsdam.pdf (pag 41)

*Lo que hemos hablado hoy brevemente es que para obtener el campo de densidad rho(r vector) a partir del espectro de potencias P(k vector) es usar la idea dada en la página 41 de este PDF (aunque no haremos exactamente esto, pero sí muy parecido): https://astro.uchicago.edu/~andrey/talks/PM/pmpotsdam.pdf*

*Básicamente: el espectro de potencias me da la varianza (el cuadrado de la desviación típica, es decir cómo de altas son las fluctuaciones) pero no en el espacio real sino en el espacio de Fourier. Resulta que (y esto tendremos que verlo cuando veamos un poco acerca de inflación) en el espacio de Fourier, cada k vector (que llamaremos "modo de Fourier") es independiente de los demás, con lo que el análisis en el espacio de Fourier se simplifica. No será así en el espacio real, donde fluctuaciones de distinta anchura, aunque estén centradas en puntos distintos, pueden solapar en una misma región, y por tanto las fluctuaciones no son independientes en el espacio real.*

*Por tanto, para un espectro de potencias P(k) dado, simplemente tendremos que generar números aleatorios gaussianos para cada k vector, cuya media sea cero y cuya desviación típica sea la raíz cuadrada de P(k). A esto le llamaremos una "realización" de dicho campo aleatorio, porque si al ejecutarlo de nuevo nos hubieran salido otros números aleatorios, el resultado cambiaría (pero sus propiedades estadísticas no). Para generar dichos números aleatorios podemos usar rutinas propias de Python o el algoritmo de Box-Muller https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform*

*La forma funcional del espectro de potencias la vamos a fijar a k^n (scale-free, que es lo que predice inflación) y por tanto exploraremos los casos n=1 (Harrison-Zel'dovich) , n<1 (red-tilted, porque las escalas grandes tienen más fluctuaciones), n>1 (blue-tilted, porque las escalas pequeñas tienen más fluctuaciones), simplemente tendremos que calcular los coeficientes (complejos) de cada modo, de forma que al hacer la transformada de Fourier me quede un número real (por tanto el coeficiente asociado a un vector k ha de imponerse que sea el complejo conjugado del coeficiente asociado al vector opuesto -k). Por tanto, hay que tener cuidado con esto.*

*El resto es saber usar la FFT en 3D, y discretizar el espacio de Fourier en "cubos". Para ello está bien consultar el libro "Numerical Recipes", que por cierto, está en las referencias recomendadas en la ayuda del algoritmo FFT de numpy: https://numpy.org/doc/stable/reference/routines.fft.html#module-numpy.fft . El resultado será el campo de densidad (en el espacio real) en 3D, que podremos visualizar tomando rodajas en dicho espacio usando el comando meshgrid: https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html*

**SEMANA 2**

*¿No debería ser la ifft de k a x?*

*Sentido de lo que me sale en 1D.*

*Valor central real por condición hermiticidad.*

*¿P(k)?*

**SEMANA X (resolvimos lo de las sigmas)**

* *Al final de inflación (t=0) es cuando el campo escalar encuentra su mínimo.*

* *Oscila alrededor de este punto con fluctuaciones cuánticas.*

* *Estas fluctuaciones están amplificadas por la expansión exponencial del espacio.*

* *Hay una transición de un estado con densidad muy baja y alta energía potencial a otro donde las partículas del SM son creadas y tiene mucha energía (reheating)*

*Inflación surge para resolver:*

* *El problema de la plenitud del horizonte*

* *Monopolos magnéticos*

* *El fondo de ondas gravitacionales debería estar ahí*

**RESULTADOS - MATERIALES Y MÉTODOS (ENTORNO, HERRAMIENTAS MATEMÁTICAS) - INTRODUCCIÓN (ECUACIONES) - OBJETIVOS - CONCLUSIONES - ABSTRACT - BIBLIOGRAFÍA**