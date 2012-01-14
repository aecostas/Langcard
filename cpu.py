#!/usr/bin/python

# Ejemplo de widget con Cairo
#
# Author: Wil Alvarez (aka Satanas)
# Oct 19, 2009

import gtk
import cairo

# Creamos una clase que herede de gtk.DrawingArea para usarla como canvas
class Cpu(gtk.DrawingArea):
    def __init__(self, parent):
        self.par = parent
        gtk.DrawingArea.__init__(self)
        # Nos conectamos al evento expose, pues alli es donde ocurre toda 
        # la diversion
        self.connect('expose-event', self.expose)
        self.set_size_request(130, 200)
    
    # Este evento se ejecuta cada vez que la aplicacion necesita redibujarse
    # o cuando cambiamos un valor y mandamos a redibujarla. Aqui se pintara
    # y se le dara forma al widget
    def expose(self, widget, event):
        # Aqui obtenemos el contexto de cairo
        cr = widget.window.cairo_create()
        cr.set_line_width(0.8)
        
        # Definimos un rectangulo para limitar el proceso de dibujado y asi
        # optimizar la operacion
        cr.rectangle(event.area.x, event.area.y, 
            event.area.width, event.area.height)
        cr.clip()
        
        cr.rectangle(0,0,130,200)
        cr.set_source_rgb(0, 0, 0)  # Establecemos el color de la brocha/pincel
        cr.fill()
        
        # Obtenemos el valor actual del slider
        x = (self.par.cur_value * 34) / 100
        
        # Dibujamos 34 barritas para el medidor y segun el valor de 'x'
        # decidimos si esta 'encendida' o no
        for i in range(34):
            if (i < 34 - x):
                cr.set_source_rgb(0.53, 0, 0)
            else:
                cr.set_source_rgb(1, 0, 0)
            
            h = 15 + (i*5)
            cr.rectangle(15,h,49,4)
            cr.fill()
            
            cr.rectangle(67,h,49,4)
            cr.fill()

# Creamos una ventana sencilla en PyGTK con el slider y el canvas
class PyApp(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        
        self.set_title('CPU Meter')
        self.set_size_request(200, 200)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect('destroy', gtk.main_quit)

        self.cur_value = 10
       
        vbox = gtk.VBox(False, 2)
        
        scale = gtk.VScale()
        scale.set_range(0, 100)
        scale.set_digits(0)
        scale.set_size_request(35, 160)
        scale.set_value(self.cur_value)
        scale.set_inverted(True)
        scale.connect('value-changed', self.on_changed)
        
        self.cpu = Cpu(self)
        
        hbox = gtk.HBox(False)
        hbox.pack_start(self.cpu)
        hbox.pack_start(scale)
        
        vbox.pack_start(hbox, True, True, 2)

        self.add(vbox)
        self.show_all()
        
    # Programamos el evento 'value-changed' de la barra para que con cada
    # cambio mande a redibujar al widget del medidor
    def on_changed(self, widget):
        self.cur_value = widget.get_value()
        self.cpu.queue_draw()


    def get_cur_value(self):
        return self.cur_value

PyApp()
gtk.main()
