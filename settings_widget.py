from collections import OrderedDict
from enum import Enum

import ipywidgets as widgets


def settings_widget(cls):
    """Class decorator to generate a settings widget. This uses type annotation
    and default values syntax similar to dataclasses. The following example::
    
        class IC(Enum):
            randomized = 0
            single_pixel = 1
    
        @settings_widget
        class Settings:
            size: int        = 256
            generations: int = 200
            rule: int        = 30
            ic_type: IC
            
    Generates a list of IPyWidgets that can be used as follows::
    
        settings = Settings()
        layout = AppLayout(
            header=Label("Elementary Cellular Automata"),
            left_sidebar=settings.vbox(),
            center=widgets.interactive_output(f, {"settings": settings}),
            right_sidebar=Label("Stats"),
            footer=Label("(C) Netherlands eScience Center"))
    """
    cls._defaults = {}
    for k in cls.__annotations__:
        if hasattr(cls, k):
            cls._defaults[k] = getattr(cls, k)
            delattr(cls, k)
    
    def m_init(self, **kwargs):
        self.widgets = OrderedDict()
        for k, v in cls.__annotations__.items():
            if v is int:
                self.widgets[k] = widgets.IntText(value=0, description=k)
            elif issubclass(v, Enum):
                self.widgets[k] = widgets.Select(options=list(v), description=k)
            else:
                self.widgets[k] = widgets.Label(str(v))

            if k in cls._defaults:
                self.widgets[k].value = cls._defaults[k]
                
            if k in kwargs:
                self.widgets[k].value = v(kwargs[k])
        
    def m_getattr(self, key):
        return cls.__annotations__[key](self.widgets[key].value)
    
    def m_observe(self, handler, names, type='change'):
        for w in self.widgets.values():
            w.observe(handler, names, type)
    
    def m_value(self):
        return self
    
    def m_vbox(self):
        return widgets.VBox(list(self.widgets.values()))
    
    cls.__init__ = m_init
    cls.__getattr__ = m_getattr
    cls.observe = m_observe
    cls.value = property(m_value)
    return cls