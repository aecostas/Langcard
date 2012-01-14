#!/usr/bin/python
# http://www.aclevername.com/articles/python-webgui/#a-complete-example

# Ejemplo de widget con WebKit
#
# Author: Wil Alvarez (aka Satanas)
# Oct 20, 2009
import Queue
import gtk
import webkit
import gobject
gobject.threads_init()

# Codigo HTML que insertaremos al control para que lo muestre
ABOUT_PAGE = """
<html><head><title>PyWebKitGtk</title>

<script type="text/javascript">

function send(msg) {
    document.title = "null";
    document.title = msg;
}

function alerta() {
alert("alerta en javascript");

send("'python_print'");
}

</script>

</head><body>
<h1>Mi primera prueba con PyWebKit</h1>
<p><a href="http://code.google.com/p/pywebkitgtk/">http://code.google.com/p/pywebkitgtk/</a><br/>
</p>
<div style="border: 1px solid #000; width:300px; height: 100px; background-color:#aaa;">
  zOMG! This is fucking awesome<br/><br/>
  No se que mas poner en este div con estilos css  XDDD
</div>
</body></html>
"""

# Clase donde sobreecribimos el widget WebView de WebKit para implementar
# nuestro codigo y hacer uso del load_string para inyectar HTML directamente
# sobre el control (sin usar URI o algo similar)
class MessageStreamView(webkit.WebView):
    def __init__(self):
        webkit.WebView.__init__(self)
#        self.connect("navigation-requested", self.on_click_link)
        
        self.settings = webkit.WebSettings()
        self.set_settings(self.settings)

        self.connect('load-finished', self.onloadevent)
        print "loading string"
        # Recibe como parametros el codigo HTML, el mime-type de la pagina,
        # la codificacion y un URI
        self.load_html_string(ABOUT_PAGE, "file:///")
 #       self.load_uri("www.google.es")
        
        self.execute_script('alerta("asdf")');
        
    def onloadevent(self, view, frame):
        print "load-finished"
        # para llamar a funciones javascript definidas por nosotros
        # es necesario que la pagina se haya cargado ya lo cual 
        # se asegura con el evento 'load-finished'
        self.execute_script('alerta("asdf")');


    def on_click_link(self, view, frame, req):
        uri = req.get_uri()
        print uri
        return True

# Creamos una ventana simple en PyGTK con el control que acabamos de crear y 
# voila! Tenemos nuestro widget que renderiza paginas web con el motor WebKit
class Simulador(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title('Pruebas de Gwibber, Webkit y otras shits')
        self.set_default_size(400, 400)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect('destroy', gtk.main_quit)
        
        messages = MessageStreamView()
        
        vbox = gtk.VBox(False, 5)
        vbox.pack_start(messages, True, True, 0)
        
        self.add(vbox)
        self.show_all()
    
Simulador()
gtk.main()
