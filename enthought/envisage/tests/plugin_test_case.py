""" Tests for plugins. """


# Standard library imports.
import random, unittest

# Enthought library imports.
from enthought.envisage.api import Application, ExtensionPoint, Plugin
from enthought.envisage.api import PluginManager, Service
from enthought.traits.api import HasTraits, Instance, Int, Interface, List, Str
from enthought.traits.api import implements


def listener(obj, trait_name, old, new):
    """ A useful trait change handler for testing! """

    listener.obj = obj
    listener.trait_name = trait_name
    listener.old = old
    listener.new = new

    return


class TestApplication(Application):
    """ The type of application used in the tests. """

    id = 'test'
    
    def _plugin_manager_default(self):
        """ Trait initializer. """

        return PluginManager(application=self)

    
class PluginTestCase(unittest.TestCase):
    """ Tests for plugins. """

    ###########################################################################
    # 'TestCase' interface.
    ###########################################################################

    def setUp(self):
        """ Prepares the test fixture before each test method is called. """

        return

    def tearDown(self):
        """ Called immediately after each test method has been called. """
        
        return
    
    ###########################################################################
    # Tests.
    ###########################################################################

    def test_service_trait_type(self):
        """ service trait type"""

        class Foo(HasTraits):
            pass

        class PluginA(Plugin):
            id = 'A'
            foo = Instance(Foo, (), service=True)

        class PluginB(Plugin):
            id = 'B'
            foo = Service(Foo)

        a = PluginA()
        b = PluginB()
        
        application = TestApplication(plugins=[a, b])
        application.start()

        # Make sure the services were registered.
        self.assertEqual(a.foo, b.foo)

        # Stop the application.
        application.stop()

        # Make sure the service was unregistered.
        self.assertEqual(None, b.foo)

        # You can't set service traits!
        self.failUnlessRaises(SystemError, setattr, b, 'foo', 'bogus')
        
        return

    def test_service(self):
        """ service """

        class Foo(HasTraits):
            pass

        class Bar(HasTraits):
            pass

        class Baz(HasTraits):
            pass
        
        class PluginA(Plugin):
            id = 'A'
            foo = Instance(Foo, (), service=True)
            bar = Instance(Bar, (), service=True)
            baz = Instance(Baz, (), service=True)

        a = PluginA()

        application = TestApplication(plugins=[a])
        application.start()

        # Make sure the services were registered.
        self.assertNotEqual(None, application.get_service(Foo))
        self.assertEqual(a.foo, application.get_service(Foo))

        self.assertNotEqual(None, application.get_service(Bar))
        self.assertEqual(a.bar, application.get_service(Bar))

        self.assertNotEqual(None, application.get_service(Baz))
        self.assertEqual(a.baz, application.get_service(Baz))

        application.stop()

        # Make sure the service was unregistered.
        self.assertEqual(None, application.get_service(Foo))
        self.assertEqual(None, application.get_service(Bar))
        self.assertEqual(None, application.get_service(Baz))

        return

    def test_service_protocol(self):
        """ service protocol """

        class IFoo(Interface):
            pass

        class IBar(Interface):
            pass
        
        class Foo(HasTraits):
            implements(IFoo, IBar)

        class PluginA(Plugin):
            id = 'A'
            foo = Instance(Foo, (), service=True, service_protocol=IBar)
            
        a = PluginA()
        
        application = TestApplication(plugins=[a])
        application.start()

        # Make sure the service was registered with the 'IBar' protocol.
        self.assertNotEqual(None, application.get_service(IBar))
        self.assertEqual(a.foo, application.get_service(IBar))

        application.stop()

        # Make sure the service was unregistered.
        self.assertEqual(None, application.get_service(IBar))

        return

    def test_multiple_trait_contributions(self):
        """ multiple trait contributions """

        class PluginA(Plugin):
            id = 'A'
            x  = ExtensionPoint(List, id='x')

        class PluginB(Plugin):
            id = 'B'

            x  = List([1, 2, 3], extension_point='x')
            y  = List([4, 5, 6], extension_point='x')

        a = PluginA()
        b = PluginB()

        application = TestApplication(plugins=[a, b])

        # We should get an error because the plugin has multiple traits
        # contributing to the same extension point.
        self.failUnlessRaises(ValueError, application.get_extensions, 'x')

        return


# Entry point for stand-alone testing.
if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
