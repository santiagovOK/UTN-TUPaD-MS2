Factory Method
También llamado: Método de Fábrica, Constructor Virtual
Categoría: Creacional (diseño de creación)

Propósito
Factory Method es un patrón de diseño creacional que define una interfaz para la creación de un objeto, pero deja que las subclases decidan qué clase concreta instanciar.

Problema
Estás construyendo una aplicación de mensajería. Cada tipo de mensaje (correo, SMS, fax) necesita ser creado de forma diferente, pero la clase que orquesta el envío no debe saber qué tipo concreto está enviando.
Cada vez que añades un nuevo tipo de mensaje, tendrías que modificar la clase principal, que ya es grande y compartida por otros módulos. El código se vuelve frágil: cualquier cambio en un tipo de mensaje afecta a toda la clase.

Solución
El patrón Factory Method propone extraer la creación de objetos en un método propio de una clase abstracta. Esa clase declara un método de fábrica que devuelve un producto abstracto, y cada subclase concreta lo sobrescribe para crear el producto que le corresponde.
Así, la clase que orquesta el envío trabaja únicamente con el producto abstracto. Para añadir un nuevo tipo de mensaje, basta con crear una nueva subclase de fábrica sin tocar el código existente.

Estructura
La clase Abstract Factory Method declara un método de fábrica que devuelve un producto abstracto.
La interfaz Producto describe el comportamiento común a todos los productos.
Las Clases Producto Concretas implementan el producto real.
Las Clases Fábrica Concretas sobrescriben el método de fábrica para crear el producto concreto correspondiente.

Pseudocódigo
// La clase abstracta declara el método de fábrica.
abstract class Mensaje is
method enviar()
// Las fábricas concretas crean el producto concreto.
class EmailFactory extends Mensaje is
method crearMensaje() is
return new Email()
class SmsFactory extends Mensaje is
method crearMensaje() is
return new Sms()
// El cliente usa el producto a través de la interfaz abstracta.
class Orquestador is
private mensaje: Mensaje
constructor(crear: Mensaje) is
this.mensaje = crear.crearMensaje()
method enviar() is
mensaje.enviar()

Aplicabilidad
 Utiliza Factory Method cuando una clase debe crear un objeto, pero no debe acoplarse a la clase concreta, ya que podría no conocerla de antemano o quieres permitir una extensibilidad futura.
 Úsalo cuando debas añadir nuevas variantes de producto sin modificar el código existente.
 Úsalo cuando el código contenga una gran cantidad de expresiones condicionales que decidan qué clase instanciar.

Pros y contras
 Puedes introducir nuevas variantes de producto sin cambiar el código del cliente (principio de abierto/cerrado).
 Evitas el acoplamiento fuerte entre la clase creadora y las clases concretas.
 El programa se complica porque se introducen nuevas clases e interfaces.
 Las subclases deben conocer las diferencias entre los productos para elegir la adecuada.

Relaciones con otros patrones
Factory Method y Abstract Factory se parecen: ambos crean objetos sin acoplar a las clases concretas. La diferencia es que Factory Method crea un solo tipo de objeto por subclase (y se apoya en la herencia), mientras que Abstract Factory crea familias de objetos relacionados (una clase de fábrica devuelve varios productos compatibles).
Factory Method suele ser el primer paso hacia Abstract Factory: muchos diseños empiezan con Factory Method (más simple) y evolucionan hacia Abstract Factory cuando las familias de productos crecen.