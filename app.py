from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode,Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from pyvirtualdisplay import Display
from selenium import webdriver

class Compiler(object):
    @classmethod
    def connect(ctx):
        ctx.display = Display(visible=0, size=(1024, 768))
        ctx.display.start()

        ctx.driver = webdriver.Firefox()
        ctx.driver.get('http://www.codepad.org/')

    @classmethod
    def disconnect(ctx):
        	ctx.driver.close()
        	ctx.display.stop()

    @classmethod
    def chooseLang(ctx,lang):
        	a="//input[@name='lang' and @value='{0}']".format(lang)
        	lang_button=ctx.driver.find_elements_by_xpath(a)[0]
        	lang_button.click()

    @classmethod
    def private(ctx):
        	element_checkbox=ctx.driver.find_element_by_name("private")
        	element_checkbox.click()

    @classmethod
    def pasteCode(ctx,code):
        	code_area = ctx.driver.find_element_by_id("textarea")
        	code_area.send_keys(code)

    @classmethod
    def run(ctx):
        	submit_button = ctx.driver.find_element_by_name("submit")
        	submit_button.click()

    @classmethod
    def out(ctx):
        for element in ctx.driver.find_elements_by_xpath("""//div[@class='code'][2]/
        table/tbody/tr/td[2]/div[@class='highlight']/pre"""):
        	return element.text

class MyService(ServiceBase):

    @rpc(Unicode,Unicode,Boolean,_returns=(Unicode))
    def compile(ctx,lang,code,private):
        """
        @param lang the compiler lang
        @param times the number of times to say hello
        @return the completed array
        """
        if(lang==1):
            lang='Python'

    	dd=Compiler()
        dd.connect()
    	driver,display=dd.driver,dd.display
    	dd.chooseLang(lang)
        if(private):
    	       dd.private()

        dd.pasteCode(code)
    	dd.run()
    	resp = dd.out()
    	dd.disconnect()
    	return resp


application = Application([MyService], 'spyne.pyCompile.pyCompile',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("Listening to http://127.0.0.1:1234")
    logging.info("Wsdl is at: http://localhost:1234/?wsdl")

    server = make_server('127.0.0.1', 1234, wsgi_application)
    server.serve_forever()
