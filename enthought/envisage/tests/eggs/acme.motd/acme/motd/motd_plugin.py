""" The 'Message of the Day' plugin """


# Enthought library imports.
from enthought.envisage.api import Plugin
from enthought.traits.api import Bool


class MOTDPlugin(Plugin):
    """ The 'Message of the Day' plugin """
    
    ###########################################################################
    # 'MOTD' interface.
    ###########################################################################

    #### 'MOTDPlugin' interface ###############################################

    started = Bool(False)
    stopped = Bool(False)
            
    ###########################################################################
    # 'IPlugin' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _id_default(self):
        """ Initializer. """

        return 'acme.motd.plugin'

    #### Methods ##############################################################
    
    def start(self):
        """ Start the plugin. """
        
        self.started = True
        self.stopped = False
        
        return

    def stop(self):
        """ Stop the plugin. """
        
        self.started = False
        self.stopped = True
        
        return

#### EOF ######################################################################
